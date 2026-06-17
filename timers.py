class Timers:
    def __init__(self):
        self.delay_timer = 0
        self.sound_timer = 0 
    def tick(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1