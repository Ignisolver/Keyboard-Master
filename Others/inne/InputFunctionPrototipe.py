import pygame

x = 2
# inicjalizacja pygame
pygame.init()

# ustawienia okna
size_x = 1200
size_y = 650
white = (255, 255, 255)
display_surface = pygame.display.set_mode((size_x, size_y))
screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("Miszcz Klawiatury")
icon = pygame.image.load('klawiatura.png')
pygame.display.set_icon(icon)
screen.fill((255, 255, 255))
myfont = pygame.font.SysFont("monospace", 30)
CAPS = 12288
SHIFT = 4097
SHIFT2 = 4098
# NONE = 4096
# CAPS_SHIFT = 12289
# CAPS_SHIFT2 = 12290

font = pygame.font.Font('freesansbold.ttf', 50)
green = (0, 255, 0)
#
napis = ''
letter = ''
text = font.render(napis, True, green)
textRect = text.get_rect()
display_surface.fill(white)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            print(event)
            if event.key == pygame.K_BACKSPACE:
                if len(napis):
                    napis = napis[:-1]
            letter = code2letter.get(event.key, '')
    mode = pygame.key.get_mods()
    if mode in (CAPS, SHIFT, SHIFT2):
        napis += letter.upper()
    else:
        napis += letter
    letter = ''
    text = font.render(napis, True, green)
    textRect = text.get_rect()
    textRect.topleft = (0, 0)
    display_surface.blit(text, textRect)
    # Draws the surface object to the screen.
    pygame.display.update()
    display_surface.fill(white)
    pygame.draw.rect(display_surface, (100, 0, 100), (0, 0, 100, 100))
