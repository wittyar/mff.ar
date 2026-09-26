@echo off
REM TA GUIANAEL MFF desde el repo. La version instalada se abre desde su acceso directo.
REM Hace lo mismo que el acceso directo: abre la app en su ventana, sin consola, con los
REM datos en %LOCALAPPDATA%\TA GUIANAEL MFF (los mismos que usa la app instalada). Lo que
REM pase queda en registro.txt, en esa carpeta.
setlocal
cd /d "%~dp0"

set "PYW="
if exist "python\pythonw.exe" set "PYW=python\pythonw.exe"
if not defined PYW (
  where pyw >nul 2>nul && set "PYW=pyw"
)
if not defined PYW (
  where pythonw >nul 2>nul && set "PYW=pythonw"
)
if not defined PYW (
  echo No se encontro Python.
  echo.
  echo Instala Python desde https://www.python.org/downloads/ o usa la app instalada.
  echo.
  pause
  exit /b 1
)

start "" "%PYW%" desktop\lanzador.py %*
endlocal
