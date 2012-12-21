10 '                       PAGEDIST.BAS
20 '                      --------------
30 '   PROGRAMA DISTRIBUCION DE FUNCIONES DE CAJA DE LA AGENCIA
40 '   --------------------------------------------------------
52 '
54 '
56 '
60 ON ERROR GOTO 9100
70 'WIDTH "LPT1:",132:OPEN "LPT1:" FOR OUTPUT AS #9
75 'LPRINT CHR$(27) "C" CHR$(72);:LPRINT CHR$(15)
80 KEY 1,CHR$(14):KEY 7,CHR$(7):KEY 8,CHR$(9):KEY 10,CHR$(10)
82 KEY 2,CHR$(15):KEY 3,CHR$(16):KEY 4,CHR$(17)
90 CERO$=STRING$(15,"0"):T$=STRING$(4,205):B$="    ":F$=STRING$(4,178)
100 '
132 FECHA$=MID$(DATE$,4,3)+LEFT$(DATE$,3)+RIGHT$(DATE$,2)
134 GOSUB 33000
135 OPEN "I",#4,"FAGECLA.DIA"
136 LINE INPUT #4,TODO$
137 CLAVE$=LEFT$(TODO$,4)
138 CLOSE
140 DEFSTR H,C
150 OPTION BASE 1
160 DIM TABRUT$(4),DIAS%(12),TABENT$(30)
174 DATA 31,28,31,30,31,30,31,31,30,31,30,31
176 FOR A%=1 TO 12:READ DIAS%(A%):NEXT A%
178 '
200 DATA " OPERACIONES CON PROVEEDORES "
202 DATA "  OPERACIONES CON CLIENTES   "
215 DATA "      OTRAS OPERACIONES      "
230 DATA "       FIN DE PROGRAMA       "
232 FOR I%=1 TO 4
234    READ TABRUT$(I%)
236 NEXT I%
299 '
300 '******************************
302 '***TRATAMIENTO DEL PROGRAMA***
310 '******************************
320 'Presentamos el Menu del Programa.
330 GOSUB 8000
332 TIT$="- GESTION DE OPERACIONES DE CAJA DE LA AGENCIA -"
334 X%=80-LEN(TIT$):X%=INT(X%/2)
340 COLOR 11:LOCATE 7,X%:PRINT TIT$
350 LOCATE 8,X%:PRINT STRING$(LEN(TIT$),205)
360 FOR I%=10 TO 13
370    LOCATE I%,25:PRINT TABRUT$(I%-9)
380 NEXT I%
390 '
400 GOSUB 8500:COLOR 11
410 LOCATE 22,15:PRINT "Seleccione Opci¢n con las Flechas y Pulsando la Tecla ";
420 COLOR 15:PRINT " ENTER "
430 'COLOR 7,0,0
440 '
450 C.F%=10:C%=25:L.F%=13:N.L%=4
460 GOSUB 50000
470 '
480 ON I.A% GOTO 6000,6010,6020,9000
490 '
500 '
510 '
520 '
5720 '
5722 '
6000 RUN "PAGEOPPR"
6004 '
6010 RUN "PAGEOPCL"
6014 '
6020 RUN "PAGEOPOT"
6024 '
6030 RUN "PAGEPAPR"
8000 '***********************************************
8010 '***  RUTINA PARA SACAR CARATULA EN PANTALLA ***
8020 '***********************************************
8030 '
8040 CLS:COLOR 10:LOCATE 1,1:PRINT CHR$(201)+STRING$(78,205)+CHR$(187)
8050 LOCATE 2,1:PRINT CHR$(186):COLOR 11:LOCATE 2,3:PRINT EMPRESA$ :COLOR 10:LOCATE 2,36:PRINT "Aplicaci¢n : C A J A    ":COLOR 11:LOCATE 2,63:PRINT "FECHA : "FECHA$" ":COLOR 10 : LOCATE 2,80 :PRINT CHR$(186)
8060 LOCATE 3,1:PRINT CHR$(200)+STRING$(78,205)+CHR$(188)
8070 'FOR J%=4 TO 21 :LOCATE J%,1:PRINT CHR$(186):LOCATE J%,80 :PRINT CHR$(186):NEXT
8080 LOCATE 21,1:PRINT CHR$(201)+STRING$(78,205)+CHR$(187)
8090 LOCATE 22,1:PRINT CHR$(186):COLOR 11:LOCATE 22,3:PRINT "Mensajes: ":COLOR 10:LOCATE 22,80:PRINT CHR$(186)
8100 LOCATE 23,1:PRINT CHR$(200)+STRING$(78,205)+CHR$(188);
8110 COLOR 7,0,0:RETURN
8120 '
8250 '
8490 '*************************
8500 '***IMPRESION DE MENSAJES*
8510 '*************************
8515 '
8520 L.L$=""+MEN$+"":LOCATE 22,14:PRINT L.L$;
8525 IF RET%=1 THEN FOR H%=1 TO 1500:NEXT H%:RET%=0
8530 MEN$=SPACE$(66)
8540 RETURN
8550 '
9000 '**********************
9010 '***FIN DEL PROGRAMA***
9020 '**********************
9030 CLOSE
9040 RUN "PAGECAJA"
9050 END
9060 '
9070 '
9080 '
9090 '
9100 '*******************************
9110 '***RUTINA CONTROL DE ERRORES***
9120 '*******************************
9130 IF ERR=24 OR ERR=25 OR ERR=27 THEN GOSUB 8500:MEN$="--COMPRUEBE LA IMPRESORA Y PULSE UNA TECLA---":GOSUB 8500:A$=INPUT$(1):RESUME
9140 IF ERL=30052 AND ERR=53 THEN GOSUB 8500:MEN$="Fichero FACTCALE.DIR inexistente, pulsa una tecla":GOSUB 8500:A$=INPUT$(1):CLOSE:RESUME 9000
9150 IF ERL=30100 AND ERR=53 THEN GOSUB 8500:MEN$="Fichero FACTCALE.DAT inexistente, pulsa una tecla":GOSUB 8500:A$=INPUT$(1):CLOSE:RESUME 9000
9170 ON ERROR GOTO 0
9180 '
33000 '**********************************
33010 '***APERTURA FICHERO DATOS FIJOS***
33020 '**********************************
33030 OPEN "R",#1,"FDATFIJ.DAT",100
33040 FIELD #1,2 AS NRO$,8 AS NDIRE$,30 AS NEMPRESA$,15 AS NNIF$,8 AS NPROG$,37 AS NFILLER$
33050 GET #1,1
33052 NROEM$=NRO$
33060 DIRE$=NDIRE$
33070 EMPRESA$="*** AGENCIA DE VIAJES EIDE ***"
33080 NIF$=NNIF$
33082 PROGRAMA$=NPROG$
33090 CLOSE
33100 '
33110 '
33120 RETURN
33130 '
40000 '
40010 '   +-------------------------------------------+
40020 '   +   SUBRUTINA de CONTROL DE FECHA LOGICA    +
40030 '   +-------------------------------------------+
40040 '   -  Recibe la fecha en formato DDMMAA sobre FECSUB$
40050 '   -  Devuelve sobre FEF$ la fecha en formato DD-MM-AA
40060 '   -  Utiliza ERF como Codigo de Retorno.0=fecha correcta,1=fecha erronea
40070 '-------------------------------------------------------------------------
40080 AA$=RIGHT$(FECSUB$,2):MM$=MID$(FECSUB$,3,2):DD$=LEFT$(FECSUB$,2)
40090 ANOMAX%=VAL(RIGHT$(DATE$,2))
40100 ANO%=VAL(AA$):MES%=VAL(MM$):DIA%=VAL(DD$):ERF%=0
40110 IF  (ANO% < 1  OR ANO% > 99 OR MES% < 1 OR MES% > 12) THEN 40150
40120 IF (ANO% MOD 4)= 0 THEN DIAS%(2)=29 ELSE DIAS%(2)=28
40130 IF (DIA% < 1 OR DIA% > DIAS%(MES%)) THEN 40150
40140 FDMA$=DD$+"-"+MM$+"-"+AA$:FAMD$=AA$+MM$+DD$:ERF%=0:RETURN 'Fecha Correcta
40150 ERF%=1:RETURN  'Fecha Incorrecta
40160 '-------------------------------------------------------------------------
40170 '
45010 'RINT CHR$(27)+"&l0O"+CHR$(27)+"(s10h3B";
50000 '************************
50010 '***RUTINA VIDEO INVERSO*
50020 '************************
50030 '
50035            ' Devuelve la opcion sobre I.A%
50050 R$=CHR$(0):F%=C.F%
50060 WHILE ASC(R$)<>13
50065 F.I%=C.F%-1
50070 FOR I.A%=1 TO N.L%
50080 F.I%=F.I%+1:IF F%=F.I% THEN 50100
50090 NEXT I.A%
50100 'Tengo el valor de I.A%
50110 COLOR 12:LOCATE F%,C%:PRINT TABRUT$(I.A%)
50120 R$=INKEY$:IF R$="" THEN 50120
50121 IF ASC(R$)=13 OR ASC(R$)=30 OR ASC(R$)=31 THEN 50130
50122 IF R$=CHR$(0)+CHR$(80) THEN R$=CHR$(31)
50123 IF R$=CHR$(0)+CHR$(72) THEN R$=CHR$(30)
50124 IF R$="2" THEN R$=CHR$(31)
50125 IF R$="8" THEN R$=CHR$(30)
50130 IF ASC(R$)=13 THEN 50190
50140 IF F%=C.F% AND ASC(R$)<>31 THEN 50120
50145 IF F%=L.F% AND ASC(R$)=31 AND NOMENU%=1 THEN LOCATE F%,C%:PRINT SPC(1):F%=C.F%:GOTO 50050
50150 IF F%=L.F% AND ASC(R$)=31 THEN COLOR 11:LOCATE F%,C%:PRINT TABRUT$(I.A%):F%=C.F%:GOTO 50050
50160 IF NOMENU%=1 THEN LOCATE F%,C%:PRINT SPC(1) ELSE COLOR 11:LOCATE F%,C%:PRINT TABRUT$(I.A%)
50170 IF ASC(R$)=30 THEN F%=F%-1
50180 IF ASC(R$)=31 THEN F%=F%+1
50190 WEND
50200 COLOR 15
50300 RETURN
50340 '
50510 '
60000 '   +-------------------------------------------+
60010 '   +   SUBRUTINA de CONTROL DE FECHA LOGICA    +
60020 '   +-------------------------------------------+
60030 '   -  Recibe la fecha en formato DDMMAA sobre FECSUB$
60040 '   -  Devuelve sobre FEF$ la fecha en formato DD-MM-AA
60050 '   -  Utiliza ERF como Codigo de Retorno.0=fecha correcta,1=fecha erronea
60060 '-------------------------------------------------------------------------
60070 AA$=RIGHT$(FECSUB$,2):MM$=MID$(FECSUB$,3,2):DD$=LEFT$(FECSUB$,2)
60080 ANOMAX%=VAL(RIGHT$(DATE$,2))
60090 ANO%=VAL(AA$):MES%=VAL(MM$):DIA%=VAL(DD$):ERF%=0
60100 IF  (ANO% < 1  OR ANO% > 99 OR MES% < 1 OR MES% > 12) THEN 60140
60110 IF (ANO% MOD 4)= 0 THEN DIAS%(2)=29 ELSE DIAS%(2)=28
60120 IF (DIA% < 1 OR DIA% > DIAS%(MES%)) THEN 60140
60130 FDMA$=DD$+"-"+MM$+"-"+AA$:FAMD$=AA$+MM$+DD$:ERF%=0:RETURN 'Fecha Correcta
60140 ERF%=1:RETURN  'Fecha Incorrecta
60150 '-------------------------------------------------------------------------
60160 '
63000 '********************************
63010 '***RUTINA DE ENTRADA NUMERICA***
63020 '********************************
63030 '
63040 D.E$="":I.T%=0
63050 LOCATE F.C1%,C.C1%,1,0,7
63060 FOR JMG%=1 TO L.E%
63070  D.R$=INPUT$(1)
63080  IF ASC(D.R$)=13 AND JMG%=1 THEN JMG%=L.E%:I.T%=1:GOTO 63200  '===>AL NEXT
63090  IF ASC(D.R$)=13 THEN JMG%=L.E%:GOTO 63200  '===>AL NEXT
63100  IF ASC(D.R$)=10 THEN JMG%=L.E%:I.T%=2:GOTO 63200  '===>AL NEXT
63110  IF ASC(D.R$)=9 THEN JMG%=L.E%:I.T%=3:GOTO 63200   '===>AL NEXT
63120  IF ASC(D.R$)=7 THEN JMG%=L.E%:I.T%=4:GOTO 63200   '===>AL NEXT
63130  IF JMG%=1 THEN LOCATE F.C1%,C.C1%:PRINT STRING$(BO%,"-"):LOCATE F.C1%,C.C1%
63140  IF D.R$<"0" OR D.R$>"9" THEN 63170               'Error
63150  D.E$=D.E$+D.R$:PRINT D.R$;
63160  GOTO 63200 'AL NEXT
63170  'Error.
63175  IF ASC(D.R$)=8 AND JMG%=1 THEN 63190
63180  IF ASC(D.R$)=8 THEN LOCATE F.C1%,C.C1%+LEN(D.E$)-1:PRINT "-":LOCATE F.C1%,C.C1%+LEN(D.E$)-1:D.E$=LEFT$(D.E$,LEN(D.E$)-1):JMG%=JMG%-1
63190  JMG%=JMG%-1
63200 NEXT JMG%
63210 IF I.T%<>0 THEN 63230
63220 IF LEN(D.E$)<>L.E% THEN D.E$=LEFT$(CERO$,L.E%-LEN(D.E$))+D.E$
63225 IF ESC%=1 THEN LOCATE F.C1%,C.C1%:PRINT D.E$
63230 RETURN
63240 '
64000 '*************************************
64010 '***RUTINA DE ENTRADA ALFA/NUMERICA***
64020 '*************************************
64030 '
64040 D.E$="":I.T%=0
64050 LOCATE F.C1%,C.C1%,1,0,7
64060 FOR JMG%=1 TO L.E%
64070  D.R$=INPUT$(1)
64080  IF ASC(D.R$)=13 AND JMG%=1 THEN JMG%=L.E%:I.T%=1:GOTO 64200  '===>AL NEXT
64090  IF ASC(D.R$)=13 THEN JMG%=L.E%:GOTO 64200  '===>AL NEXT
64100  IF ASC(D.R$)=10 THEN JMG%=L.E%:I.T%=2:GOTO 64200  '===>AL NEXT
64110  IF ASC(D.R$)=9 THEN JMG%=L.E%:I.T%=3:GOTO 64200   '===>AL NEXT
64120  IF ASC(D.R$)=7 THEN JMG%=L.E%:I.T%=4:GOTO 64200   '===>AL NEXT
64130  IF JMG%=1 THEN LOCATE F.C1%,C.C1%:PRINT STRING$(BO%," "):LOCATE F.C1%,C.C1%
64135  IF ASC(D.R$)=34 THEN 64170
64140  IF ASC(D.R$)<32 OR ASC(D.R$)>126 THEN 64170               'Error
64150  D.E$=D.E$+D.R$:PRINT D.R$;
64160  GOTO 64200 'AL NEXT
64170  'Error.
64172  IF D.R$="¥" OR D.R$="¤" THEN 64150
64175  IF ASC(D.R$)=8 AND JMG%=1 THEN 64190
64180  IF ASC(D.R$)=8 THEN LOCATE F.C1%,C.C1%+LEN(D.E$)-1:PRINT " ":LOCATE F.C1%,C.C1%+LEN(D.E$)-1:D.E$=LEFT$(D.E$,LEN(D.E$)-1):JMG%=JMG%-1
64190  JMG%=JMG%-1
64200 NEXT JMG%
64210 IF I.T%<>0 THEN 64230
64220 'LOCATE F.C1%,C.C1%:PRINT SPC(L.E%)
64225 'LOCATE F.C1%,C.C1%:PRINT D.E$
64230 RETURN
64240 '
64760 '========================================================================
64762 ' RUTINA PARA EDITAR IMPORTES EN CRISTIANO X.XXX.XXX,XX                 =
64764 '                                                                       =
64766 ' SE ENTRARA A ESTA RUTINA DE LA FORMA  SIGUIENTE:                      =
64768 '                                                                       =
64770 ' GOSUB 64760 MANDANDO EN UN CAMPO LLAMADO GUAPRI#,                     =
64772 '                                                                       =
64773 '             LA CANTIDAD O NUMERO QUE DESEEMOS EDITAR.                 =
64774 '                                                                       =
64775 '             Y EN UN CAMPO LLAMADO N.D% EL NUMERO DE DECIMALES         =
64776 '                                                                       =
64778 ' DEVOLVERA EL CAMPO EDITADO EN GUAPRI$ Y LA LONGITUD EN L.C%           =
64780 '                                                                       =
64782 '========================================================================
64784 '
64786 '
64788 GUAPRI$=STR$(GUAPRI#):L.P%=0:N.D%=0
64790 FOR I%=1 TO 30:TABENT$(I%)="":NEXT I%
64792 SIGNO$=LEFT$(GUAPRI$,1):GUAPRI$=RIGHT$(GUAPRI$,LEN(GUAPRI$)-1)
64794 FOR I%=1 TO LEN(GUAPRI$)
64796   IF MID$(GUAPRI$,I%,1)="." THEN L.P%=I%:I%=LEN(GUAPRI$)
64798 NEXT I%
64800 IF L.P%=0 THEN DEC$="":ENT$=GUAPRI$:GOTO 64812
64802 IF N.D%=0 THEN DEC$="":GOTO 64808
64804 DEC$=","+MID$(GUAPRI$,L.P%+1,N.D%)
64806 IF LEN(DEC$)<>N.D%+1 THEN DEC$=DEC$+LEFT$(CERO$,N.D%+1-LEN(DEC$))
64808 ENT$=LEFT$(GUAPRI$,L.P%-1)
64810 IF LEN(ENT$)=0 THEN GUAPRI$="0":GOTO 64834
64812 X%=31
64814 FOR I%=LEN(ENT$) TO 1 STEP -1
64816   X%=X%-1
64818   IF X%=27 OR X%=23 OR X%=19 OR X%=15 OR X%=12 THEN TABENT$(X%)=".":X%=X%-1
64820   TABENT$(X%)=MID$(ENT$,I%,1)
64822 NEXT I%
64824 GUAPRI$=""
64826 FOR I%=1 TO 30
64828   IF TABENT$(I%)="" THEN 64832
64830   GUAPRI$=GUAPRI$+TABENT$(I%)
64832 NEXT I%
64833 IF SIGNO$=" " THEN GUAPRI$=GUAPRI$+DEC$:L.C%=LEN(GUAPRI$)-1:RETURN
64834 GUAPRI$=GUAPRI$+DEC$+SIGNO$:L.C%=LEN(GUAPRI$)-1
64836 RETURN
64838 '
