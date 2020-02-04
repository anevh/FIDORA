########################## En fil kun for testing av syntax etc ########################

"""
a = "HEI"

print(type(a))

a = "3"

try:
    a = float(a)
    print(a)
    print(type(a))
except:
    print("did not work")

"""

A = [[2, 6], [3, 3], [1,9]]
A = sorted(A,key=lambda l:l[0])
print(A[0])

A.append([3,2])
print(A[0][:])

print(A)
if 2 in A[1]:
    print("Ja")
if not [3,4] in A:
    print("Nei")


list1 = [item[0] for item in A]
print(list1)
