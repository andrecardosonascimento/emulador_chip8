import pygame 

# Tela do Emulador
class Display:
    WIDTH = 64
    HEIGHT = 32

    def __init__(self):
        pygame.init()
        self.scale = 15
        
        self.screen = pygame.display.set_mode(
            ( 
                self.WIDTH * self.scale,
                self.HEIGHT * self.scale
             )
        )

        self.pixels = [
            [0] * self.WIDTH
            for _ in range(self.HEIGHT)
        ]

# Limpar tela 
    def clear(self):
        self.pixels = [
            [0] * self.WIDTH
            for _ in range(self.HEIGHT)
        ]
# Mostrar em tela
    def draw(self):
        self.screen.fill((0,0,0))
        for a in range(self.HEIGHT):
            for b in range(self.WIDTH):
                if self.pixels[a][b]:
                    pygame.draw.rect(
                        self.screen,
                        (255,255,255),
                        (
                            b*self.scale,
                            a*self.scale,
                            self.scale,
                            self.scale
                        )
                    )
        pygame.display.flip()

