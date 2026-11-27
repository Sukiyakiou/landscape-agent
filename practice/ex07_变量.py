def is_prime(n):
    count = 0
    for x in range(2,int(n**0.5) + 1):
        if n % x == 0:
            count += 1
    if count > 1:
        return False
    else:
        return True
for x in range(2,51):
    if is_prime(x):
        print(x)

