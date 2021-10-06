import math
a = [
    [1, 1, 0, 1, 1],
    [0,1, 0, 1, 0]
    ]
b = []
temp = 0
for idx, row in enumerate(a):
    for idx, col in enumerate(row):
        temp += col * math.pow(2, idx)  
    b.append(int(temp))
    temp = 0
print("a:", a)
print("b:", b)

print("a[0]:", a[0])
print("(b[0] >> 0) & 1:", (b[0] >> 0) & 1)
print("(b[0] >> 1) & 1:", (b[0] >> 1) & 1)
print("(b[0] >> 2) & 1:", (b[0] >> 2) & 1)
print("(b[0] >> 3) & 1:", (b[0] >> 3) & 1)
print("(b[0] >> 4) & 1:", (b[0] >> 4) & 1)