

k = var('k', domain='integer')
p(n, r, s) = (1 / (binomial(n, s) ^ r)) * sum((-1) ^ (n - k) * binomial(n, k) * binomial(k, s) ^ r, k, s, n)

print(float(simplify(p(11, 10, 3))))
