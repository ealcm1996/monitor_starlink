echo Creando archivo de inicio automático...
(
echo @echo off
echo cd /d "C:\starlink-grpc-tools-main\"
echo start /B /MIN "Starlink Web Server" pythonw.exe starlink_map.py
) > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\StartStarlinkMonitor.bat"

REM Inicia el servicio inmediatamente
cd /d "%~dp0"

REM Inicia el servidor web Flask
start /B "Starlink Web Server" pythonw.exe starlink_map.py

REM Espera 5 segundos para que el servidor inicie
timeout /t 5 /nobreak >nul

REM Abre el navegador
echo Abriendo navegador...
start http://localhost:5000

echo Configuracion completada! La aplicacion esta corriendo en http://localhost:5000
echo Se ha creado un acceso directo en el escritorio
echo El servidor se iniciara automaticamente al iniciar Windows
echo Para detener el servidor, use el Administrador de tareas y busque "pythonw.exe"
pause