ackley = (2 * [(-32, 32)], lambda x: -20 * exp(-0.2 * sqrt(1 / len(x) * sum(v ** 2 for v in x))) - exp(1 / len(x) * sum(cos(2 * pi * v) for v in x)) + 20 + exp(1))

ackley2 = (2 * [(-32, 32)], lambda x: -200 * exp(-0.2 * sqrt(x[0] ** 2 + x[1] ** 2)))

ackley3 = (2 * [(-32, 32)], lambda x: -200 * exp(-0.2 * sqrt(x[0] ** 2 + x[1] ** 2)) + 5 * exp(cos(3 * x[0]) + sin(3 * x[1])))

ackley4 = (2 * [(-35, 35)], lambda x: sum(exp(-0.2) * sqrt(x[i] ** 2 + x[i + 1] ** 2) + 3 * (cos(2 * x[i]) + sin(2 * x[i + 1])) for i in range(len(x) - 1)))

easom = (2 * [(-100, 100)], lambda x: -cos(x[0]) * cos(x[1]) * exp(-(x[0] - pi) ** 2 - (x[1] - pi) ** 2))

rastrigin = (2 * [(-5.12, 5.12)], lambda x: 10 * len(x) + sum(v ** 2 - 10 * cos(2 * pi * v) for v in x))

rosenbrock = (2 * [(-5, 10)], lambda x: sum(100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2 for i in range(len(x) - 1)))

schaffer4 = (2 * [(-100, 100)], lambda x: 0.5 + (cos(sin(abs(x[0] ** 2 - x[1] ** 2))) ** 2 - 0.5) / (1 + 0.001 * (x[0] ** 2 + x[1] ** 2)) ** 2)
