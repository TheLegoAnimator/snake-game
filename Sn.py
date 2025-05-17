import os
import time
import random
import sys
import threading

try:
    import msvcrt  # Windows-only for instant key press detection
except ImportError:
    import tty, termios  # Unix-based systems

# Game settings
WIDTH, HEIGHT = 30, 20
snake = [[5, 5]]
direction = "RIGHT"
food = [random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2)]
score = 0
paused = False
input_lock = threading.Lock()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def draw_board():
    clear_screen()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if [x, y] in snake:
                print("O", end="")  # Snake body
            elif [x, y] == food:
                print("X", end="")  # Food
            elif x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1:
                print("#", end="")  # Walls
            else:
                print(" ", end="")
        print()
    print(f"Score: {score}")
    print("Controls: W/A/S/D to move | P: Pause | R: Restart | Q: Quit")

def move():
    global food, score
    with input_lock:
        head = snake[-1][:]

        if direction == "UP":
            head[1] -= 1
        elif direction == "DOWN":
            head[1] += 1
        elif direction == "LEFT":
            head[0] -= 1
        elif direction == "RIGHT":
            head[0] += 1

        if head in snake or head[0] == 0 or head[0] == WIDTH - 1 or head[1] == 0 or head[1] == HEIGHT - 1:
            print(f"Game Over! Final Score: {score}")
            sys.exit()

        snake.append(head)
        if head == food:
            score += 1
            food = [random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2)]
        else:
            snake.pop(0)

def get_input():
    global direction, paused, snake, score, food

    while True:
        if os.name == "nt":
            user_input = msvcrt.getch().decode().upper()
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                user_input = sys.stdin.read(1).upper()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        with input_lock:
            if user_input == "W" and direction != "DOWN":
                direction = "UP"
            elif user_input == "S" and direction != "UP":
                direction = "DOWN"
            elif user_input == "A" and direction != "RIGHT":
                direction = "LEFT"
            elif user_input == "D" and direction != "LEFT":
                direction = "RIGHT"
            elif user_input == "P":
                paused = not paused
            elif user_input == "R":
                snake.clear()
                snake.append([5, 5])
                direction = "RIGHT"
                food = [random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2)]
                score = 0
            elif user_input == "Q":
                print("Thanks for playing!")
                sys.exit()

# Start input listener in a separate thread
input_thread = threading.Thread(target=get_input, daemon=True)
input_thread.start()

# Game loop
while True:
    draw_board()
    
    if not paused:
        move()
    
    time.sleep(0.3)  # Adjusted speed for smoother gameplay
