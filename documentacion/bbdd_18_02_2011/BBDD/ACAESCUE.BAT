ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////ACAESCUE.BAT////////////////////////////
REM ////////////////////LLAMA A ACAESCUE.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT ACAESCUE.SRT
COPY FACAESCU.DAT FACAESCU.RES
DEL FACAESCU.DAT
RENAME FACAESCU.CLA FACAESCU.DAT
EXIT
