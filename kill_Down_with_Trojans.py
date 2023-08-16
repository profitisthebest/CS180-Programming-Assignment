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


def gridTraveler(n, i, j, tile_types, tile_values, protect_token, mult_token, memo):
    key = (i, j, protect_token, mult_token)

    # check memo
    if key in memo:
        return memo[key]
    
    
    # base case
    if i == n-1 and j == n-1:
        if protect_token and tile_types[i][j] == DMG:
            memo[key] = 0
        else:
            memo[key] = tile_values[i][j] if tile_types[i][j] == DMG else 0
        return memo[key]

    # edge
    if i == n-1:
        memo[key] = min_to_next_tile(n, i, j+1, tile_types, tile_values, tile_types[i][j], tile_values[i][j], protect_token, mult_token, memo)
    elif j == n-1:
        memo[key] = min_to_next_tile(n, i+1, j, tile_types, tile_values, tile_types[i][j], tile_values[i][j], protect_token, mult_token, memo)
    else:
        right_move = min_to_next_tile(n, i, j+1, tile_types, tile_values, tile_types[i][j], tile_values[i][j], protect_token, mult_token, memo)
        down_move = min_to_next_tile(n, i+1, j, tile_types, tile_values, tile_types[i][j], tile_values[i][j], protect_token, mult_token, memo)
        memo[key] = min(right_move, down_move)

    return memo[key]


def min_to_next_tile(n, next_i, next_j, tile_types, tile_values, last_tile_type, last_tile_value, protect_token, mult_token, memo):
    if last_tile_type == HEALING:
        last_tile_value *= -1 # make it negative - reduces hp needed because we heal
    
    if (next_i, next_j, protect_token, mult_token) in memo:
        return memo[(next_i, next_j, protect_token, mult_token)]
    
    result = 0
    if mult_token and last_tile_type == HEALING:
        use_token = 2*last_tile_value + gridTraveler(n, next_i, next_j, tile_types, tile_values, protect_token, 0, memo)
        not_use_token = last_tile_value + gridTraveler(n, next_i, next_j, tile_types, tile_values, protect_token, 1, memo)
        result = min(use_token, not_use_token)
    elif protect_token and last_tile_type == DMG:
        use_token = gridTraveler(n, next_i, next_j, tile_types, tile_values, 0, mult_token, memo)  # no damage
        not_use_token = last_tile_value + gridTraveler(n, next_i, next_j, tile_types, tile_values, 1, mult_token, memo)
        result = min(use_token, not_use_token)
    else:
        if last_tile_type == MULTIPLIER:
            result = gridTraveler(n, next_i, next_j, tile_types, tile_values, protect_token, 1, memo)
        elif last_tile_type == PROTECTION:
            result = gridTraveler(n, next_i, next_j, tile_types, tile_values, 1, mult_token, memo)
        else:
            result = last_tile_value + gridTraveler(n, next_i, next_j, tile_types, tile_values, protect_token, mult_token, memo)
    
    memo[(next_i, next_j, protect_token, mult_token)] = result
    return result


def DP(n, H, tile_types, tile_values):
    # initialize memo
    memo = {}

    # get minimum hp needed to reach the last tile
    required_h = gridTraveler(n, 0, 0, tile_types, tile_values, 0, 0, memo)

    return H >= required_h



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
