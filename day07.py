from get_input import get_aoc_input
from intcomputer import *
import itertools
import logging
import sys
log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
# log.setLevel(logging.DEBUG)

aoc_inp = "".join(get_aoc_input(7))
def part1():
    # inp = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    # inp = "3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0"
    # inp = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    inp = aoc_inp
    # print(inp)

    phase_setting = range(5)
    all_phase_settings = itertools.permutations(phase_setting)
    # all_phase_settings = [(4,3,2,1,0)]
    outputs = {}
    c = intcomputer(inp)
    for ps in all_phase_settings:
        input_signal = 0
        for p in ps:
            # print(f"p = {p}")
            # print(f"input_signal = {input_signal}")
            log.debug(f"running program with input = {input_signal}")
            c.push_input(input_signal) # 2nd
            c.push_input(p) # 1st arg
            c.run() # run until HALT/WAIT_OUTPUT/WAIT_INPUT
            # output = run_program(inp, [p, input_signal])[0]
            # print(f"(input {p} -> output {output}")
            output = c.get_output()
            input_signal = output
            c.reset()
            # break

        log.debug(f"phase setting {ps} -> {output}.")
        outputs[ps] = output

    max_output_setting = max(outputs, key=lambda key: outputs[key])
    max_output = outputs[max_output_setting]

    print(f"max. output = {max_output} for setting {max_output_setting}.")

### part 2
# input_phases = [9,8,7,6,5]
# code = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
# input_phases = [9,7,8,5,6]
# code = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

code = aoc_inp

phase_setting = range(5,10)
all_phase_settings = itertools.permutations(phase_setting)
outputs = {}
for ps in all_phase_settings:

    amps = [intcomputer(code, phase) for phase in ps]

    next_input = 0
    loop_counter = 0
    end_states = [None]*len(amps)
    while not all([a.state == HALT for a in amps]):
        # print(f"loop_counter = {loop_counter}")
        loop_counter += 1
        for i,a in enumerate(amps):
            a.push_input(next_input)
            # print(f"state of amp {i}: {a.state} / ip: {a.ip} / input_queue: {a.input_queue} / output_queue: {a.output_queue}")
            a.run()
            # print(f"state of amp {i}: {a.state} / ip: {a.ip} / input_queue: {a.input_queue} / output_queue: {a.output_queue}")
            # print(f"memory: {amps[i].memory}")
            output = a.get_output()
            if a.state == HALT:
                end_states[i] = output
            next_input = output
            # else:
            #     total_output = next_input
            #     print(f"a{i} is in HALT output queue: {a.output_queue}")
            #     next_input = None

    # print(f"{end_states[-1]}")
    outputs[ps] = end_states[-1] 

max_output_setting = max(outputs, key=lambda key: outputs[key])
max_output = outputs[max_output_setting]

print(f"part 2: max. output = {max_output} for setting {max_output_setting}.")


