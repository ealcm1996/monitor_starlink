@echo off
sc create StarlinkMonitor binPath= "C:\xampp\htdocs\starlink-grpc-tools-main\start_starlink.bat" start= auto
sc description StarlinkMonitor "Servicio de monitoreo de Starlink"
sc start StarlinkMonitor 