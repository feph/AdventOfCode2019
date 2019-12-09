from get_input import get_aoc_input
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
STOPPED = 0
HALT = 99
WAIT_INPUT = 3
WAIT_OUTPUT = 4
RUNNING = 1
class operation(object):
    def __init__(self, length, modes):
        self.length = length
        self.argc = length-1
        self.argv = [0]*self.argc
        # log.debug("during init self.argv = " + str(self.argv))
        self.modes = modes
        self.bp_change = 0

    def consume(self, codes, ip, bp=0):
        """ take the necessary arguments from the code list. """
        for i in range(self.argc):
            # log.debug(f"setting argv[{i}] = {codes[ip+i+1]}")
            self.argv[i] = codes[ip+i+1]
        self.nextip = ip + self.length
        self.bp = bp
    def access_param(self, pnum, codes):
        log.debug(f'accessing parameter {pnum} in mode {self.modes[pnum]}')
        log.debug(f'DEBUG: self.modes = {self.modes}')
        log.debug(f'DEBUG: self.argv= {self.argv}')
        # log.debug(f'DEBUG: pnum = {pnum}')
        assert (self.modes[pnum] in [0,1,2])
        if self.modes[pnum] == 0: # position mode
            log.debug(f'returning pmode value *{self.argv[pnum]}')
            return codes[self.argv[pnum]]
        else:
            if self.modes[pnum] == 1: # value mode
                log.debug(f'returning vmode value {self.argv[pnum]}')
                return self.argv[pnum]
            else:
                if self.modes[pnum] == 2: # relative mode
                    log.debug(f'returning rmode value {codes[self.bp+self.argv[pnum]]} at *({self.bp}+{self.argv[pnum]})')
                    log.debug(f"{codes[0:5]}")
                    retval = codes[self.bp + self.argv[pnum]]
                    log.debug(f"retval = {retval}")
                    return retval
    def access_dest_param(self, pnum, codes):
        assert (self.modes[pnum] in [0,1,2])
        if self.modes[pnum] == 0: # position mode
            return self.argv[pnum]

        if self.modes[pnum] == 2: # relative mode
            retval = self.bp + self.argv[pnum]
            return retval



class addition(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        log.debug(f'created add obj with modes {self.modes}')
    def execute(self,codes):
        # do the addition
        a = self.access_param(0, codes)
        # log.debug(f'a = {a}')
        b = self.access_param(1, codes)
        # log.debug(f'b = {b}')
        dest = self.access_dest_param(2, codes)
        # log.debug(f'dest = {dest}')
        log.debug(f"*{dest} = {a}+{b} = {a+b}")
        codes[dest] = a + b
        return True

class isequal(operation):
    def __init__(self, modes):
        super().__init__(4, modes)
        log.debug(f'created isequal obj with modes {self.modes}')
    def execute(self, codes):
        # do the mult
        a = self.access_param(0, codes)
        # log.debug(f'a = {a}')
        b = self.access_param(1, codes)
        # log.debug(f'b = {b}')
        dest = self.access_dest_param(2, codes)
        # log.debug(f'dest = {dest}')
        log.debug(f"*{dest} = {a}=={b} = {int(a==b)}")
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
        dest = self.access_dest_param(2, codes)
        if a < b:
            codes[dest] = 1
        else:
            codes[dest] = 0
        return True

class base_adjust(operation):
    def __init__(self, modes):
        super().__init__(2, modes)
    def execute(self,codes):
        d = self.access_param(0, codes)
        self.bp_change = d
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
        # log.debug(f'a = {a}')
        b = self.access_param(1, codes)
        # log.debug(f'b = {b}')
        log.debug("now dest")
        dest = self.access_dest_param(2, codes)
        # log.debug(f'dest = {dest}')
        log.debug(f"*{dest} = {a}*{b} = {a*b}")
        codes[dest] = a * b
        return True

class op_input(operation):
    def __init__(self, modes):
        super().__init__(2, modes)
    def execute(self, codes):
        dest_pointer = self.access_dest_param(0, codes)
        log.debug("self argv = " + repr(self.argv))
        log.debug(f"setting codes[{self.argv[0]}] = {self.input}") 
        codes[dest_pointer] = self.input
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
           9: base_adjust,
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

class intcomputer(object):
    def dump(self):
        for c in self.memory:
            print(f"{c}")

    def __init__(self, code="", input_queue=[], memsize=1024):
        self.state = STOPPED
        self.memsize = memsize
        if len(code) > 0:
            self.load_program(code)
        else:
            self.code = []
        if not isinstance(input_queue, list):
            input_queue = [input_queue]
            # print(f"new input queue: {input_queue}")
        self.input_queue = input_queue
        self.output_queue = []

    def push_input(self, inp):
        self.input_queue.insert(0,inp)

    def load_program(self, s):
        if isinstance(s, str):
            self.code = [int(x) for x in s.strip().split(",")]
        else:
            self.code = s
        self.reset()

    def reset(self):
        self.memory = self.code + [0]*(self.memsize-len(self.code))
        self.ip = 0
        self.bp = 0 # base pointer

    def get_output(self):
        return self.output_queue.pop()

    def run(self):
        if self.state == HALT:
            return False
        self.state = RUNNING
        while self.state == RUNNING:
            c = self.memory[self.ip]
            op = parse_opcode(c)
            op.consume(self.memory, self.ip, self.bp)
            if isinstance(op, op_input):
                log.debug(f"input queue is: {self.input_queue}")
                if len(self.input_queue) > 0:
                    op.input = self.input_queue.pop()
                    log.debug(f"input queue is: {self.input_queue}")
                else:
                    self.state = WAIT_INPUT
                    break
            running = op.execute(self.memory)
            if not running:
                self.state = HALT
                break
            self.ip = op.nextip
            self.bp += op.bp_change
            if op.bp_change != 0:
                log.debug(f"BP changed to {self.bp}!")
            if isinstance(op, op_output):
                # self.state = WAIT_OUTPUT
                log.debug(f"OUTPUT!: {op.output}")
                self.output_queue.insert(0, op.output)
        return self.state




def run_program(codes_inp, prog_input):
    if isinstance(codes_inp, str):
        codes_inp = [int(a.strip()) for a in codes_inp.split(",")]
    output = []
    if not isinstance(prog_input, list):
        prog_input = [prog_input]
    log.debug(f"prog_input = {prog_input}")
    codes = list(codes_inp) # new memory
    log.debug(codes)
    input_counter = 0
    ip = 0
    running = True
    while running:
        c = codes[ip]
        op = parse_opcode(c)
        op.consume(codes, ip)
        log.debug(op)
        if isinstance(op, op_input):
            log.debug(f"prog_input = {prog_input}")
            op.input = prog_input[input_counter]
            log.debug(f"{op.input}")
            input_counter += 1
        log.debug(f"executing operation {op}")
        running = op.execute(codes)
        ip = op.nextip
        if isinstance(op, op_output):
            log.debug(f"appending output {op.output}")
            output.append(op.output)
    return output
