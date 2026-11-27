nums =  range(1,101)
n = 0
for x in nums:
    if (x % 3 == 0) != (x % 5 == 0):
        print(x)
        n += 1
print(n)
