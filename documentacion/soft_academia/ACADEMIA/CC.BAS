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
