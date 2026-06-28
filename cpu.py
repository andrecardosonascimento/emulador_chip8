# Nucleo do emulador
class CPU:
    def __init__(self, memory, display=None):
        self.memory = memory
        self.display = display
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
    
    def fetch(self):
        high = self.memory.read(self.pc)
        low = self.memory.read(self.pc + 1)
        opcode = (high << 8) | low 
        self.pc += 2
        return opcode
        
# decodificador de instruções
    def execute(self, opcode):
        match opcode & 0xf000:
            case 0x0000:
                if opcode == 0x00E0:
                    self.clear_screen(opcode)
                elif opcode == 0x00EE:
                    self.ret(opcode)
            case 0x1000:
                self.jump(opcode)
            case 0x2000:
                self.call(opcode)
            case 0x3000:
                self.skip_eq(opcode)
            case 0x4000:
                self.skip_ne(opcode)
            case 0x5000:
                self.skip_eq_xy(opcode)
            case 0x6000:
                self.set_registrer(opcode)
            case 0x7000:
                self.add_registrer(opcode)
            case 0x8000:
                self.execute_8xy(opcode)
            case 0x9000:
                self.skip_ne_xy(opcode)
            case 0xA000:
                self.set_index(opcode)
            case 0xB000:
                self.jump_offset(opcode)
            case 0xC000:
                self.rand(opcode)
            case 0xD000:
                self.draw(opcode)
            case 0xE000:
                self.execute_ex(opcode)
            case 0xF000:
                self.execute_fx(opcode)

# Instruções implementadas

# 00E0 - CLS (Clear Screen)
    def clear_screen(self, opcode):
        if self.display:
            self.display.clear()

# 00EE - RET (Return from subroutine)
    def ret(self, opcode):
        if self.stack:
            self.pc = self.stack.pop()

# 1NNN - JP (Jump to address)
    def jump(self, opcode):
        address = opcode & 0x0fff
        self.pc = address

# 6XNN - LD Vx, byte (Set register Vx to NN)
    def set_registrer(self, opcode):
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        self.V[x] = nn

# 7XNN - ADD Vx, byte (Add NN to Vx)
    def add_registrer(self, opcode):
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        self.V[x] = (self.V[x] + nn) & 0xFF

# DXYN - DRW (Draw sprite)
    def draw(self, opcode):
        if not self.display:
            return
        
        x = (opcode & 0x0f00) >> 8
        y = (opcode & 0x00f0) >> 4
        height = opcode & 0x000f
        
        vx = self.V[x] % self.display.WIDTH
        vy = self.V[y] % self.display.HEIGHT
        
        self.V[0xF] = 0
        
        for row in range(height):
            sprite_byte = self.memory.read(self.I + row)
            for col in range(8):
                if sprite_byte & (0x80 >> col):
                    screen_x = (vx + col) % self.display.WIDTH
                    screen_y = (vy + row) % self.display.HEIGHT
                    
                    if self.display.pixels[screen_y][screen_x]:
                        self.V[0xF] = 1
                    
                    self.display.pixels[screen_y][screen_x] ^= 1

# 2NNN - CALL (Call subroutine)
    def call(self, opcode):
        address = opcode & 0x0fff
        self.stack.append(self.pc)
        self.pc = address

# 3XNN - SE (Skip if Vx == NN)
    def skip_eq(self, opcode):
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        if self.V[x] == nn:
            self.pc += 2

# 4XNN - SNE (Skip if Vx != NN)
    def skip_ne(self, opcode):
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        if self.V[x] != nn:
            self.pc += 2

# 5XY0 - SE (Skip if Vx == Vy)
    def skip_eq_xy(self, opcode):
        x = (opcode & 0x0f00) >> 8
        y = (opcode & 0x00f0) >> 4
        if self.V[x] == self.V[y]:
            self.pc += 2

# ANNN - LD I (Set I to NNN)
    def set_index(self, opcode):
        self.I = opcode & 0x0fff

# 8XY0-8XYE - Arithmetic/Logic operations
    def execute_8xy(self, opcode):
        x = (opcode & 0x0f00) >> 8
        y = (opcode & 0x00f0) >> 4
        n = opcode & 0x000f
        
        match n:
            case 0x0:  # 8XY0 - LD Vx, Vy
                self.V[x] = self.V[y]
            case 0x4:  # 8XY4 - ADD Vx, Vy
                result = self.V[x] + self.V[y]
                self.V[0xF] = 1 if result > 255 else 0
                self.V[x] = result & 0xFF
            case 0x1:  # 8XY1 - OR Vx, Vy
                self.V[x] |= self.V[y]
            case 0x2:  # 8XY2 - AND Vx, Vy
                self.V[x] &= self.V[y]
            case 0x3:  # 8XY3 - XOR Vx, Vy
                self.V[x] ^= self.V[y]
            case 0x5:  # 8XY5 - SUB Vx, Vy
                self.V[0xF] = 1 if self.V[x] >= self.V[y] else 0
                self.V[x] = (self.V[x] - self.V[y]) & 0xFF
            case 0x7:  # 8XY7 - SUBN Vx, Vy
                self.V[0xF] = 1 if self.V[y] >= self.V[x] else 0
                self.V[x] = (self.V[y] - self.V[x]) & 0xFF

# FX** - Special operations
    def execute_fx(self, opcode):
        x = (opcode & 0x0f00) >> 8
        n = opcode & 0x00ff
        
        match n:
            case 0x07:  # FX07 - LD Vx, DT (Set Vx to delay timer)
                self.V[x] = 0  # Placeholder
            case 0x15:  # FX15 - LD DT, Vx (Set delay timer to Vx)
                pass  # Placeholder

# 9XY0 - SNE (Skip if Vx != Vy)
    def skip_ne_xy(self, opcode):
        x = (opcode & 0x0f00) >> 8
        y = (opcode & 0x00f0) >> 4
        if self.V[x] != self.V[y]:
            self.pc += 2

# BNNN - JP (Jump to NNN + V0)
    def jump_offset(self, opcode):
        address = opcode & 0x0fff
        self.pc = address + self.V[0]

# CXNN - RND (Set Vx to random number & NN)
    def rand(self, opcode):
        import random
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        self.V[x] = random.randint(0, 255) & nn

# EX9E and EXA1 - Keyboard operations (placeholder)
    def execute_ex(self, opcode):
        x = (opcode & 0x0f00) >> 8
        n = opcode & 0x00ff
        
        match n:
            case 0x9E:  # EX9E - SKP (Skip if key Vx is pressed)
                pass  # Placeholder
            case 0xA1:  # EXA1 - SKNP (Skip if key Vx is not pressed)
                pass  # Placeholder