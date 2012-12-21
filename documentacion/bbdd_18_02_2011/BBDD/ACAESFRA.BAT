ECHO OFF
REM ///////////////////////////////////////////////////////////////
REM ///////////////////////ACAESFRA.BAT////////////////////////////
REM ////////////////////LLAMA A ACAESFRA.SRT//////////////////////
REM //////////////////////////////////////////////////////////////
REM
CLS
ECHO *************************************************************
ECHO *****CLASIFICANDO FICHERO DE DATOS. Espere por Favor...******
ECHO *************************************************************
ECHO
REM
PCSORT ACAESFRA.SRT
COPY FACAESFR.DAT FACAESFR.RES
DEL FACAESFR.DAT
RENAME FACAESFR.CLA FACAESFR.DAT
EXIT
