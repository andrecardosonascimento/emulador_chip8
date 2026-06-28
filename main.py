import sys
from pathlib import Path

import pygame

from cpu import CPU
from display import Display
from memory import Memory
from rom_loader import RomLoader
from timers import Timers


def get_resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path


def main() -> None:
    memory = Memory()
    display = Display()
    timers = Timers()
    cpu = CPU(memory, display)

    rom_path = get_resource_path("roms/pong.ch8")

    try:
        RomLoader.load(memory, str(rom_path))
        print(f"ROM carregada com sucesso em: {rom_path}")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {rom_path}")
        pygame.quit()
        raise SystemExit(1)

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
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()