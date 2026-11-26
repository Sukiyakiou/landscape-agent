nums = list(range(1, 21))
for x in nums[:5]:
    print(x)
for x in nums[-5:]:
    print(x)
for x in nums:
    if x % 2 == 0:
        print(x)
for x in nums[::-1]:
    print(x)

