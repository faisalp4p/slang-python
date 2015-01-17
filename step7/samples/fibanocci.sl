///////////////////////////////////////
//
//  Program to print fibanocci series by iterative method
//

FUNCTION BOOLEAN MAIN()
  NUMERIC newterm;
  NUMERIC prevterm;
  NUMERIC currterm;

  currterm = 1;
  prevterm = 0;

  newterm = currterm + prevterm;

  PRINTLINE newterm;

  WHILE (newterm < 1000)
    prevterm = currterm;
    currterm = newterm;
    newterm = currterm + prevterm;
    PRINTLINE newterm;
  WEND
 END