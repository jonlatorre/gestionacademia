ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////ACABANCO.BAT////////////////////////////
REM ////////////////////LLAMA A ACABANCO.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT ACABANCO.SRT
COPY FACABANC.DAT FACABANC.RES
DEL FACABANC.DAT
RENAME FACABANC.CLA FACABANC.DAT
EXIT
