///////////////////////////////////////////
///
///    Program to find Factorial of first 10 number
//

FUNCTION NUMERIC FACT(NUMERIC d)
  IF (d<=0) THEN
    RETURN 1;
  ELSE
    RETURN d*FACT(d-1);
  ENDIF
END


FUNCTION BOOLEAN MAIN()
  NUMERIC c;
  c = 0;
  WHILE(c<=10)
    PRINTLINE FACT(c);
    c = c + 1;
  WEND
END