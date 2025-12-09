import pygame

pygame.init()

pencere = pygame.display.set_mode((300, 300))


canavar = pygame.image.load("monster.png")
kordinat = canavar.get_rect()
kordinat.topleft = (35, 35)

hız = 15
fps = 60
saat = pygame.time.Clock()

durum = True

while durum:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            durum = False

    tuslar = pygame.key.get_pressed()
    if tuslar[pygame.K_UP]:
        kordinat.y -= hız
    if tuslar[pygame.K_DOWN]:
        kordinat.y += hız
    if tuslar[pygame.K_RIGHT]:
        kordinat.x += hız
    if tuslar[pygame.K_LEFT]:
        kordinat.x -= hız

    
    pencere.fill((0, 0, 0))  

    pencere.blit(canavar, kordinat)


    pygame.display.update()


    saat.tick(fps)

pygame.quit()
