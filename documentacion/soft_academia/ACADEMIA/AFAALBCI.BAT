ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////AFAALBCI.BAT////////////////////////////
REM ////////////////////LLAMA A AFAALBCI.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT AFAALBCI.SRT
COPY FFACALBA.SEL FFACALBA.RES
DEL FFACALBA.SEL
RENAME FFACALBA.CLA FFACALBA.SEL
EXIT
