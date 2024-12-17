from collections import deque
import random


def replace_edge(adjacency_list, start_vertex, old_edge, new_edge):
    for i in range(start_vertex - 1, start_vertex - 6, -1):
        if i > 0:
            adjacency_list[i] = [new_edge if x == old_edge else x for x in adjacency_list[i]]


def bfs(adjacency_list, parent, level, start):
    level[start] = 0
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for neighbor in adjacency_list[current]:
            if level[neighbor] == -1:  
                level[neighbor] = level[current] + 1
                parent[neighbor] = current
                queue.append(neighbor)


def print_path(parent, destination):
    if parent[destination] == -1:
        return [destination]
    else:
        path = print_path(parent, parent[destination])
        path.append(destination)
        return path


def create_adjacency_list(vertices, ladders, snakes):
    adjacency_list = [[] for _ in range(vertices + 1)]
    for i in range(1, vertices + 1):
        for j in range(i + 1, min(i + 7, vertices + 1)):
            adjacency_list[i].append(j)


    for start, end in ladders.items():
        replace_edge(adjacency_list, start, start, end)
        adjacency_list[start] = []


    for start, end in snakes.items():
        replace_edge(adjacency_list, start, start, end)
        adjacency_list[start] = []

    return adjacency_list



def custom_snakes_and_ladders():
    ladders = {}
    snakes = {}

    choice = input("Do you want to input custom ladders and snakes? (yes/no): ").strip().lower()
    if choice == "yes":
        print("Enter ladders in the format 'start:end' (e.g., 3:24). Type 'done' when finished.")
        while True:
            ladder = input("Enter ladder: ").strip()
            if ladder.lower() == "done":
                break
            try:
                start, end = map(int, ladder.split(":"))
                if 1 <= start < end <= 100:
                    ladders[start] = end
                else:
                    print("Invalid ladder position. Ensure start < end and both are between 1 and 100.")
            except ValueError:
                print("Invalid format. Please use 'start:end'.")

        print("Enter snakes in the format 'start:end' (e.g., 95:18). Type 'done' when finished.")
        while True:
            snake = input("Enter snake: ").strip()
            if snake.lower() == "done":
                break
            try:
                start, end = map(int, snake.split(":"))
                if 1 <= end < start <= 100:
                    snakes[start] = end
                else:
                    print("Invalid snake position. Ensure start > end and both are between 1 and 100.")
            except ValueError:
                print("Invalid format. Please use 'start:end'.")
    else:
        ladders = {3: 24, 14: 42, 30: 86, 37: 57, 50: 96, 66: 74}
        snakes = {95: 18, 77: 45, 60: 28, 34: 10, 20: 2}

    return ladders, snakes

def board(l):
    turn=2
    for i in range(0,100):
        l.insert(i,i+1)
    for j in range(99,-1,-10):
        if (turn%2==0):
            print(l[j],"|",l[j-1],"|",l[j-2],"|",l[j-3],"|",l[j-4],"|",l[j-5],"|",l[j-6],"|",l[j-7],"|",l[j-8],"|",l[j-9])
            print("---------------------------------------------------")
            turn-=1
        else:
            print(l[j-9],"|",l[j-8],"|",l[j-7],"|",l[j-6],"|",l[j-5],"|",l[j-4],"|",l[j-3],"|",l[j-2],"|",l[j-1],"|",l[j])
            print("---------------------------------------------------")
            turn+=1



def play_game():

    l=[]
    board(l)
    vertices = 100
    ladders, snakes = custom_snakes_and_ladders()
    print("\nLADDERS:")
    for start, end in ladders.items():
        print(f"{start} -> {end}")
    print("\nSNAKES:")
    for start, end in snakes.items():
        print(f"{start} -> {end}")
    adjacency_list = create_adjacency_list(vertices, ladders, snakes)
    print("\n")


    player1 = input("Enter Player 1 name in this Game!\n")
    player2 = input("Enter Player 2 name in this Game!\n")
    current_turn = int(input("Enter who wants to start the Game! Enter 1 or Enter 2....\n"))
    print("------!!GAME IS STARTED!!----------")


    positions = {player1: 1, player2: 1}
    dice = [1, 2, 3, 4, 5, 6]


    while positions[player1] < 100 and positions[player2] < 100:
        current_player = player1 if current_turn == 1 else player2
        print(f"Player {current_player} -> Enter 1 to ROLL the dice!: ", end="")
        roll = int(input())
        if roll == 1:
            rolled_value = random.choice(dice)
            print(f"Dice rolled: {rolled_value}")
            current_position = positions[current_player]
            next_position = current_position + rolled_value


            if next_position > 100:
                print(f"Roll exceeds position 100. {current_player} stays at position {current_position}.")
                next_position = current_position

            if next_position in ladders:
                print(f"{next_position} before climb")
                next_position = ladders[next_position]
                print(f"--> {current_player} is at position: {next_position}")
            elif next_position in snakes:
                print(f"{next_position} before fall")
                next_position = snakes[next_position]
                print(f"--> {current_player} is at position: {next_position}")
            else:
                print(f"--> {current_player} is at position: {next_position}")

            positions[current_player] = next_position
            
            parent = [-1] * (vertices + 1)
            level = [-1] * (vertices + 1)
            bfs(adjacency_list, parent, level, positions[current_player])
            shortest_path = print_path(parent, 100)
            print(f"Minimum number of moves required from {current_player}'s position = {level[100]}")
            print(f"Shortest path to finish the game = {' -> '.join(map(str, shortest_path))}")
            print("--------------------------------------------------")

            if positions[current_player] == 100:
                print(f"Congrats {current_player}!! You are the winner!")
                break

        else:
            print("Enter 1 to proceed...")

        current_turn = 1 if current_turn == 2 else 2
play_game()