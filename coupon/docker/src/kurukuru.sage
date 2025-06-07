import functools

# x = var('x')
# n = var('n', domain='integer')
#
# f(x) = ((exp(x)-1) / x)^n
#
# k = 9
# df = f
# for _ in range(k):
#     df = diff(df, x)
#
# v = limit(df, x = 0)
# print(v)

# m = 1
# f = sum(j * m * f(j) * factorial(n) * factorial(m + j) / (factorial(j) * factorial(m + n + 1)), j, 0, n)
# print(f)

# A = Matrix(
#     [
#         [6^4, 6^3, 6^2, 6^1, 1],
#         [7^4, 7^3, 7^2, 7^1, 1],
#         [8^4, 8^3, 8^2, 8^1, 1],
#         [9^4, 9^3, 9^2, 9^1, 1],
#         [10^4, 10^3, 10^2, 10^1, 1],
#     ]
# )

# v = vector([
#     2^6/(252 * 6*5*4*3*2*1),
#     2^7/(72 * 7*6*5*4*3*2),
#     2^8/(64 * 8*7*6*5*4*3),
#     -5 * 2^9/(384 * 9*8*7*6*5*4),
#     -745 * 2^10/(9216 * 10*9*8*7*6*5),
# ])
# print(A.solve_right(v))

# f(n, m) = factorial(m) * n^(n+m) / factorial(n + m) - sum(binomial(n, r) * factrial(m) * f(m+n-r, m) / factorial(n + m - r), (r, 1, n-1))


m = var('m', domain='integer')
n = var('n', domain='integer')

def mp(k):
    g = 1
    for i in range(k):
        g *= (m - i)
    return g

f(m) = (mp(12) / (2^10*3^8*5) - mp(10) / (2^6*3^6*5) + mp(8) * 101 / (2^5*3^5*5^2*7)) / 2^m
print(f)
print(f(10))

f(m) = (mp(10) / (2^8*3^6*5) - mp(8) / (2^5*3^4*5) + mp(6) / (3^4*5*7)) / 2^m
print(f(7))

# g(m) = mp(6) * (m^4 - 30 * m^3 + 263 * m^2 - 714 * m + 2304/7) / (2^8*3^6*5 * 2^m)
# g(m) = (mp(10)- mp(6) * 72 * ((m-6) * (m-7) - 32/7)) / (2^8*3^6*5 * 2^m)
# print(g(6))

def getOtherB(dim):
    k = var('k', domain='integer')
    n = var('n', domain='integer')
    m = var('m', domain='integer')

    p(n, m) = (1/n^(n+m)) * sum((-1)^(n-k) * binomial(n, k) * k^(n+m), k, 0, n)

    b(n, m) = factorial(m)/factorial(n+m) * sum((-1)^(n-k) * binomial(n, k) * k^(n+m), k, 0, n)

    A = Matrix(
        [[(i+1)^(j+1) for j in range(dim)] for i in range(dim)]
    )
    # v = vector([b(i + 1, dim).unhold() * 2^dim for i in range(dim)])
    v = vector([b(i + 1, dim).unhold() for i in range(dim)])

    a = list(A.solve_right(v))
    a.reverse()

    return a

@functools.cache
def getOtherP(i):
    if i == 0:
        return 1

    startM = i + 2
    term = i // 2 + (i % 2)

    A = Matrix(
        [[mp(k)(m=m) for k in range(i * 2, i * 2 - term * 2, -2)] for m in range(i + 2, i + 2 + 2 * term, 2)]
    )
    v = vector([getOtherB(m)[i] * 2^m for m in range(i + 2, i + 2 + 2 * term, 2)])
    a = list(A.solve_right(v))

    r = 0
    for p, c in zip([mp(k)(m=m) for k in range(i * 2, i * 2 - term * 2, -2)], a):
        r += p * c
    return r

