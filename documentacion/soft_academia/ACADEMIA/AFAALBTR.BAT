ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////AFAALBTR.BAT////////////////////////////
REM ////////////////////LLAMA A AFAALBTR.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT AFAALBTR.SRT
COPY FFACALBA.SEL FFACALBA.RES
DEL FFACALBA.SEL
RENAME FFACALBA.CLA FFACALBA.SEL
EXIT
