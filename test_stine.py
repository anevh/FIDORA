A = []

A.append([1,2,3])

print(A)

A.append([10])

print(A)

B = [8,9,11]

for i in range(len(B)):
    A[1].append(B[i])

print(A)