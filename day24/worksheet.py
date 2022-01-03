#!/usr/bin/env python3

inp = [1, 3, 5, 7, 9, 2, 4, 6, 8, 9, 9, 9, 9, 9]
inp = [1, 3, 5, 2, 9, 2, 4, 6, 8, 9, 9, 9, 9, 9]
inp = [1, 3, 5, 2, 9, 2, 5, 6, 8, 9, 9, 9, 9, 9]

inp = [1, 3, 5, 2, 7, 2, 5, 9, 8, 9, 9, 9, 9, 9]
inp = [1, 3, 5, 2, 7, 2, 5, 9, 8, 3, 9, 9, 9, 9]
inp = [1, 1, 5, 2, 7, 2, 5, 9, 8, 3, 9, 8, 8, 9]
inp = [9, 1, 5, 2, 7, 2, 5, 9, 8, 3, 9, 8, 8, 1]

w, x, y, z = 0, 0, 0, 0

step = 0

def print_state(step, w, x, y, z):
    print(f"@{step+1:-2d}  w:{w:-2d}  x:{x:-2d}  y:{y:-2d}  z:{z:-2d}")

# >>> @1
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 11
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 11) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 3
# mul y x
# add z y

y = (w + 3) * x
z = z + (w + 3) * x
print_state(step, w, x, y, z)
step += 1

# >>> @2
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 14
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 14) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

z = z * (25*x + 1)

# mul y 0
# add y w
# add y 7
# mul y x
# add z y

y = (w + 7) * x
z = z + (w + 7) * x
print_state(step, w, x, y, z)
step += 1

# >>> @3
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 13
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 13) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 1
# mul y x
# add z y

y = (w + 1) * x
z = z + (w + 1) * x
print_state(step, w, x, y, z)
step += 1

# >>> @4
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -4
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) - 4) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 6
# mul y x
# add z y

y = (w + 6) * x
z = z + (w + 6) * x
print_state(step, w, x, y, z)
step += 1

# >>> @5
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 11
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 11) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 14
# mul y x
# add z y

y = (w + 14) * x
z = z + (w + 14) * x
print_state(step, w, x, y, z)
step += 1

# >>> @6
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 10
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 10) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 7
# mul y x
# add z y

y = (w + 7) * x
z = z + (w + 7) * x
print_state(step, w, x, y, z)
step += 1

# >>> @7
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -4
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) - 4) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 9
# mul y x
# add z y

y = (w + 9) * x
z = z + (w + 9) * x
print_state(step, w, x, y, z)
step += 1

# >>> @8
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -12
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) - 12) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 9
# mul y x
# add z y

y = (w + 9) * x
z = z + (w + 9) * x
print_state(step, w, x, y, z)
step += 1

# >>> @9
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 10
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 10) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 6
# mul y x
# add z y

y = (w + 6) * x
z = z + (w + 6) * x
print_state(step, w, x, y, z)
step += 1

# >>> @10
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -11
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) - 11) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 4
# mul y x
# add z y

y = (w + 4) * x
z = z + (w + 4) * x
print_state(step, w, x, y, z)
step += 1

# >>> @11
# inp w
# mul x 0
# add x z
# mod x 26
# div z 1
# add x 12
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 12) != w)

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 0
# mul y x
# add z y

y = (w + 0) * x
z = z + (w + 0) * x
print_state(step, w, x, y, z)
step += 1

# >>> @12
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -1
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) - 1) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 7
# mul y x
# add z y

y = (w + 7) * x
z = z + (w + 7) * x
print_state(step, w, x, y, z)
step += 1

# >>> @13
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x 0
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) + 0) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 12
# mul y x
# add z y

y = (w + 12) * x
z = z + (w + 12) * x
print_state(step, w, x, y, z)
step += 1

# >>> @14
# inp w
# mul x 0
# add x z
# mod x 26
# div z 26
# add x -11
# eql x w
# eql x 0

w = inp[step]
x = int(((z % 26) - 11) != w)
z = z // 26

# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y

y = 25*x + 1
z = z * (25*x + 1)

# mul y 0
# add y w
# add y 1
# mul y x
# add z y

y = (w + 1) * x
z = z + (w + 1) * x
print_state(step, w, x, y, z)
step += 1


