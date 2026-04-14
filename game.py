import pygame
import sys
import random
from collections import deque

#.............SNAKE...............

class Snake:
    def __init__(self):
        self.body = [[100, 50],[90, 50],[80, 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction


    def move(self):
        head = list(self.body[0])

        if self.direction == "RIGHT":
            head[0] += 10
        elif self.direction == "LEFT":
            head[0] -= 10
        elif self.direction == "UP":
            head[1] -= 10
        elif self.direction == "DOWN":
            head[1] += 10

        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(list(tail))

#FOOD

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = self.spawn()

    def spawn(self):
        return [
            random.randrange(1,(self.width//10))* 10,
            random.randrange(1,(self.height//10))* 10
        ]


#GAME
class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH = 600
        self.HEIGHT = 400
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake_Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.WIDTH, self.HEIGHT)

        self.score = 0

        self.game_over_flag = False
        self.font = pygame.font.SysFont("Arial", 30)
        self.ai_mode = True #ai


    def run(self):
        while True:
            self.handle_events()
            if not self.game_over_flag:
                self.update()
            self.draw()
            self.clock.tick(15)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_over_flag:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.ai_mode = not self.ai_mode

            if not self.ai_mode:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.snake.change_to = "LEFT"
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_to = "RIGHT"
                    elif event.key == pygame.K_UP:
                        self.snake.change_to = "UP"
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_to = "DOWN"

    def update(self):
        if self.ai_mode:
            self.ai_move()
        else:
            # Direction logic
            if self.snake.change_to == "RIGHT" and self.snake.direction != "LEFT":
                self.snake.direction = "RIGHT"
            elif self.snake.change_to == "LEFT" and self.snake.direction != "RIGHT":
                self.snake.direction = "LEFT"
            elif self.snake.change_to == "UP" and self.snake.direction != "DOWN":
                self.snake.direction = "UP"
            elif self.snake.change_to == "DOWN" and self.snake.direction != "UP":
                self.snake.direction = "DOWN"



        self.snake.move()

        #Eat Food
        if self.snake.body[0] == self.food.position:
            self.score += 1
            self.snake.grow()
            self.food.position = self.food.spawn()

        #Collision (wall)
        x, y = self.snake.body[0]
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            self.game_over()

        #collison (self)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    def draw(self):
        self.screen.fill((0,0,0))

        #Draw Snake
        for block in self.snake.body:
            pygame.draw.rect(self.screen, (0,255,0), (*block, 10, 10))

        #Draw Food
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food.position, 10, 10))


        #Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10,10))

        if self.game_over_flag:
            game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
            score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))
            quit_text = self.font.render("Press Q to Quit", True, (255, 255, 255))

            self.screen.blit(game_over_text, (180, 100))
            self.screen.blit(score_text, (180, 150))
            self.screen.blit(restart_text, (120, 200))
            self.screen.blit(quit_text, (140, 250))


        pygame.display.update()

    def game_over(self):
        self.game_over_flag = True

    def reset_game(self):
        self.snake = Snake()
        self.food = Food(self.WIDTH, self.HEIGHT)
        self.score = 0
        self.game_over_flag = False

    def ai_move(self):
        head = self.snake.body[0]
        food = self.food.position

        path = self.bfs(head, food, self.snake.body)
        next_cell = None

        if len(path) > 0:
            next_cell = path[0]
        else:
            # Plan B: Look for ANY safe adjacent square if BFS fails
            directions = [(10, 0), (-10, 0), (0, 10), (0, -10)]
            snake_set = set(tuple(block) for block in self.snake.body)

            for dx, dy in directions:
                temp_cell = [head[0] + dx, head[1] + dy]
                # Check walls and body
                if (0 <= temp_cell[0] < self.WIDTH and
                        0 <= temp_cell[1] < self.HEIGHT and
                        tuple(temp_cell) not in snake_set):
                    next_cell = temp_cell
                    break

        if next_cell:
            dx = next_cell[0] - head[0]
            dy = next_cell[1] - head[1]

            if dx == 10:
                self.snake.direction = "RIGHT"
            elif dx == -10:
                self.snake.direction = "LEFT"
            elif dy == 10:
                self.snake.direction = "DOWN"
            elif dy == -10:
                self.snake.direction = "UP"

    def bfs(self, start, goal, snake_body):
        directions = [(10, 0), (-10, 0), (0, 10), (0, -10)]

        queue = deque()
        queue.append((start, []))
        visited = set()

        snake_set = set(tuple(block) for block in snake_body)

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            if tuple(current) in visited:
                continue
            visited.add(tuple(current))

            for dx, dy in directions:
                new_x = current[0] + dx
                new_y = current[1] + dy
                next_cell = [new_x, new_y]

                # wall check
                if new_x < 0 or new_x >= self.WIDTH or new_y < 0 or new_y >= self.HEIGHT:
                    continue

                # snake collision check
                if tuple(next_cell) in snake_set:
                    continue

                queue.append((next_cell, path + [next_cell]))

        return []




#_________________________________RUN GAME___________________

if __name__ == "__main__":
    game = Game()
    game.run()

















