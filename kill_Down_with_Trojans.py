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


# approach: at each tile -> in memo store the min hp required to reach end from curr
def gridTraveler(n, i, j, tile_types, tile_values, protect_token, mult_token, memo):
    # memo key
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

    # out of bounds
    if i >= n or j >= n:
        return float('inf')
    
    # if healing tile, val should subtract
    if tile_types[i][j] == HEALING and tile_values[i][j] > 0:
        tile_values[i][j] *= -1
    
    # CASES: DMG, HEALING, PROTECTION, MULTIPLIER
    res = 0
    if tile_types[i][j] == DMG:
        if protect_token: # have protection token
            use_token_right = gridTraveler(n, i, j+1, tile_types, tile_values, 0, mult_token, memo)
            keep_token_right = gridTraveler(n, i, j+1, tile_types, tile_values, 1, mult_token, memo) + tile_values[i][j] # account for curr dmg
            use_token_down = gridTraveler(n, i+1, j, tile_types, tile_values, 0, mult_token, memo)
            keep_token_down = gridTraveler(n, i+1, j, tile_types, tile_values, 1, mult_token, memo) + tile_values[i][j]

            res = min(use_token_right, keep_token_right, use_token_down, keep_token_down) # take min of all possible moves
        else: # no protection token
            right = gridTraveler(n, i, j+1, tile_types, tile_values, 0, mult_token, memo) + tile_values[i][j]
            down = gridTraveler(n, i+1, j, tile_types, tile_values, 0, mult_token, memo) + tile_values[i][j]
            res = min(right, down)
    elif tile_types[i][j] == HEALING:
        if mult_token: # have multiplier token
            use_token_right = gridTraveler(n, i, j+1, tile_types, tile_values, protect_token, 0, memo) + 2*tile_values[i][j]
            keep_token_right = gridTraveler(n, i, j+1, tile_types, tile_values, protect_token, 1, memo) + tile_values[i][j]
            use_token_down = gridTraveler(n, i+1, j, tile_types, tile_values, protect_token, 0, memo) + 2*tile_values[i][j]
            keep_token_down = gridTraveler(n, i+1, j, tile_types, tile_values, protect_token, 1, memo) + tile_values[i][j]

            res = min(use_token_right, keep_token_right, use_token_down, keep_token_down)
        else: # no multiplier token
            right = gridTraveler(n, i, j+1, tile_types, tile_values, protect_token, 0, memo) + tile_values[i][j]
            down = gridTraveler(n, i+1, j, tile_types, tile_values, protect_token, 0, memo) + tile_values[i][j]
            res = min(right, down)
    elif tile_types[i][j] == PROTECTION:
        right = gridTraveler(n, i, j+1, tile_types, tile_values, 1, mult_token, memo)
        down = gridTraveler(n, i+1, j, tile_types, tile_values, 1, mult_token, memo)
        res = min(right, down)
    else: # MULT
        right = gridTraveler(n, i, j+1, tile_types, tile_values, protect_token, 1, memo)
        down = gridTraveler(n, i+1, j, tile_types, tile_values, protect_token, 1, memo)
        res = min(right, down)
    
    memo[key] = max(res, 0)
    return memo[key]


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