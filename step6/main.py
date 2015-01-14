
from RDParser import RDParser
from contexts import COMPILATION_CONTEXT, RUNTIME_CONTEXT

import sys

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
    	print ""
        print "Usage: python main.py <sorce code filename>"
        print ""
        return
    f = open(filename, 'r')
    script = f.read()
    pars = RDParser(script)
    com_cntxt = COMPILATION_CONTEXT()
    stmts = pars.Parse(com_cntxt)
    run_cntxt = RUNTIME_CONTEXT()
    for stm in stmts:
    	stm.Execute(run_cntxt)


if __name__ == "__main__":
    main()
