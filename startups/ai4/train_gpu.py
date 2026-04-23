"""
GPU対応・本格学習スクリプト (一晩放置用)

構成:
  - マルチプロセスで自己対戦を並列化 (CPUコアを全部使う)
  - NN推論はGPU (ROCm/CUDA/MPS対応、なければCPU)
  - 学習もGPU
  - チェックポイント保存 (中断→再開可能)
  - 学習曲線のログ出力
  - 定期的に旧バージョンと対戦して強さを測定

使い方:
    python train_gpu.py                        # 自動でGPU検出
    python train_gpu.py --device cuda          # CUDA指定
    python train_gpu.py --device rocm          # ROCm (AMD)
    python train_gpu.py --device mps           # Apple Silicon
    python train_gpu.py --resume checkpoint.pt # 途中から再開

推奨パラメータ (一晩放置):
    デフォルトのまま実行すれば OK。
    約8〜12時間で 50イテレーション x 100ゲーム = 5000ゲームの自己対戦。
"""

from __future__ import annotations
import argparse
import json
import math
import os
import random
import time
from copy import deepcopy
from datetime import datetime
from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from startups import StartupsGame, NUM_PLAYERS
from network import PolicyValueNet
from encoding import (
    encode_observation,
    get_legal_action_mask,
    get_legal_action_map,
    action_to_index_with_game,
    OBSERVATION_SIZE,
    ACTION_SIZE,
)
from determinize import determinize_from_observation
from az_ismcts import AlphaZeroISMCTS, AZNode
from self_play import TrainingSample


# ============================================================
# デバイス検出
# ============================================================

def detect_device(requested: str = "auto") -> torch.device:
    """使用可能なデバイスを検出する。"""
    if requested == "auto":
        if torch.cuda.is_available():
            name = torch.cuda.get_device_name(0)
            # ROCm は torch.cuda として見える (HIP backend)
            print(f"  GPU 検出: {name}")
            if "AMD" in name or "Radeon" in name or "gfx" in name.lower():
                print(f"  -> AMD GPU (ROCm/HIP backend)")
            else:
                print(f"  -> NVIDIA GPU (CUDA)")
            return torch.device("cuda")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            print("  GPU 検出: Apple Silicon (MPS)")
            return torch.device("mps")
        else:
            print("  GPU なし → CPU で実行")
            return torch.device("cpu")
    elif requested in ("cuda", "rocm"):
        if not torch.cuda.is_available():
            print("  警告: CUDA/ROCm が利用不可。CPU にフォールバック")
            return torch.device("cpu")
        return torch.device("cuda")
    elif requested == "mps":
        if not (hasattr(torch.backends, "mps") and torch.backends.mps.is_available()):
            print("  警告: MPS が利用不可。CPU にフォールバック")
            return torch.device("cpu")
        return torch.device("mps")
    else:
        return torch.device(requested)


# ============================================================
# 並列自己対戦 (マルチプロセス)
# ============================================================

def _self_play_worker(args):
    """1ゲーム分の自己対戦ワーカー (子プロセスで実行)。

    NN は state_dict をシリアライズして渡す (子プロセスでロード)。
    GPU は使わない (子プロセスごとにGPUコンテキストを作るとメモリが爆発)。
    → 子プロセスは CPU で推論、親プロセスが GPU で学習。
    """
    state_dict_bytes, hidden, num_layers, mcts_iters, seed, temperature_moves = args

    # NN をCPUで再構築
    net = PolicyValueNet(hidden=hidden, num_layers=num_layers)
    sd = torch.load(
        torch.io.BytesIO(state_dict_bytes) if hasattr(torch, "io") else None,
        weights_only=True,
        map_location="cpu",
    )
    # BytesIOが使えない場合のフォールバック
    if sd is None:
        import io
        sd = torch.load(io.BytesIO(state_dict_bytes), weights_only=True, map_location="cpu")
    net.load_state_dict(sd)
    net.eval()

    rng = random.Random(seed)
    game = StartupsGame(seed=rng.randint(0, 10**9))

    agents = [
        AlphaZeroISMCTS(
            net=net, iterations=mcts_iters,
            rng=random.Random(rng.randint(0, 10**9)),
            add_dirichlet_noise=True,
        )
        for _ in range(NUM_PLAYERS)
    ]

    pending = [[] for _ in range(NUM_PLAYERS)]
    move_count = 0

    while not game.is_terminal():
        pid = game.current_player()
        obs = game.get_observation(pid)
        state_vec = encode_observation(obs)
        mask = get_legal_action_mask(game)
        action, policy_vec = agents[pid].search(game, root_player=pid, return_policy=True)
        pending[pid].append((state_vec, policy_vec, mask))

        if move_count < temperature_moves and policy_vec.sum() > 0:
            sampled_idx = np.random.choice(len(policy_vec), p=policy_vec)
            action_map = get_legal_action_map(game)
            if sampled_idx in action_map:
                action = action_map[sampled_idx]

        game.step(action)
        move_count += 1

    rewards = game.get_rewards()
    point_to_value = {2: 1.0, 1: 0.0, -1: -1.0}
    values = [point_to_value.get(rewards[pid], 0.0) for pid in range(NUM_PLAYERS)]

    samples = []
    for pid in range(NUM_PLAYERS):
        for state, policy, mask in pending[pid]:
            samples.append((state, policy, values[pid], mask))

    winner = game.get_winner()
    return samples, rewards, winner


