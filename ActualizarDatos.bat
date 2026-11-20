@echo off
REM Actualiza los datos publicados desde esta PC (scripts\actualizar_datos.py): baja las fuentes, corre el build,
REM commitea "Datos actualizados AAAA-MM-DD" en main y lo empuja. Reemplaza al workflow "Actualizar datos MFF".
REM Lo que muestra queda tambien en work\actualizar_datos.log. Para el Programador de tareas, ver CLAUDE.md
REM (seccion "Datos"): la tarea corre el script con Python directamente, sin esta ventana.
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo No se encontro Python.
  echo.
  echo Instala Python 3.12 o mas desde https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

%PY% scripts\actualizar_datos.py
set "CODIGO=%ERRORLEVEL%"
echo.
pause
endlocal & exit /b %CODIGO%
