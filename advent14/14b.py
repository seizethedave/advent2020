import sys
import re
import itertools

class Machine:
    def __init__(self):
        self.memory = {}
        self.mask_x_positions = []
        self.mask_bits = 0

    def set_mask(self, mask):
        self.mask_x_positions = []
        self.mask_bits = 0
        for i, ch in enumerate(reversed(mask)):
            if ch == "X":
                self.mask_x_positions.append(i)
            elif ch == "1":
                self.mask_bits |= 1 << i

    def set_value(self, addr, val):
        for a in self.float_values(addr | self.mask_bits):
            self.memory[a] = val

    def float_values(self, val):
        """
        float pos's = [0, 3, 5] if Xs were in 0,3,5 slots (LSB).
        """
        for seq in itertools.product(['0', '1'], repeat=len(self.mask_x_positions)):
            # seq is a string like '0101'.
            mask = 0
            realmask = 0
            for i, bit in enumerate(int(b) for b in seq):
                mask |= bit << self.mask_x_positions[i]
                realmask |= 1 << self.mask_x_positions[i]
            yield (val & ~realmask) | mask

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