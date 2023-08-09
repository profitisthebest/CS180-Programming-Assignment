import numpy as np

# global constants
DMG = 0
HEALING = 1
PROTECTION = 2
MULTIPLIER = 3


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def d_square_logic(h, x):
    return h - x


def h_square_logic(h, x):
    return h + x


def gridTraveler(n, H, x, y, tile_types, tile_values, protect_token, mult_token, memo={}):
    # memoization
    if (x, y, H, protect_token, mult_token) in memo:
        return memo[(x, y, H, protect_token, mult_token)]

    # base cases
    if H < 0:  # if we are dead, return False immediately
        return False
    if n == 0:
        return True
    # if we are at the end of the grid, check if we are dead or alive
    if x == n-1 and y == n-1:
        if tile_types[x][y] == DMG:  # is a dmg square
            if not protect_token:  # we do not have a protection token - then damage is applied
                H = d_square_logic(H, tile_values[x][y])
        return H >= 0  # check if we are still alive

    # modify the health based on the current tile or give a token
    if tile_types[x][y] == DMG:
        H = d_square_logic(H, tile_values[x][y])
    if tile_types[x][y] == HEALING:
        H = h_square_logic(H, tile_values[x][y])
    if tile_types[x][y] == PROTECTION:
        protect_token = True
    if tile_types[x][y] == MULTIPLIER:
        mult_token = True

    # COMPUTE THE PATH RIGHT (only compute this if we are not going out of array bounds)
    right_path_result = False
    if y+1 != n:
        # if we are on a dmg tile and have a protection token, we can choose to use it or not and get the result based off that.
        if tile_types[x][y] == DMG and protect_token:
            right_path_result_use_token = gridTraveler(
                n, H+tile_values[x][y], x, y+1, tile_types, tile_values, False, mult_token, memo)
            right_path_result_no_token = gridTraveler(
                n, H, x, y+1, tile_types, tile_values, True, mult_token, memo)
            right_path_result = right_path_result_use_token or right_path_result_no_token
        # if we are on a healing tile and have a multiplier token, we can choose to use it (double the healing done) or not.
        elif tile_types[x][y] == HEALING and mult_token:
            right_path_result_use_token = gridTraveler(
                n, H+tile_values[x][y], x, y+1, tile_types, tile_values, protect_token, False, memo)  # double the healing done
            right_path_result_no_token = gridTraveler(
                n, H, x, y+1, tile_types, tile_values, protect_token, True, memo)
            right_path_result = right_path_result_use_token or right_path_result_no_token
        else:
            right_path_result = gridTraveler(
                n, H, x, y+1, tile_types, tile_values, protect_token, mult_token, memo)

    # COMPUTE THE PATH DOWN (only compute this if we are not going out of array bounds)
    down_path_result = False
    if x+1 != n:
        if tile_types[x][y] == DMG and protect_token:
            down_path_result_use_token = gridTraveler(
                n, H+tile_values[x][y], x+1, y, tile_types, tile_values, False, mult_token, memo)
            down_path_result_no_token = gridTraveler(
                n, H, x+1, y, tile_types, tile_values, True, mult_token, memo)
            down_path_result = down_path_result_use_token or down_path_result_no_token
        elif tile_types[x][y] == HEALING and mult_token:
            down_path_result_use_token = gridTraveler(
                n, H+tile_values[x][y], x+1, y, tile_types, tile_values, protect_token, False, memo)
            down_path_result_no_token = gridTraveler(
                n, H, x+1, y, tile_types, tile_values, protect_token, True, memo)
            down_path_result = down_path_result_use_token or down_path_result_no_token
        else:
            down_path_result = gridTraveler(
                n, H, x+1, y, tile_types, tile_values, protect_token, mult_token, memo)

    memo[(x, y, H, protect_token, mult_token)
         ] = right_path_result or down_path_result
    return right_path_result or down_path_result


def DP(n, H, tile_types, tile_values):
    return gridTraveler(n, H, 0, 0, tile_types, tile_values, False, False)


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
