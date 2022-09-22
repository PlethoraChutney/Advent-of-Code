from collections import defaultdict

with open('input.txt', 'r') as f:
    instruction_list = [x.rstrip() for x in f]

class Processor(object):
    def __init__(self, proc_id, instruction_list) -> None:
        self.instructions = instruction_list
        self.registers = defaultdict(lambda: 0)
        self.proc_id = proc_id
        self.registers['p'] = proc_id
        self.signal_queue = []
        self.instruction_pointer = 0
        self.send_count = 0

    def queue_put(self, value):
        self.signal_queue.append(value)

    def connect_to_processor(self, processor):
        self.partner_processor = processor

    def convert_to_value(self, value):
        try:
            return int(value)
        except ValueError:
            return self.registers[value]
    
    def set_reg(self, reg, value):
        self.registers[reg] = value

    def add_reg(self, reg, value):
        self.registers[reg] += value
    
    def mul_reg(self, reg, value):
        self.registers[reg] = self.registers[reg] * value

    def mod_reg(self, reg, value):
        self.registers[reg] = self.registers[reg] % value

    def jump(self, value, offset):
        if value > 0:
            self.instruction_pointer += offset
        else:
            self.instruction_pointer += 1

    def send(self, value):
        self.partner_processor.queue_put(value)
        self.send_count += 1

    def receive(self, reg):
        if len(self.signal_queue) == 0:
            return False
        else:
            value = self.signal_queue.pop(0)
            self.registers[reg] = value
            return True

    def process_instruction(self):
        if self.instruction_pointer >= len(self.instructions) or self.instruction_pointer < 0:
            return True

        inst = self.instructions[self.instruction_pointer]
        deadlock = False

        fun = inst[:3]
        params = inst[4:].split()

        if fun == 'snd':
            self.send(self.convert_to_value(params[0]))
            self.instruction_pointer += 1
        elif fun == 'set':
            self.set_reg(params[0], self.convert_to_value(params[1]))
            self.instruction_pointer += 1
        elif fun == 'add':
            self.add_reg(params[0], self.convert_to_value(params[1]))
            self.instruction_pointer += 1
        elif fun == 'mul':
            self.mul_reg(params[0], self.convert_to_value(params[1]))
            self.instruction_pointer += 1
        elif fun == 'mod':
            self.mod_reg(params[0], self.convert_to_value(params[1]))
            self.instruction_pointer += 1
        elif fun == 'rcv':
            if self.receive(params[0]):
                self.instruction_pointer += 1
            else:
                deadlock = True
        elif fun == 'jgz':
            self.jump(self.convert_to_value(params[0]), self.convert_to_value(params[1]))
        else:
            raise ValueError

        return deadlock

proc_0 = Processor(0, instruction_list)
proc_1 = Processor(1, instruction_list)

proc_0.connect_to_processor(proc_1)
proc_1.connect_to_processor(proc_0)

deadlock = False
while not deadlock:
    deadlock_0 = proc_0.process_instruction()
    deadlock_1 = proc_1.process_instruction()

    deadlock = deadlock_0 and deadlock_1

print(proc_1.send_count)