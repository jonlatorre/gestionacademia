ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////ACAESALE.BAT////////////////////////////
REM ////////////////////LLAMA A ACAESALE.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT ACAESALE.SRT
COPY FACAESAL.DAT FACAESAL.RES
DEL FACAESAL.DAT
RENAME FACAESAL.CLA FACAESAL.DAT
EXIT
