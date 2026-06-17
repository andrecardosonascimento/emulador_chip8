class RomLoader:

    @staticmethod
    def load(memory, path):
        with open(path, "rb") as rom:
            data = rom.read()
        
        for i, byte in enumerate(data):
            memory.write(0x200 + i, byte)

        