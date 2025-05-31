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


n = var('n', domain='integer')
m = var('m', domain='integer')
j = var('j', domain='integer')

f(n) = 1 / 2

# m = 1
# f = sum(j * m * f(j) * factorial(n) * factorial(m + j) / (factorial(j) * factorial(m + n + 1)), j, 0, n)
# print(f)



# f(n, m) = factorial(m) * n^(n+m) / factorial(n + m) - sum(binomial(n, r) * factrial(m) * f(m+n-r, m) / factorial(n + m - r), (r, 1, n-1))

