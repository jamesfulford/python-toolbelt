# logistics.py
# by James Fulford
# 2/21/17 in class

from matplotlib import pyplot as plt


def growth(capacity, max_grow):
	return lambda x: (-max_grow * x / float(capacity)) + max_grow


# Parameters:
x = 10
K = 7000  # defines carrying capacity
R = -.18  # defines fastest growth rate
epsilon = .1  # defines what is close enough
max_iterations = 200



r = growth(K, R)
values = [x]
print str(0) + ":", x
for i in range(1, max_iterations):
    x += r(x) * x
    values.append(x)
    print str(i) + ":", x
    if abs(x - K) < epsilon or abs(x) < epsilon:
        print "Completed after", i, "iterations."
        break

plt.plot(values)
plt.show()


