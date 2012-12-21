ECHO OFF
CLS
ECHO **************************************************************
ECHO **** C O M P I L A   P R O G R A M A S   E  N   B A S I C ****
ECHO **************************************************************
BASCOM %1,%1,%1,/E/R/X
ECHO ----------------------------------------------
ECHO --SI SE HAN PRODUCIDO ERRORES PULSE 'CTRL+C'--
ECHO ----------------------------------------------
ECHO   -- SI NO SE HAN PRODUCIDO PULSE UNA TECLA --
ECHO ----------------------------------------------
ECHO ÿÿÿÿÿÿ
PAUSE
CLS
ECHO ***************************************************************
ECHO *** L I N K E D I T O R   D E   M O D U L O S   O B J E T O ***
ECHO ***************************************************************
LINK %1,%1,%1,,
DEL %1.OBJ
DEL %1.LST
DEL %1.MAP
ECHO ÿÿ
DIR %1.*