def _serialize_state_dict(net: PolicyValueNet) -> bytes:
    """state_dict をバイト列にシリアライズ (子プロセスに渡すため)。"""
    import io
    buf = io.BytesIO()
    torch.save(net.state_dict(), buf)
    return buf.getvalue()


def parallel_self_play(
    net: PolicyValueNet,
    num_games: int,
    mcts_iters: int,
    num_workers: int,
    hidden: int,
    num_layers: int,
    base_seed: int = 0,
    temperature_moves: int = 12,
) -> tuple[list[TrainingSample], dict]:
    """マルチプロセスで自己対戦を並列実行。"""
    sd_bytes = _serialize_state_dict(net)

    args_list = [
        (sd_bytes, hidden, num_layers, mcts_iters, base_seed + g, temperature_moves)
        for g in range(num_games)
    ]

    all_samples = []
    wins = [0] * NUM_PLAYERS
    done = 0
    start = time.time()

    with Pool(processes=num_workers) as pool:
        for result in pool.imap_unordered(_self_play_worker, args_list):
            raw_samples, rewards, winner = result
            for s, p, v, m in raw_samples:
                all_samples.append(TrainingSample(state=s, policy=p, value=v, legal_mask=m))
            wins[winner] += 1
            done += 1
            if done % max(1, num_games // 10) == 0:
                elapsed = time.time() - start
                rate = done / elapsed
                eta = (num_games - done) / rate if rate > 0 else 0
                print(f"    {done}/{num_games} games ({rate:.1f} games/s, ETA {eta:.0f}s)")

    elapsed = time.time() - start
    stats = {
        "games": num_games,
        "samples": len(all_samples),
        "wins": wins,
        "time": elapsed,
        "games_per_sec": num_games / elapsed,
    }
    return all_samples, stats


# ============================================================
# 子プロセスワーカー (BytesIOフォールバック版)
# ============================================================

# _self_play_worker を修正: BytesIO を使う安全な版
def _self_play_worker(args):
    import io as _io
    state_dict_bytes, hidden, num_layers, mcts_iters, seed, temperature_moves = args

    net = PolicyValueNet(hidden=hidden, num_layers=num_layers)
    buf = _io.BytesIO(state_dict_bytes)
    sd = torch.load(buf, weights_only=True, map_location="cpu")
    net.load_state_dict(sd)
    net.eval()

    rng = random.Random(seed)
    game = StartupsGame(seed=rng.randint(0, 10**9))

    agents = [
        AlphaZeroISMCTS(
            net=net, iterations=mcts_iters,
            rng=random.Random(rng.randint(0, 10**9)),
            add_dirichlet_noise=True,
        )
        for _ in range(NUM_PLAYERS)
    ]

    pending = [[] for _ in range(NUM_PLAYERS)]
    move_count = 0

    while not game.is_terminal():
        pid = game.current_player()
        obs = game.get_observation(pid)
        state_vec = encode_observation(obs)
        mask = get_legal_action_mask(game)
        action, policy_vec = agents[pid].search(game, root_player=pid, return_policy=True)
        pending[pid].append((state_vec, policy_vec, mask))

        if move_count < temperature_moves and policy_vec.sum() > 0:
            sampled_idx = np.random.choice(len(policy_vec), p=policy_vec)
            action_map = get_legal_action_map(game)
            if sampled_idx in action_map:
                action = action_map[sampled_idx]

        game.step(action)
        move_count += 1

    rewards = game.get_rewards()
    point_to_value = {2: 1.0, 1: 0.0, -1: -1.0}
    values = [point_to_value.get(rewards[pid], 0.0) for pid in range(NUM_PLAYERS)]

    samples = []
    for pid in range(NUM_PLAYERS):
        for state, policy, mask in pending[pid]:
            samples.append((state, policy, values[pid], mask))

    return samples, rewards, game.get_winner()


# ============================================================
# GPU 学習
# ============================================================

def train_on_gpu(
    net: PolicyValueNet,
    samples: list[TrainingSample],
    device: torch.device,
    epochs: int = 5,
    batch_size: int = 256,
    lr: float = 1e-3,
    lr_schedule: bool = True,
) -> dict:
    """GPU上でNNを学習。"""
    net.to(device)
    net.train()

    states = torch.from_numpy(np.stack([s.state for s in samples])).float().to(device)
    policies = torch.from_numpy(np.stack([s.policy for s in samples])).float().to(device)
    values = torch.from_numpy(np.array([s.value for s in samples], dtype=np.float32)).to(device)
    masks = torch.from_numpy(np.stack([s.legal_mask for s in samples])).float().to(device)

    dataset = TensorDataset(states, policies, values, masks)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=False)

    optimizer = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = None
    if lr_schedule:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    history = {"loss": [], "policy_loss": [], "value_loss": [], "lr": []}

    for ep in range(epochs):
        ep_loss = ep_pl = ep_vl = 0.0
        n_batches = 0
        for s, p, v, m in loader:
            logits, pred_v = net(s)
            pred_v = pred_v.squeeze(-1)

            masked_logits = logits.clone()
            masked_logits[m == 0] = -1e9
            log_probs = F.log_softmax(masked_logits, dim=1)
            policy_loss = -(p * log_probs * m).sum(dim=1).mean()
            value_loss = F.mse_loss(pred_v, v)

            loss = policy_loss + value_loss
            optimizer.zero_grad()
            loss.backward()
            # 勾配クリッピング (学習安定化)
            torch.nn.utils.clip_grad_norm_(net.parameters(), max_norm=1.0)
            optimizer.step()

            ep_loss += loss.item()
            ep_pl += policy_loss.item()
            ep_vl += value_loss.item()
            n_batches += 1

        if scheduler:
            scheduler.step()

        avg = ep_loss / max(1, n_batches)
        avg_pl = ep_pl / max(1, n_batches)
        avg_vl = ep_vl / max(1, n_batches)
        cur_lr = optimizer.param_groups[0]["lr"]
        history["loss"].append(avg)
        history["policy_loss"].append(avg_pl)
        history["value_loss"].append(avg_vl)
        history["lr"].append(cur_lr)
        print(f"    epoch {ep+1}/{epochs}: loss={avg:.4f} (P={avg_pl:.4f} V={avg_vl:.4f}) lr={cur_lr:.6f}")

    net.to("cpu")  # 推論は子プロセスCPUなので戻す
    return history


