import matplotlib.pyplot as plt
import numpy as np

points = []
patches = []
patches_type = []
fitness = []
file="log_mergesort"

with open(file) as file:
    while line := file.readline():
        if "location: MyBuggy.java" in line:
            points.append(line.split("location: MyBuggy.java")[1].rstrip())
        if "operation: OP_INSTANCE:" in line:
            # patches_type.append((next(file, '').strip()).split(":")[0])
            patches.append((next(file, '').strip()))
        if ", fitness" in line:
            fitness.append(float(line.split("fitness ")[1].rstrip()))

points.sort()

# === fitness ===

# plt.plot(fitness)

# plt.xlabel("Iterations")
# plt.ylabel("Fitness Value")

# === patches type ===

# lines, counts = np.unique(patches, return_counts=True)

# for i, v in enumerate(counts):
#     plt.text(lines[i], v + 3, str(v), horizontalalignment='center', verticalalignment='center')
#     if(v > 1):
#         print("Repeated for " + str(v) + " times for the following line:")
#         print(lines[i])

# plt.bar(lines, counts, align='center')

# plt.xlabel("Type of Operation")
# plt.ylabel("Number of Attempt")

# === line of fix ===

lines, counts = np.unique(points, return_counts=True)

for i, v in enumerate(counts):
    plt.text(lines[i], v + 1, str(v), horizontalalignment='center', verticalalignment='center')

plt.bar(lines, counts, align='center')

plt.xlabel("Location (Line Number)")
plt.ylabel("Number of Attempt")

plt.show()