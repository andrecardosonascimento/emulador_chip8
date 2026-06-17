import pygame
from memory import Memory 
from cpu import CPU
from display import Display
from timers import Timers 
from rom_loader import RomLoader 
#chamando classes
memory = Memory()
display = Display()
timers = Timers()
cpu = CPU(memory)

# executando a rom
RomLoader.load(
    memory,
    "roms/pong.ch8"
)

# Loop de execução principal 

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    opcode = cpu.fetch()
    cpu.execute(opcode)
    timers.tick()
    display.draw()
    clock.tick(60)  # 60 FPS

pygame.quit()

