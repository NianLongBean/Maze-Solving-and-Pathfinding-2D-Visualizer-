@echo off
setlocal
cd /d "%~dp0"

py -3 -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name MazeVisualizer --distpath dist --workpath build\pyinstaller ^
  --specpath build --add-data "%~dp0assets;assets" main.py

if errorlevel 1 exit /b %errorlevel%
echo.
echo Build complete: %~dp0dist\MazeVisualizer.exe
