@echo off
REM TA GUIANAEL MFF - lanzador de escritorio.
REM Levanta el servidor local y abre la app en el navegador por defecto.
REM Usa el Python que viaja en la carpeta si existe; si no, el del sistema.
setlocal
cd /d "%~dp0"

set "PYEXE="
if exist "python\python.exe" set "PYEXE=python\python.exe"
if not defined PYEXE (
  where py >nul 2>nul && set "PYEXE=py"
)
if not defined PYEXE (
  where python >nul 2>nul && set "PYEXE=python"
)
if not defined PYEXE (
  echo No se encontro Python.
  echo.
  echo Esta carpeta deberia traer Python adentro, en la subcarpeta "python".
  echo Si la bajaste sin esa subcarpeta, instala Python desde https://www.python.org/downloads/
  echo o pedi el paquete completo.
  echo.
  pause
  exit /b 1
)

echo Iniciando TA GUIANAEL MFF...
"%PYEXE%" desktop\servidor.py
if errorlevel 1 (
  echo.
  echo La app termino con un error. La ventana queda abierta para que puedas leerlo.
  pause
)
endlocal
