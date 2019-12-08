from get_input import get_aoc_input
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

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
        self.nextip = ip + self.length
    def access_param(self, pnum, codes):
        log.debug(f'accessing parameter {pnum} in mode {self.modes[pnum]}')
        log.debug(f'DEBUG: self.modes = {self.modes}')
        log.debug(f'DEBUG: pnum = {pnum}')
        assert (self.modes[pnum] in [0,1])
        if self.modes[pnum] == 0: # position mode
            log.debug(f'returning value at addr {self.argv[pnum]}')
            return codes[self.argv[pnum]]
        else:
            if self.modes[pnum] == 1:
                log.debug(f'returning value {self.argv[pnum]}')
                return self.argv[pnum]

class addition(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        log.debug(f'created add obj with modes {self.modes}')
    def execute(self,codes):
        # do the addition
        a = self.access_param(0, codes)
        log.debug(f'a = {a}')
        b = self.access_param(1, codes)
        log.debug(f'b = {b}')
        dest = self.argv[2]
        log.debug(f'dest = {dest}')
        log.debug(f"setting addr {dest} = {a+b}")
        codes[dest] = a + b
        return True

class isequal(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        log.debug(f'created isequal obj with modes {self.modes}')
    def execute(self, codes):
        # do the mult
        a = self.access_param(0, codes)
        log.debug(f'a = {a}')
        b = self.access_param(1, codes)
        log.debug(f'b = {b}')
        dest = self.argv[2]
        log.debug(f'dest = {dest}')
        log.debug(f"setting addr {dest} = {int(a==b)}")
        codes[dest] = int(a == b)
        return True

class jump_if_zero(operation):
    def __init__(self, modes):
        super().__init__(3, modes)
        log.debug(f'created jmp if zero obj with modes {self.modes}')
    def execute(self, codes):
        a = self.access_param(0, codes)
        b = self.access_param(1, codes)
        if a == 0:
            log.debug(f"setting next ip = {b}")
            self.nextip = b
        return True

class jump_if_true(operation):
    def __init__(self, modes):
        super().__init__(3, modes)
        log.debug(f'created jmp if true obj with modes {self.modes}')
    def execute(self, codes):
        a = self.access_param(0, codes)
        b = self.access_param(1, codes)
        if a != 0:
            log.debug(f"setting next ip = {b}")
            self.nextip = b
        return True

class less_than(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        log.debug(f'created less than obj with modes {self.modes}')
    def execute(self, codes):
        a = self.access_param(0, codes)
        b = self.access_param(1, codes)
        dest = self.argv[2]
        if a < b:
            codes[dest] = 1
        else:
            codes[dest] = 0
        return True

class halt(operation):
    def __init__(self, modes=[]):
        super().__init__(1, modes)
    def execute(self,codes):
        return False

class multiplication(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        log.debug(f'created mult obj with modes {self.modes}')
    def execute(self, codes):
        # do the mult
        a = self.access_param(0, codes)
        log.debug(f'a = {a}')
        b = self.access_param(1, codes)
        log.debug(f'b = {b}')
        dest = self.argv[2]
        log.debug(f'dest = {dest}')
        log.debug(f"setting addr {dest} = {a*b}")
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
        log.debug(f"output value = {self.output}")
        return True
    def __init__(self, modes):
        super().__init__(2, modes)
        log.debug(f'created op_output obj with modes {self.modes}')

OPCODES = {1: addition,
           2: multiplication,
           3: op_input,
           4: op_output,
           5: jump_if_true,
           6: jump_if_zero,
           7: less_than,
           8: isequal,
           99: halt,
          }
def parse_opcode(x):
    x = int(x)
    log.debug(f'parsing opcode {x}')
    opcode_str = f'{x:05}'
    opcode = int(opcode_str[-2:])
    modes = [int(m) for m in list(opcode_str[:-2])[::-1]]
    return OPCODES[opcode](modes)
    # if opcode == 1: #add
    #     return addition(modes)
    # if opcode == 2: #mul
    #     return multiplication(modes)
    # if opcode == 3: #inp
    #     return op_input(modes)
    # if opcode == 4: #out
    #     return op_output(modes)
    # if opcode == 8: #out
    #     return isequal(modes)
    # if opcode == 99: #hlt
    #     return halt()
def run_program(codes_inp, prog_input):
    if isinstance(codes_inp, str):
        codes_inp = [int(x) for x in codes_inp.strip().split(",")]
    output = []
    if not isinstance(prog_input, list):
        prog_input = [prog_input]
    codes = list(codes_inp) # new memory
    input_counter = 0
    ip = 0
    running = True
    while running:
        c = codes[ip]
        op = parse_opcode(c)
        op.consume(codes, ip)
        if isinstance(op, op_input):
            op.input = prog_input[input_counter]
            input_counter += 1
        running = op.execute(codes)
        ip = op.nextip
        if isinstance(op, op_output):
            log.debug(f"appending output {op.output}")
            output.append(op.output)
    return output
