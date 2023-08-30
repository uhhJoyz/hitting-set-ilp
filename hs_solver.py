import hitting_set_ilp as hilp
import sys

if len(sys.argv) != 3:
    print(sys.argv)
    raise Exception("This script requires two input arguments in the following order: "
                    "\n 1. Input file \n 2. Output file");
else:
    desc = hilp.solve(str(sys.argv[1]))
    print(desc)
    with open(str(sys.argv[2]), 'w') as f:
        f.write(str(desc))
