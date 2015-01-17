//////////////////////////////////////
//
//  Program to find descriminant of a quadratic equation
//


FUNCTION NUMERIC Quad(NUMERIC a, NUMERIC b, NUMERIC c)
  NUMERIC n;
  n = (b*b) - (4*a*c);
  IF (n<0) THEN
    RETURN 0;
  ELSE
    IF (n==0) THEN
      RETURN 1;
    ELSE
      RETURN 2;
    ENDIF
  ENDIF
  RETURN 0;
END

FUNCTION BOOLEAN MAIN()
  NUMERIC d;
  d = Quad(5, 1, 1);
  IF (d==0) THEN
    PRINT "No Roots";
  ELSE
    IF (d==1) THEN
      PRINT "Discriminant is Zero";
    ELSE
      PRINT "Two roots are available";
    ENDIF
  ENDIF
END