# ============================================================
# 評価 (旧モデルと対戦)
# ============================================================

def evaluate(
    new_net: PolicyValueNet,
    old_net: PolicyValueNet,
    num_games: int = 30,
    mcts_iters: int = 50,
) -> dict:
    """new_net (P0) vs old_net (P1, P2) で対戦。"""
    new_agent = AlphaZeroISMCTS(net=new_net, iterations=mcts_iters, rng=random.Random(0))
    old_agent1 = AlphaZeroISMCTS(net=old_net, iterations=mcts_iters, rng=random.Random(1))
    old_agent2 = AlphaZeroISMCTS(net=old_net, iterations=mcts_iters, rng=random.Random(2))

    wins = [0, 0, 0]
    for g in range(num_games):
        game = StartupsGame(seed=g + 50000)
        agents = [new_agent, old_agent1, old_agent2]
        while not game.is_terminal():
            pid = game.current_player()
            action = agents[pid].search(game, root_player=pid)
            game.step(action)
        wins[game.get_winner()] += 1

    new_wr = wins[0] / num_games * 100
    return {"new_wins": wins[0], "old_wins": wins[1] + wins[2], "new_winrate": new_wr}


# ============================================================
# メインループ
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="スタータップス 本格学習 (GPU対応)")
    parser.add_argument("--device", default="auto", help="cuda / rocm / mps / cpu / auto")
    parser.add_argument("--resume", default=None, help="チェックポイントから再開")
    parser.add_argument("--hidden", type=int, default=128, help="NN 隠れ層サイズ")
    parser.add_argument("--layers", type=int, default=4, help="NN 層数")
    parser.add_argument("--iterations", type=int, default=50, help="学習イテレーション数")
    parser.add_argument("--games", type=int, default=100, help="1イテレーションの自己対戦ゲーム数")
    parser.add_argument("--mcts-iters", type=int, default=80, help="MCTS探索回数")
    parser.add_argument("--epochs", type=int, default=5, help="1イテレーションの学習エポック数")
    parser.add_argument("--batch-size", type=int, default=256, help="学習バッチサイズ")
    parser.add_argument("--lr", type=float, default=1e-3, help="初期学習率")
    parser.add_argument("--buffer-size", type=int, default=50000, help="経験バッファ最大サイズ")
    parser.add_argument("--workers", type=int, default=0, help="並列ワーカー数 (0=自動)")
    parser.add_argument("--eval-interval", type=int, default=5, help="評価を行うイテレーション間隔")
    parser.add_argument("--eval-games", type=int, default=30, help="評価対戦数")
    parser.add_argument("--save-dir", default="checkpoints", help="チェックポイント保存先")
    args = parser.parse_args()

    # ── 初期化 ──
    print("=" * 60)
    print("  スタータップス AlphaZero 学習 (GPU対応)")
    print("=" * 60)

    device = detect_device(args.device)
    num_workers = args.workers if args.workers > 0 else max(1, cpu_count() - 1)
    print(f"  並列ワーカー数: {num_workers}")
    print(f"  NN: hidden={args.hidden}, layers={args.layers}")
    print(f"  学習: {args.iterations} iterations x {args.games} games x {args.mcts_iters} MCTS")
    print(f"  推定所要時間: ゲーム速度に依存 (初回で見積もり)")

    save_dir = Path(args.save_dir)
    save_dir.mkdir(exist_ok=True)

    # NN 構築
    net = PolicyValueNet(hidden=args.hidden, num_layers=args.layers)
    start_iter = 0
    all_samples = []
    log_entries = []

    if args.resume:
        print(f"\n  チェックポイントから再開: {args.resume}")
        ckpt = torch.load(args.resume, weights_only=False, map_location="cpu")
        net.load_state_dict(ckpt["model"])
        start_iter = ckpt.get("iteration", 0)
        log_entries = ckpt.get("log", [])
        print(f"  → iteration {start_iter} から再開")

    n_params = sum(p.numel() for p in net.parameters())
    print(f"  パラメータ数: {n_params:,}")

    # 旧モデル (評価用)
    best_net = PolicyValueNet(hidden=args.hidden, num_layers=args.layers)
    best_net.load_state_dict(net.state_dict())

    print(f"\n{'─' * 60}")
    total_start = time.time()

    for it in range(start_iter, args.iterations):
        iter_start = time.time()
        print(f"\n  ===== Iteration {it+1}/{args.iterations} =====")

        # ── 自己対戦 ──
        print(f"  [Self-play] {args.games} games, {args.mcts_iters} MCTS iters, {num_workers} workers")
        sp_start = time.time()
        new_samples, sp_stats = parallel_self_play(
            net,
            num_games=args.games,
            mcts_iters=args.mcts_iters,
            num_workers=num_workers,
            hidden=args.hidden,
            num_layers=args.layers,
            base_seed=it * 100000,
        )
        sp_time = time.time() - sp_start
        print(f"    -> {sp_stats['samples']} samples, {sp_stats['games_per_sec']:.1f} games/s, {sp_time:.0f}s")
        print(f"    勝率: P0={sp_stats['wins'][0]} P1={sp_stats['wins'][1]} P2={sp_stats['wins'][2]}")

        # 経験バッファ
        all_samples.extend(new_samples)
        if len(all_samples) > args.buffer_size:
            all_samples = all_samples[-args.buffer_size:]
        print(f"    経験バッファ: {len(all_samples)} samples")

        # ── 学習 ──
        print(f"  [Train] {len(all_samples)} samples, {args.epochs} epochs, device={device}")
        tr_start = time.time()
        # LR を後半で下げる
        current_lr = args.lr * (0.1 ** (it // max(1, args.iterations // 3)))
        history = train_on_gpu(
            net, all_samples, device,
            epochs=args.epochs, batch_size=args.batch_size, lr=current_lr,
        )
        tr_time = time.time() - tr_start
        final_loss = history["loss"][-1]
        print(f"    -> loss={final_loss:.4f}, {tr_time:.1f}s")

        # ── 評価 ──
        eval_result = None
        if (it + 1) % args.eval_interval == 0 or it == args.iterations - 1:
            print(f"  [Eval] new vs best, {args.eval_games} games")
            eval_result = evaluate(net, best_net, num_games=args.eval_games, mcts_iters=50)
            print(f"    -> new winrate: {eval_result['new_winrate']:.1f}% ({eval_result['new_wins']}/{args.eval_games})")

            # 55%以上なら best を更新
            if eval_result["new_winrate"] >= 55:
                print(f"    ★ ベストモデル更新!")
                best_net.load_state_dict(net.state_dict())
                torch.save(net.state_dict(), save_dir / "best.pt")

        # ── ログ ──
        iter_time = time.time() - iter_start
        entry = {
            "iteration": it + 1,
            "loss": final_loss,
            "policy_loss": history["policy_loss"][-1],
            "value_loss": history["value_loss"][-1],
            "samples_total": len(all_samples),
            "sp_time": sp_time,
            "tr_time": tr_time,
            "iter_time": iter_time,
            "games_per_sec": sp_stats["games_per_sec"],
        }
        if eval_result:
            entry["eval_winrate"] = eval_result["new_winrate"]
        log_entries.append(entry)

        # ── チェックポイント保存 ──
        ckpt_path = save_dir / f"iter_{it+1:04d}.pt"
        torch.save({
            "model": net.state_dict(),
            "iteration": it + 1,
            "log": log_entries,
            "args": vars(args),
        }, ckpt_path)
        # latest.pt を常に最新に
        torch.save({
            "model": net.state_dict(),
            "iteration": it + 1,
            "log": log_entries,
            "args": vars(args),
        }, save_dir / "latest.pt")

        total_elapsed = time.time() - total_start
        remaining_iters = args.iterations - it - 1
        eta = remaining_iters * iter_time
        print(f"  [{iter_time:.0f}s] 総経過: {total_elapsed/60:.1f}分, 残り推定: {eta/60:.1f}分")

    # ── 完了 ──
    total_time = time.time() - total_start
    print(f"\n{'=' * 60}")
    print(f"  学習完了! 総時間: {total_time/3600:.1f}時間")
    print(f"  最終モデル: {save_dir / 'latest.pt'}")
    print(f"  ベストモデル: {save_dir / 'best.pt'}")

    # 最終モデルを az_net_trained.pt としてもコピー
    torch.save(net.state_dict(), "az_net_trained.pt")
    print(f"  -> az_net_trained.pt に最終モデルをコピー")

    # ログをJSONで保存
    with open(save_dir / "training_log.json", "w") as f:
        json.dump(log_entries, f, indent=2)
    print(f"  -> {save_dir / 'training_log.json'} にログ保存")

    # ── 最終成績表示 ──
    if log_entries:
        print(f"\n  学習曲線:")
        for e in log_entries:
            wr = f"  eval={e['eval_winrate']:.1f}%" if "eval_winrate" in e else ""
            print(f"    iter {e['iteration']:3d}: loss={e['loss']:.4f} "
                  f"({e['games_per_sec']:.1f} g/s){wr}")


if __name__ == "__main__":
    main()
