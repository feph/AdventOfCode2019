from get_input import get_aoc_input
from intcomputer import *
import itertools
import logging
log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# inp = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
# inp = "3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0"
# inp = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
inp = "".join(get_aoc_input(7))
# print(inp)

phase_setting = range(5)
all_phase_settings = itertools.permutations(phase_setting)
outputs = {}
for ps in all_phase_settings:
    input_signal = 0
    for p in ps:
        # print(f"p = {p}")
        log.debug("running program with input = {input_signal}")
        output = run_program(inp, [p, input_signal])[0]
        # print(f"(input {p} -> output {output}")
        input_signal = output
        # break

    log.debug(f"phase setting {ps} -> {output}.")
    outputs[ps] = output

max_output_setting = max(outputs, key=lambda key: outputs[key])
max_output = outputs[max_output_setting]

print(f"max. output = {max_output} for setting {max_output_setting}.")

