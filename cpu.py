# Nucleo do emulador
class CPU:
    def __init__(self, memory):
        self.memory = memory
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
            case 0x1000:
                self.jump(opcode)
            case 0x6000:
                self.set_registrer(opcode)
            case 0x7000:
                self.add_registrer(opcode)

# executando instrução 6xNN
    def set_registrer(self, opcode):
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        self.V[x] = nn
# executando intrtução 7xNN
    def add_registrer(self, opcode):
        x = (opcode & 0x0f00) >> 8
        nn = opcode & 0x00ff
        self.V[x] += nn
# executando intrtução 7xNN
    def jump(self, opcode):
        address = opcode & 0x0fff
        self.pc = address
        