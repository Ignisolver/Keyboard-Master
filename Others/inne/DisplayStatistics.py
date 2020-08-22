import pygame

# inicjalizacja pygame
pygame.init()

# ustawienia okna
size_x = 1200
size_y = 650
screen = pygame.display.set_mode((size_x, size_y))
pygame.display.set_caption("Miszcz Klawiatury")
icon = pygame.image.load('klawiatura.png')
pygame.display.set_icon(icon)
screen.fill((255, 255, 255))

running = True
amount_of_scores = 10

# ustawienia pola rysowania
x0 = int(size_x / 12)
y0 = int(size_y / 6.5) + 22
x_max = int(size_x / 1.33)
y_max = int(size_y / 1.18)
x_length = x_max - x0
y_length = abs(y0 - y_max)
unit_q = 2
unit = x_length / (unit_q * amount_of_scores)
pole_width = unit
tab = [pygame.Rect(x0 + i * unit_q * int(unit), y_max, int(pole_width), 2) for i in range(amount_of_scores)]

# dane
scores = [10, 55, 99, 32, 11, 43, 77, 0, 66, 100]
scores_high = [y_max - y_length * i / 100 for i in scores]

# pomocnicze prostokąty
# pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((x0, y0, 10, 10)))
#
# pygame.draw.rect(screen, (200, 0, 0), pygame.Rect((x0, y_max, 10, 10)))
# pygame.draw.rect(screen, (0, 200, 0), pygame.Rect((x_max, y0, 10, 10)))
# pygame.draw.rect(screen, (0, 0, 200), pygame.Rect((x_max, y_max, 10, 10)))

myimage = pygame.image.load("siatka2.png")
imagerect = myimage.get_rect()
print(imagerect)
image_loc = [-5, -22]
screen.blit(myimage, [*image_loc, *imagerect[2:4]])

# pętla rysowania
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(amount_of_scores):
        if tab[i].y >= scores_high[i]:
            pygame.draw.rect(screen, (0, 150, 255), tab[i])
            tab[i].y -= 1
    pygame.display.flip()