def getP(vi):
    p0(m) = mp(0)
    p1(m) = mp(2) / (2*3)

    p2(m) = mp(4) / (2^3*3^2)
    p3(m) = mp(6) / (2^4*3^4) - mp(4) / (2^2*3^2*5)

    p4(m) = mp(8) / (2^7*3^5) - mp(6) / (2^3*3^3*5)
    p5(m) = mp(10) / (2^8*3^6*5) - mp(8) / (2^5*3^4*5) + mp(6) / (3^4*5*7)

    p6(m) = mp(12) / (2^10*3^8*5) - mp(10) / (2^6*3^6*5) + mp(8) * 101 / (2^5*3^5*5^2*7)
    p7(m) = mp(14) / (2^11*3^9*5*7) - mp(12) / (2^9*3^7*5) + mp(10) * 61 / (2^6*3^6*5^2*7) - mp(8) / (2^3*3^3*5^2*7)

    p8(m) = mp(16) / (2^15*3^10*5*7) - mp(14) / (2^10*3^8*5^2) + mp(12) * 101 / (2^8*3^7*5^2*7) - mp(10) * (13/576) / (14175/4)
    p9(m) = mp(18) / (2^16*3^13*5*7) - mp(16) / (2^12*3^10*5^2) + mp(14) * 101 / (2^9*3^9*5^2*7) - mp(12) * (13/576) / (14175/4) + mp(10) * (1/132) / (14175/4)

    p10(m) = mp(20) / (2^15*3^10*5*7) - mp(18) / (2^10*3^8*5^2) + mp(16) * 101 / (2^8*3^7*5^2*7) - mp(14) * (13/576) / (14175/4) + mp(12) * (1/132) / (14175/4)
    p11(m) = mp(18) / (2^15*3^10*5*7) - mp(16) / (2^10*3^8*5^2) + mp(14) * 101 / (2^8*3^7*5^2*7) - mp(12) * (13/576) / (14175/4) + mp(10) * (1/132) / (14175/4)

    ps = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]
    return ps[vi]

@functools.cache
def getB(vm):
    if vm == 0:
        return 1

    f = 0
    for i in range(vm):
        f += getOtherP(i) * n ^ (vm - i)

    return (f / 2^m)(m=vm)

print("-----------")
# print(getB(8)(n=1))
# print(getB(8)(n=2))
# print(getB(9)(n=1))
# print(getB(9)(n=2))

# A = Matrix(
#     [
#         [1, 1],
#         [4, 2],
#     ]
# )
#
# v = vector([
#     1/9 - getB(8)(n=1),
#     511/45 - getB(8)(n=2),
# ])
# print(v)
# print(A.solve_right(v))


print("-----------")

print(getB(2))
print(getB(3))
# print(getB(10))
# print(getB(11))
for vm in range(1, 3):
    diff = (n + vm) * getB(vm) - n * getB(vm)(n=n-1) - n * vm * getB(vm - 1)
    print(vm, diff.collect(n))


# m = 12
# print()
# print(p0(m) / 2 ^ m)
# print(p1(m) / 2 ^ m)
# print(p2(m) / 2 ^ m)
# print(p3(m) / 2 ^ m)
# print(p4(m) / 2 ^ m)
# print(p5(m) / 2 ^ m)
# print(p6(m) / 2 ^ m)
# print(p7(m) / 2 ^ m)
# print(p8(m) / 2 ^ m)


print("------------------------------")
# or vi in range(1, 13):
#    p = getOtherP(vi)
#    print(p.collect(m))
#     s = "\\phi_{" + str(vi) + "}(m) &= "
#     for i, pp in enumerate(p):
#         if pp.numerator() == 0:
#             continue
#
#         sgn = 1 if pp.numerator() > 0 else -1
#         s += (" + " if sgn == 1 else " - ") + "\\frac{" + str(sgn * pp.numerator() * mp(2*vi - 2*i)).replace("*", "") + "}{" + str(pp.denominator()) + "}"
#     print(s + " \\\\")

for vm in range(1, 10):
    p = getOtherB(vm)
    s = "B_{" + str(vm) + "}^{(-n)} &= "
    for i, pp in enumerate(p):
        if pp.numerator() == 0:
            s += " &"
            continue

        sgn = 1 if pp.numerator() > 0 else -1
        s += (" &+ " if sgn == 1 else " &- ") + "\\frac{" + str(sgn * pp.numerator()) + "}{" + str(pp.denominator()) + "}" + ("n" if vm - i == 1 else "n^{" + str(vm - i) + "}")
    print(s + (" &" * (8 - i)) + " \\\\")

print("------------------------------")
