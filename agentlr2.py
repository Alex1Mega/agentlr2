import random
from collections import deque

# Ровер
class Rover:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.energy = 100
        self.explored = set()
        self.trajectory = [(0, 0)]
        self.goal = 30

    # Перцепція
    def perceive(self, env):
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        result = {}

        for name, (dx, dy) in directions.items():
            x = self.x + dx
            y = self.y + dy

            if not env.inside(x, y):
                result[name] = "boundary"
            elif env.grid[x][y] == "#":
                result[name] = "obstacle"
            else:
                result[name] = "free"

        return result

    # Рух
    def move(self, direction, env):
        moves = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        dx, dy = moves[direction]
        x = self.x + dx
        y = self.y + dy

        if not env.inside(x, y) or env.grid[x][y] == "#":
            return False

        self.x = x
        self.y = y
        self.energy -= 1

        self.explored.add((x, y))
        self.trajectory.append((x, y))

        return True

    # Вибір напрямку
    def choose_direction(self, env):
        perception = self.perceive(env)

        directions = []

        for direction in perception:
            if perception[direction] == "free":
                directions.append(direction)

        if not directions:
            return None

        for direction in directions:
            moves = {
                "up": (-1, 0),
                "down": (1, 0),
                "left": (0, -1),
                "right": (0, 1)
            }

            dx, dy = moves[direction]
            position = (self.x + dx, self.y + dy)

            if position not in self.explored:
                return direction

        return random.choice(directions)

    # Перевірка
    def need_return(self):
        return len(self.explored) >= self.goal or self.energy <= 20


# Середовище
class Environment:
    def __init__(self, rows=10, cols=15):
        self.rows = rows
        self.cols = cols
        self.grid = [["." for _ in range(cols)] for _ in range(rows)]

        for _ in range(25):
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)

            if (x, y) != (0, 0):
                self.grid[x][y] = "#"

    def inside(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def show(self, rover):
        for i in range(self.rows):
            row = ""

            for j in range(self.cols):
                if (i, j) == (rover.x, rover.y):
                    row += "R "
                elif (i, j) == (0, 0):
                    row += "B "
                elif (i, j) in rover.explored:
                    row += "* "
                else:
                    row += self.grid[i][j] + " "

            print(row)

#1

MOVES = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

# Сусідні стани
def get_neighbors(state, env):
    x, y = state
    neighbors = []

    for dx, dy in MOVES:
        new_x = x + dx
        new_y = y + dy

        if env.inside(new_x, new_y):
            if env.grid[new_x][new_y] != "#":
                neighbors.append((new_x, new_y))

    return neighbors

def bfs(start, goal, env):

    queue = deque([start])
    previous = {start: None}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, env):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)

    if goal not in previous:
        return None, nodes_explored

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path, nodes_explored

def dfs(start, goal, env):

    stack = [start]
    previous = {start: None}
    nodes_explored = 0

    while stack:
        current = stack.pop()
        nodes_explored += 1
        if current == goal:
            break
        for neighbor in get_neighbors(current, env):
            if neighbor not in previous:
                previous[neighbor] = current
                stack.append(neighbor)

    if goal not in previous:
        return None, nodes_explored

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()
    return path, nodes_explored

def main():
    random.seed(10)
    env = Environment()
    rover = Rover()
    rover.explored.add((0, 0))
    print("Початкова карта:")
    env.show(rover)

    # Дослідження
    while not rover.need_return():
        direction = rover.choose_direction(env)
        if direction is None:
            break
        rover.move(direction, env)

    print("\nРовер завершив дослідження.")
    print("Поточна позиція:", (rover.x, rover.y))
    print("Досліджено клітин:", len(rover.explored))
    print("Енергія:", rover.energy)

    #1

    start = (rover.x, rover.y)
    goal = (0, 0)

    print("#1")
    print("Початковий стан:", start)
    print("Цільовий стан:", goal)
    print("Дії: up, down, left, right")
    print("Обмеження: межі карти та перешкоди")

    #2
    print("#2")

    bfs_path, bfs_nodes = bfs(start, goal, env)
    dfs_path, dfs_nodes = dfs(start, goal, env)

    #3
    print("#3")
    print("\nBFS:")

    if bfs_path:
        print("Шлях:")

        for i, state in enumerate(bfs_path):
            print(f"{i}: {state}")

        print("Довжина:", len(bfs_path) - 1)
        print("Досліджено вузлів:", bfs_nodes)

    else: print("Шлях не знайдено.")


    print("\nDFS:")

    if dfs_path:
        print("Шлях:")

        for i, state in enumerate(dfs_path):
            print(f"{i}: {state}")

        print("Довжина:", len(dfs_path) - 1)
        print("Досліджено вузлів:", dfs_nodes)

    else: print("Шлях не знайдено.")

    #4
    print("#4")
    print("\nПорівняння:")

    print(
        f"BFS: довжина = {len(bfs_path) - 1}, "
        f"вузлів = {bfs_nodes}"
    )

    print(
        f"DFS: довжина = {len(dfs_path) - 1}, "
        f"вузлів = {dfs_nodes}"
    )

    if len(bfs_path) < len(dfs_path):
        print("BFS знайшов коротший шлях.")
    elif len(dfs_path) < len(bfs_path):
        print("DFS знайшов коротший шлях.")
    else:
        print("Шляхи мають однакову довжину.")

    if bfs_nodes < dfs_nodes:
        print("BFS дослідив менше вузлів.")
    elif dfs_nodes < bfs_nodes:
        print("DFS дослідив менше вузлів.")
    else:
        print("Кількість досліджених вузлів однакова.")


    print("\nТраєкторія Ровера:")
    print(rover.trajectory)


if __name__ == "__main__":
    main()