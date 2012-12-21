ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////RESBANCO.BAT////////////////////////////
REM ////////////////////LLAMA A RESBANCO.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT RESBANCO.SRT
COPY FRESBANC.DAT FRESBANC.RES
DEL FRESBANC.DAT
RENAME FRESBANC.CLA FRESBANC.DAT
EXIT
