
from RDParser import RDParser

def main():
    a = "PRINTLINE 7+((2*20)/4);\r\nPRINT 2+4;\r\n"
    p = RDParser(a)
    arr = p.Parse()
    for obj in arr:
        obj.Execute()


if __name__ == "__main__":
    main()
