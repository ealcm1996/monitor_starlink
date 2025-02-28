import os
import sys
import subprocess
import ctypes
import shutil
import urllib.request
import time
import win32com.client

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_python():
    print("\n=== Instalando Python 3.9.0 ===")
    print("→ Descargando instalador...")
    python_url = "https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe"
    installer_path = os.path.join(os.environ['TEMP'], "python_installer.exe")
    
    try:
        urllib.request.urlretrieve(python_url, installer_path)
        print("→ Ejecutando instalador (esto puede tardar unos minutos)...")
        subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_pip=1"], 
                      check=True)
        os.remove(installer_path)
        print("✓ Python 3.9.0 instalado correctamente")
        
        # Actualizar PATH en la sesión actual
        os.environ['PATH'] = f"C:\\Python39;C:\\Python39\\Scripts;{os.environ['PATH']}"
        time.sleep(5)
    except Exception as e:
        print(f"Error instalando Python: {str(e)}")
        raise

def install_dependencies():
    print("\n=== Verificando dependencias ===")
    
    python_path = shutil.which('python')
    if not python_path:
        python_path = "C:\\Python39\\python.exe"
    
    dependencies = [
        ("wheel", "Wheel"),
        ("setuptools", "Setup Tools"),
        ("typing_extensions", "Typing Extensions"),
        ("flask", "Flask"),
        ("grpcio", "gRPC"),
        ("grpcio-tools", "gRPC Tools"),
        ("protobuf<=3.20.0", "Protocol Buffers"),
        ("firebase-admin", "Firebase Admin"),
        ("pywin32", "Windows COM"),
        ("werkzeug", "Werkzeug"),
        ("click", "Click"),
        ("itsdangerous", "It's Dangerous"),
        ("Jinja2", "Jinja2"),
        ("MarkupSafe", "MarkupSafe")
    ]
    
    # Verificar qué paquetes faltan
    missing_deps = []
    for package, description in dependencies:
        try:
            # Intentar importar el módulo
            module_name = package.split('<=')[0]  # Remover versión específica si existe
            __import__(module_name.replace('-', '_'))
            print(f"✓ {description} ya está instalado")
        except ImportError:
            missing_deps.append((package, description))
    
    if not missing_deps:
        print("✓ Todas las dependencias están instaladas")
        return
    
    print("\n→ Instalando dependencias faltantes...")
    for package, description in missing_deps:
        try:
            print(f"\n→ Instalando {description}...")
            result = subprocess.run([
                python_path, "-m", "pip", "install", 
                package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ {description} instalado correctamente")
            else:
                print(f"Error instalando {package}: {result.stderr}")
                raise Exception(f"Error instalando {package}")
        except Exception as e:
            print(f"Error instalando {package}: {str(e)}")
            raise

def generate_grpc_files(project_path):
    print("\n=== Generando archivos gRPC ===")
    try:
        # Crear directorio para los archivos generados
        spacex_dir = os.path.join(project_path, "spacex", "api", "device")
        os.makedirs(spacex_dir, exist_ok=True)

        # Copiar el archivo .proto
        proto_source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "device.proto")
        proto_dest = os.path.join(spacex_dir, "device.proto")
        shutil.copy2(proto_source, proto_dest)

        # Generar archivos Python desde .proto
        python_path = shutil.which('python')
        subprocess.run([
            python_path, "-m", "grpc_tools.protoc",
            f"--proto_path={os.path.dirname(proto_dest)}",
            f"--python_out={project_path}",
            f"--grpc_python_out={project_path}",
            proto_dest
        ], check=True)

        print("✓ Archivos gRPC generados correctamente")
    except Exception as e:
        print(f"Error generando archivos gRPC: {str(e)}")
        raise

def setup_project():
    print("\n=== Configurando proyecto ===")
    project_path = "C:\\starlink-monitor"
    
    print("→ Creando directorio del proyecto...")
    os.makedirs(project_path, exist_ok=True)
    
    print("→ Copiando archivos...")
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Copiando desde: {current_dir}")
    
    # Lista completa de archivos requeridos
    required_files = [
        'starlink_map.py',
        'starlink_grpc.py',
        'templates',
        'static',
        'device.proto'
    ]
    
    # Verificar y copiar archivos
    for source in required_files:
        try:
            source_path = os.path.join(current_dir, source)
            dest_path = os.path.join(project_path, source)
            print(f"Copiando {source} a {dest_path}")
            
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)
            else:
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(source_path, dest_path)
        except Exception as e:
            print(f"Error copiando {source}: {str(e)}")
            # No interrumpir si faltan archivos opcionales
            if source not in ['manifest.json', 'sw.js']:
                raise

    # Generar archivos gRPC después de copiar los archivos
    generate_grpc_files(project_path)
    
    print("→ Configurando inicio automático...")
    try:
        python_path = shutil.which('python')
        if not python_path:
            python_path = "C:\\Python39\\python.exe"
        
        # Verificar que Python existe
        if not os.path.exists(python_path):
            raise Exception(f"No se encontró Python en {python_path}")
        
        # Crear script bat para iniciar el servidor con verificación de dependencias
        server_bat = os.path.join(project_path, "start_server.ps1")
        with open(server_bat, "w") as f:
            f.write(f'''
Write-Host "===== Iniciando Starlink Monitor ====="

Write-Host "[1/3] Verificando entorno..."
Set-Location "{project_path}"
$env:PYTHONPATH = "{project_path}"

Write-Host "[2/3] Preparando archivos gRPC..."
$spacexPath = "spacex\\api\\device"
if (-not (Test-Path $spacexPath)) {{
    New-Item -ItemType Directory -Path $spacexPath -Force | Out-Null
}}

Copy-Item "device.proto" -Destination "$spacexPath\\device.proto" -Force

Write-Host "[3/3] Iniciando servidor web..."
$env:FLASK_APP = "starlink_map.py"
$env:FLASK_ENV = "development"

Write-Host ""
Write-Host "Iniciando servidor en http://localhost:5000"
Write-Host "(Si el navegador no se abre automáticamente, abre http://localhost:5000 manualmente)"
Write-Host ""

Start-Process "http://localhost:5000"

& "{python_path}" starlink_map.py

if ($LASTEXITCODE -ne 0) {{
    Write-Host ""
    Write-Host "Error al iniciar el servidor"
    Write-Host "Verifica que:"
    Write-Host "1. Tienes conexión con la antena Starlink"
    Write-Host "2. Puedes acceder a 192.168.100.1"
    Write-Host "3. No hay otro programa usando el puerto 5000"
    pause
    exit 1
}}
''')
        
        # Crear acceso directo que ejecuta PowerShell
        shell = win32com.client.Dispatch("WScript.Shell")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "Starlink Monitor.lnk")
        
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = "powershell.exe"
        shortcut.Arguments = f"-ExecutionPolicy Bypass -File \"{server_bat}\""
        shortcut.IconLocation = os.path.join(project_path, "static", "icons", "starlink-icon.ico")
        shortcut.WindowStyle = 1  # Normal window
        shortcut.save()
        
        print(f"✓ Acceso directo creado en: {shortcut_path}")
        
        # Verificar que el acceso directo se creó
        if not os.path.exists(shortcut_path):
            raise Exception("No se pudo crear el acceso directo")
        
        # Iniciar el servidor
        print("→ Iniciando servidor...")
        subprocess.Popen([server_bat], shell=True)
        
        print("✓ Configuración completada")
        
    except Exception as e:
        print(f"Error en la configuración: {str(e)}")
        raise

