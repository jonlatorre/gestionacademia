ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////AFAALBRU.BAT////////////////////////////
REM ////////////////////LLAMA A AFAALBRU.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT AFAALBRU.SRT
COPY FFACALBA.SEL FFACALBA.RES
DEL FFACALBA.SEL
RENAME FFACALBA.CLA FFACALBA.SEL
EXIT
