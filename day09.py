from get_input import get_aoc_input


from intcomputer import *
import logging
log = logging.getLogger()
# log.setLevel(logging.DEBUG)

inp = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
# inp = "1102,34915192,34915192,7,4,7,99,0"
 # inp = "104,1125899906842624,99"
# inp = "1,9,10,3,2,3,11,0,99,30,40,50"
# inp = "1,1,1,4,99,5,6,0,99 "
# inp = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"

inp = "".join(get_aoc_input(9))
c = intcomputer(inp, [1], memsize=4096)

c.run()

print(c.output_queue)
# print(c.memory)