def check_python_version():
    try:
        # Intentar ejecutar Python y obtener su versión
        result = subprocess.run(['python', '--version'], 
                              capture_output=True, 
                              text=True)
        version = result.stdout.strip()
        
        if '3.9.0' in version:
            print("✓ Python 3.9.0 ya está instalado")
            return True
        else:
            print(f"→ Versión de Python detectada: {version}")
            print("→ Se necesita Python 3.9.0")
            return False
    except:
        return False

def verify_dependencies():
    print("\n=== Verificando dependencias básicas ===")
    try:
        import typing_extensions
        import flask
        import grpc
        from grpc import _server
        import firebase_admin
        import win32com.client
        print("✓ Dependencias básicas instaladas correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error: Falta la dependencia {str(e)}")
        return False

def setup_firewall():
    print("\n=== Configurando Firewall ===")
    try:
        # Agregar regla para permitir el puerto 5000
        subprocess.run([
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            'name="Starlink Monitor"',
            'dir=in', 'action=allow', 'protocol=TCP', 'localport=5000'
        ], check=True)
        print("✓ Regla de firewall agregada correctamente")
        return True
    except Exception as e:
        print(f"⚠️ Advertencia al configurar firewall: {str(e)}")
        return False

def kill_port_5000():
    try:
        # Buscar y matar procesos usando el puerto 5000
        result = subprocess.run(['netstat', '-ano', '|', 'findstr', ':5000'], 
                              capture_output=True, text=True, shell=True)
        for line in result.stdout.splitlines():
            if ':5000' in line:
                pid = line.strip().split()[-1]
                subprocess.run(['taskkill', '/F', '/PID', pid], 
                             capture_output=True)
        return True
    except Exception as e:
        print(f"⚠️ Advertencia al liberar puerto 5000: {str(e)}")
        return False

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    print("\n=== INSTALADOR DE STARLINK MONITOR ===")
    print("Por favor, espere mientras se completa la instalación...\n")
    
    try:
        # Verificar Python antes de intentar instalarlo
        if not check_python_version():
            print("→ Instalando Python 3.9.0...")
            install_python()
        
        # Instalar dependencias básicas
        install_dependencies()
        if not verify_dependencies():
            raise Exception("No se pudieron instalar las dependencias básicas")
            
        # Configurar proyecto y generar archivos gRPC
        setup_project()
        
        # Configurar firewall
        if not setup_firewall():
            raise Exception("No se pudo configurar el firewall")
        
        # Liberar puerto 5000
        if not kill_port_5000():
            raise Exception("No se pudo liberar el puerto 5000")
        
        print("\n=== ¡INSTALACIÓN COMPLETADA! ===")
        print("• El servicio iniciará automáticamente al hacer clic en el acceso directo")
        print("• Puedes acceder al sistema usando el acceso directo 'Starlink Monitor' en el escritorio")
        print("• Iniciando el servicio...")
        
        # Usar el nuevo archivo BAT
        server_bat = os.path.join("C:\\starlink-monitor", "start_server.bat")
        if os.path.exists(server_bat):
            subprocess.Popen([server_bat], shell=True)
        else:
            print(f"\n⚠️ Advertencia: No se pudo encontrar {server_bat}")
            print("Por favor, inicia el servicio manualmente usando el acceso directo del escritorio")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nLa instalación no se completó correctamente.")
        input("\nPresiona Enter para salir...")
        sys.exit(1)

    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main() 