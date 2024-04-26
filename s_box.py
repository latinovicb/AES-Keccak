def __next_prime(num):
    while True:
        num += 1
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                break
        else:
            return num


def create_s_box(snum):
    p1 = __next_prime(int(str(snum)[-3:]))
    p1 = max(p1, 11)
    p2 = __next_prime(p1)
    q = (int(str(snum)[4:6]) % 32) + 2
    r1 = int(str(snum)[-4:])
    r2 = int(str(snum)[-4:][::-1])

    p1 %= 256
    p2 %= 256
    r1 %= 256
    r2 %= 256

    A = [(p1 * x + r1) % 256 for x in range(256)]

    B = [A[i: i + q][::-1] for i in range(0, len(A), q)]

    B = [item for sublist in B for item in sublist]

    C = [i for i in range(256)]
    for i in range(256):
        b_value = B[i]
        C[(p2 * i + r2) % 256] = b_value

    with open("my_table", "w") as file:
        for number in C:
            file.write(str(number) + "\n")

    return C
