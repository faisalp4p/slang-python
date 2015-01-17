
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
    p = pars.DoParse()
    if not p:
    	raise Exception("parse process failed")

    run_cntxt = RUNTIME_CONTEXT(p)
    fp = p.Execute(run_cntxt, None)


if __name__ == "__main__":
    main()
