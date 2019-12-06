from get_input import get_aoc_input

class operation(object):
    def __init__(self, length, modes):
        self.length = length
        self.argc = length-1
        self.argv = [0]*self.argc
        self.modes = modes
    def consume(self, codes, ip):
        """ take the necessary arguments from the code list. """
        for i in range(self.argc):
            self.argv[i] = codes[ip+i+1]
    def access_param(self, pnum, codes):
        print(f'accessing parameter {pnum} in mode {self.modes[pnum]}')
        print(f'DEBUG: self.modes = {self.modes}')
        print(f'DEBUG: pnum = {pnum}')
        assert (self.modes[pnum] in [0,1])
        if self.modes[pnum] == 0: # position mode
            print(f'returning value at addr {self.argv[pnum]}')
            return codes[self.argv[pnum]]
        else:
            if self.modes[pnum] == 1:
                print(f'returning value {self.argv[pnum]}')
                return self.argv[pnum]

class addition(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        print(f'created add obj with modes {self.modes}')
    def execute(self,codes):
        # do the addition
        a = self.access_param(0, codes)
        print(f'a = {a}')
        b = self.access_param(1, codes)
        print(f'b = {b}')
        dest = self.argv[2]
        print(f'dest = {dest}')
        print(f"setting addr {dest} = {a+b}")
        codes[dest] = a + b
        return True


class halt(operation):
    def __init__(self, modes=[]):
        super().__init__(1, modes)
    def execute(self,codes):
        return False

class multiplication(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        print(f'created mult obj with modes {self.modes}')
    def execute(self, codes):
        # do the mult
        a = self.access_param(0, codes)
        print(f'a = {a}')
        b = self.access_param(1, codes)
        print(f'b = {b}')
        dest = self.argv[2]
        print(f'dest = {dest}')
        print(f"setting addr {dest} = {a*b}")
        codes[dest] = a * b
        return True

class op_input(operation):
    def __init__(self, modes):
        super().__init__(2, modes)
    def execute(self, codes):
        codes[self.argv[0]] = self.input
        return True
class op_output(operation):
    def execute(self, codes):
        self.output = self.access_param(0, codes)
        print(f"output value = {self.output}")
        return True
    def __init__(self, modes):
        super().__init__(2, modes)
        print(f'created op_output obj with modes {self.modes}')

def parse_opcode(x):
    x = int(x)
    print(f'parsing opcode {x}')
    opcode_str = f'{x:05}'
    opcode = int(opcode_str[-2:])
    modes = [int(m) for m in list(opcode_str[:-2])[::-1]]
    if opcode == 1: #add
        return addition(modes)
    if opcode == 2: #mul
        return multiplication(modes)
    if opcode == 3: #inp
        return op_input(modes)
    if opcode == 4: #out
        return op_output(modes)
    if opcode == 99: #hlt
        return halt()

    return unknown_opcode()
inp = "3,0,4,0,99"
code = (''.join(inp)).split(',')
codes = list(map(int, code))

def run_program(codes_inp, prog_input):
    output = []
    codes = list(codes_inp) # new memory
    ip = 0
    running = True
    while running:
        c = codes[ip]
        op = parse_opcode(c)
        op.consume(codes, ip)
        if isinstance(op, op_input):
            op.input = prog_input
        running = op.execute(codes)
        ip += op.length
        if isinstance(op, op_output):
            print(f"appending output {op.output}")
            output.append(op.output)
    return output

arg = 123142
print(f'running program {codes} with input {arg}')
out = run_program(codes, arg)
print(f'output = {out}')

inp = "1002,6,3,6,4,6,33"
code = (''.join(inp)).split(',')
codes = list(map(int, code))
print(f'running program {codes} with input {arg}')
out = run_program(codes, arg)
print(f'output = {out}')

inp = "".join(get_aoc_input(5)).strip()
code = (''.join(inp)).split(',')
codes = list(map(int, code))
out = run_program(codes, 1)
print(f'output = {out}')
