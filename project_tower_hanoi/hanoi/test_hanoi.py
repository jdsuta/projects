def hanoi_tower(n, source, target, auxiliary):
    if n == 1:
        move = f"Move disk 1 from {source} to {target}\n"
        return
    hanoi_tower(n-1, source, auxiliary, target)
    move = f"Move disk {n} from {source} to {target}\n"
    hanoi_tower(n-1, auxiliary, target, source)

n = 3