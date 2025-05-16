import pygame
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders - Menu")
FONT = pygame.font.SysFont("arial", 28)
SMALL_FONT = pygame.font.SysFont("arial", 22)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 180, 255)        #آبی
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 128, 0), (255, 165, 0)]

# States
menu_state = "main"  # "main" | "form"
input_boxes = []
players = []
num_players = 2
selected_color = [0, 1, 2, 3]  # default colors

# Input box
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)   #kadre mostatilio mkshe
        self.base_color = GRAY
        self.active_color = (0, 120, 255)    # abi
        self.color = self.base_color
        self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.active_color
            else:
                self.active = False
                self.color = self.base_color
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.base_color
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 12:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+1))

# Draw button
def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = FONT.render(text, True, BLACK)
    screen.blit(label, (x + 15, y + 10))
    return rect

# Main menu screen
def draw_main_menu():
    screen.fill(WHITE)
    title = FONT.render(" Snakes and Ladders", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
    return draw_button("Start Game", WIDTH//2 - 100, 300, 200, 60)

# Player form screen
def draw_player_form():
    global input_boxes, selected_color
    screen.fill(WHITE)

    # Number of players
    label = FONT.render("Number of players:", True, BLACK)
    screen.blit(label, (50, 30))
    for i in range(2, 5):
        btn = draw_button(str(i), 250 + (i-2)*60, 25, 45, 55)
        if num_players == i:
            pygame.draw.rect(screen, BLACK, btn, 3)

    # Player input
    for i in range(num_players):
        name_label = SMALL_FONT.render(f"Player {i+1} name:", True, BLACK)
        screen.blit(name_label, (30, 100 + i * 100))
        input_boxes[i].draw(screen)

        color_label = SMALL_FONT.render("Color:", True, BLACK)
        screen.blit(color_label, (300, 100 + i * 100))
        for j, color in enumerate(PLAYER_COLORS):
            color_rect = pygame.Rect(360 + j * 50, 100 + i * 100, 30, 30)
            pygame.draw.rect(screen, color, color_rect)
            if selected_color[i] == j:
                pygame.draw.rect(screen, BLACK, color_rect, 3)

    return draw_button("Start Game", WIDTH//2 - 100, 500, 200, 50)

# Game loop
def main():
    global menu_state, input_boxes, num_players, selected_color
    clock = pygame.time.Clock()

    input_boxes = [InputBox(160, 100 + i * 100, 120, 35) for i in range(4)]

    while True:
        screen.fill(WHITE)

        if menu_state == "main":
            start_btn = draw_main_menu()
        elif menu_state == "form":
            start_game_btn = draw_player_form()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if menu_state == "main":
                if event.type == pygame.MOUSEBUTTONDOWN and start_btn.collidepoint(event.pos):
                    menu_state = "form"

            elif menu_state == "form":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(2, 5):
                        btn = pygame.Rect(220 + (i-2)*60, 25, 50, 40)
                        if btn.collidepoint(event.pos):
                            num_players = i
                            input_boxes = [InputBox(160, 100 + i * 100, 120, 35) for i in range(num_players)]
                            selected_color = [i % 4 for i in range(num_players)]

                    for i in range(num_players):
                        for j in range(4):
                            color_rect = pygame.Rect(360 + j * 50, 100 + i * 100, 30, 30)
                            if color_rect.collidepoint(event.pos):
                                selected_color[i] = j

                    if start_game_btn.collidepoint(event.pos):
                        players = []
                        for i in range(num_players):
                            name = input_boxes[i].text.strip() or f"Player {i+1}"
                            color = PLAYER_COLORS[selected_color[i]]
                            players.append((name, color))
                        print("🎉 Players:")
                        for p in players:
                            print(f"{p[0]} - Color: {p[1]}")
                        pygame.quit()
                        sys.exit()  # To be replaced with game screen later

                for box in input_boxes:
                    box.handle_event(event)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
