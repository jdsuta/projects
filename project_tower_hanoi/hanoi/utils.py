
# Reference: https://www.geeksforgeeks.org/c-program-for-tower-of-hanoi/

# The Tower of Hanoi problem is inherently computationally intensive for larger numbers of disks because it requires 
# 2^𝑛−1 moves to solve, where: 
# 𝑛 is the number of disks. 
# For 50 disks, this results in a massive number of moves (over 10^15), which is impractical to compute and handle in a single request due to resource constraints.


# Possible solutions:
# 1. Allocate more resources
# 
# horizontal scaling (using multiple servers) 
# verticaly scaling (upgrading server resources) 

def hanoi_tower(n, source, target, auxiliary, moves_file, moves_list):
    if n == 1:
        move = f"Move disk 1 from {source} to {target}\n"
        moves_file.write(move)
        moves_list.append(move.strip())
        return
    hanoi_tower(n-1, source, auxiliary, target, moves_file, moves_list)
    move = f"Move disk {n} from {source} to {target}\n"
    moves_file.write(move)
    moves_list.append(move.strip())
    hanoi_tower(n-1, auxiliary, target, source, moves_file, moves_list)

def solve_hanoi_to_file(n, file_path):
    moves_list = []
    with open(file_path, 'w') as moves_file:  # Open the file in write mode to ensure it's empty
        hanoi_tower(n, 'A', 'C', 'B', moves_file, moves_list)
    return moves_list

# # Example usage
# n = 15
# file_path = '/Users/davidsuta/Documents/CS50_WEB/project_tower_hanoi/hanoi/hanoi_moves/hanoi_moves.txt'
# moves = solve_hanoi_to_file(n, file_path)




