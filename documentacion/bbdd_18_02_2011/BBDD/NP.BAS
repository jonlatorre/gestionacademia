900       '*******************************
902       '***ENTRADA NUMERO PROVEEDOR ***
904       '*******************************
906       COLOR 15
908       F.C1%=6:C.C1%=14:L.E%=5:BO%=6:ESC%=1:GOSUB 63000
910       IF I.T%=0 THEN CUENTA$=D.E$:GOTO 928 'Entrada OK
912       IF I.T%=5 THEN 908
914       IF I.T%=1 AND I.A%=1 THEN 908
916       IF I.T%=1 THEN 902
918       IF I.T%=3 THEN 902                 'Retroceder Campo.
920       IF I.T%=4 THEN 4000               'Fin Entrada.
922       IF I.T%=2 AND I.A%=1 THEN 928
924       IF I.T%=2 THEN 902
926       '
928       '
930       GUAPRI#=VAL(CUENTA$):GOSUB 64770:LOCATE 6,19-L.C%:PRINT GUAPRI$:BUSCA$=CUENTA$
932       N.L%=VAL(CUENTA$)
934       IF N.L%<2 OR N.L%>ULTIMO% THEN GOSUB 8500:MEN$="Este N£mero de Proveedor no existe, pulsar una tecla":GOSUB 8500:A$=INPUT$(1):LOCATE 6,14:PRINT SPC(6):GOTO 2550
936       GET #1,N.L%
938       IF I.A%<>4 AND PMARC="L" THEN GOSUB 8500:MEN$="Proveedor dado de BAJA, pulsar una tecla":GOSUB 8500:A$=INPUT$(1):LOCATE 6,14:PRINT SPC(6):GOTO 2550
