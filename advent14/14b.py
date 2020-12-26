import sys
import re
import itertools

def float_values(val, float_positions):
    """
    float pos's = [0, 3, 6] if Xs were in 0,3,5 slots (LSB).
    """
    for seq in itertools.product(['0', '1'], repeat=len(float_positions)):
        mask = 0
        realmask = 0
        for i, bit in enumerate(int(b) for b in seq):
            mask |= bit << float_positions[i]
            realmask |= 1 << float_positions[i]
        yield (val & ~realmask) | mask

class Machine:
    def __init__(self):
        self.memory = {}
        self.mask_x_positions = []
        self.mask_mask = 0
        self.mask_bits = 0

    def set_mask(self, mask):
        self.mask_x_positions = []
        self.mask_mask = 0
        self.mask_bits = 0
        for i, ch in enumerate(reversed(mask)):
            if ch == "X":
                self.mask_x_positions.append(i)
            else:
                self.mask_mask |= 1 << i
                if ch == "1":
                    self.mask_bits |= 1 << i

    def set_value(self, addr, val):
        for a in float_values(addr | self.mask_bits, self.mask_x_positions):
            self.memory[a] = val

    def sum_values(self):
        return sum(self.memory.values())

machine = Machine()

for line in sys.stdin:
    if line.startswith("mem"):
        addr, val = re.findall(r"mem\[(\d+)\] = (\d+)", line)[0]
        machine.set_value(int(addr), int(val))
    elif line.startswith("mask"):
        mask = line.split()[-1]
        machine.set_mask(mask)

print(machine.sum_values())