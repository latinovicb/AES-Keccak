from s_box import create_s_box

# ***************************************Helper-functions***************************************


def bytes_to_integers(byte_data):
    integer_list = []

    for byte in byte_data:
        integer_value = int(byte)
        integer_list.append(min(max(integer_value, 0), 255))

    return integer_list


def insert_first_block_to_S(S, block_integers):
    # flatten the first two rows
    flattened_s = [elem for row in S[:2] for elem in row]

    # insert integers
    flattened_s[: len(block_integers)] = block_integers

    # update S
    S[:2] = [flattened_s[i: i + 5] for i in range(0, len(flattened_s), 5)]

    return S


def rotate_left(matrix, row_index, steps):
    row_to_shift = matrix[row_index]

    # calculate index
    split_index = steps % len(row_to_shift)

    # shift the row to the left
    shifted_row = row_to_shift[split_index:] + row_to_shift[:split_index]

    matrix[row_index] = shifted_row
    return matrix


def populate_matrix_from_digits(input_number):
    digits = [int(digit) for digit in str(input_number)]

    # init 5x5 matrix with zeros
    matrix = [[0] * 5 for _ in range(5)]

    # populate the matrix row-wise with digits
    digit_index = 0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = digits[digit_index % len(digits)]
            digit_index += 1

    return matrix


def multiply_matrices(first_matrix, second_matrix):
    # checks if the matrices can be multiplied
    if len(first_matrix[0]) != len(second_matrix):
        raise ValueError(
            "Number of columns in the first matrix must be equal to the number of rows in the second matrix"
        )

    # init the result matrix with zeros
    result_matrix = [[0] * len(second_matrix[0])
                     for _ in range(len(first_matrix))]

    for i in range(len(first_matrix)):
        for j in range(len(second_matrix[0])):
            for k in range(len(second_matrix)):
                # resulted matrix
                result_matrix[i][j] += first_matrix[i][k] * second_matrix[k][j]

    return result_matrix


def modulo_256_matrix(matrix):
    result_matrix = [[element % 256 for element in row] for row in matrix]
    return result_matrix


# ***************************************3-step_permutation***************************************
def sub_bytes(matrix, s_box):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = s_box[matrix[i][j]]
    return matrix


def shift_rows(state, student_number):
    # extract the digits from the end of the student number

    for i in range(1, 5):
        steps = int(str(student_number)[-i]) % 5
        if steps == 0:
            steps = 1

        state = rotate_left(state, i, steps)

    return state


def mix_columns(state, snum):
    own_matrix = populate_matrix_from_digits(snum)

    state = modulo_256_matrix(multiply_matrices(own_matrix, state))
    return state


def permutation(S, C, snum):
    round = 0
    # 3-way permutation, 6 rounds
    for i in range(6):
        round += 1
        S = sub_bytes(S, C)

        S = shift_rows(S, snum)

        S = mix_columns(S, snum)
    return S


# ***************************************Main***************************************
def main(file_name, C, snum, block_size, outQ):
    S = [[0 for j in range(5)] for i in range(5)]

    block_num = 0
    with open(file_name, "rb") as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            # -------------- block_ops

            int_bytes = bytes_to_integers(block)
            if len(int_bytes) != block_size:
                int_bytes[-1] = 0  # remove end file byte
                while len(int_bytes) != 10:
                    int_bytes.append(0)

            # --------------
            if block_num == 0:  # for the following blocks
                S = insert_first_block_to_S(
                    S, int_bytes[:10]
                )  # needs to fit in first two rows
            else:  # absorbation
                for i in range(10):
                    if i < 5:
                        S[0][i - 5] = (S[0][i - 5] + int_bytes[i]) % 256
                    else:
                        S[1][i - 5] = (S[1][i - 5] + int_bytes[i]) % 256

            S = permutation(S, C, snum)
            block_num += 1

    out = []
    for i in range(block_num):  # extraction
        out += S[0] + S[1]
        S = permutation(S, C, snum)

    print("Output: ", (bytearray(out[:outQ]).hex()))


block_size = 10

snum = input("Your snumber: ")
file_name = input("File name: ")
output_bytes = int(input("Number of output_bytes: "))
s_box_table = create_s_box(snum)
print("Your table: ", s_box_table)

main(file_name, s_box_table, snum, block_size, output_bytes)
