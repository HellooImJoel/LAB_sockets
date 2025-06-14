#!/usr/bin/env python3
"""
Implementación completa de los ejercicios de Sockets TCP
Basado en el documento LAB_SocketsTCP.pdf
Desarrollado por: Análisis del documento académico
"""

import socket
import threading
import sys
import os
import time
from datetime import datetime

# =============================================================================
# EJERCICIO 1: Escaner de puertos
# =============================================================================

def scan_ports(host, start_port=1, end_port=1024):
    """
    Escanea puertos abiertos en un host específico.
    
    Esta función implementa el Ejercicio 1 del documento, que requiere
    determinar a cuáles puertos se puede establecer conexión.
    
    Args:
        host (str): Dirección del host a escanear
        start_port (int): Puerto inicial del rango
        end_port (int): Puerto final del rango
    """
    print(f"\n=== Escaneando puertos en {host} ===")
    print(f"Rango: {start_port} - {end_port}")
    
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        try:
            # Intentamos establecer conexión con timeout corto
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)  # 100ms timeout para acelerar el escaneo
            
            result = sock.connect_ex((host, port))
            
            if result == 0:  # Conexión exitosa
                open_ports.append(port)
                print(f"Puerto {port}: ABIERTO")
            
            sock.close()
            
        except socket.gaierror:
            print(f"Error: No se pudo resolver el host {host}")
            break
        except Exception as e:
            # Puerto cerrado o error de conexión
            pass
    
    print(f"\nPuertos abiertos encontrados: {open_ports}")
    return open_ports

# =============================================================================
# EJERCICIO 2: Información de conexión
# =============================================================================

def connection_info(host, port):
    """
    Se conecta a un host y muestra información detallada de la conexión.
    
    Implementa el Ejercicio 2, mostrando información usando métodos
    equivalentes a getInetAddress() y getPort() de Java.
    
    Args:
        host (str): Host al que conectarse
        port (int): Puerto de conexión
    """
    print(f"\n=== Información de conexión a {host}:{port} ===")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Información del socket remoto
        remote_addr = sock.getpeername()
        print(f"Dirección remota: {remote_addr[0]}")
        print(f"Puerto remoto: {remote_addr[1]}")
        
        # Información del socket local
        local_addr = sock.getsockname()
        print(f"Dirección local: {local_addr[0]}")
        print(f"Puerto local: {local_addr[1]}")
        
        # Información adicional del socket
        print(f"Familia de direcciones: {sock.family}")
        print(f"Tipo de socket: {sock.type}")
        
        sock.close()
        print("Conexión cerrada exitosamente")
        
    except socket.error as e:
        print(f"Error de conexión: {e}")

# =============================================================================
# EJERCICIO 3: Cliente Daytime (Recibir datos)
# =============================================================================

def daytime_client(host, port=13):
    """
    Cliente que se conecta al servicio daytime para obtener fecha y hora.
    
    Implementa el ejemplo del protocolo daytime del documento.
    El servidor envía la fecha y hora actual cuando se establece la conexión.
    
    Args:
        host (str): Servidor daytime
        port (int): Puerto del servicio (por defecto 13)
    """
    print(f"\n=== Cliente Daytime conectando a {host}:{port} ===")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Información de conexión
        remote_addr = sock.getpeername()
        print(f"Conectado a: {remote_addr[0]}")
        print(f"Puerto: {remote_addr[1]}")
        
        # Recibir datos del servidor
        data = sock.recv(1024).decode('ascii').strip()
        print(f"Día y hora del servidor: {data}")
        
        sock.close()
        
    except socket.error as e:
        print(f"Error en cliente daytime: {e}")

# =============================================================================
# EJERCICIO 4: Cliente Echo (Enviar y recibir datos)
# =============================================================================

def echo_client(host, port=7):
    """
    Cliente interactivo que implementa el protocolo echo.
    
    El usuario puede escribir mensajes que se envían al servidor,
    y el servidor responde con el mismo mensaje (eco).
    Implementa el ejemplo del documento con protocolo RFC862.
    
    Args:
        host (str): Servidor echo
        port (int): Puerto del servicio (por defecto 7)
    """
    print(f"\n=== Cliente Echo conectando a {host}:{port} ===")
    print("Escriba mensajes (escriba '.' para salir)")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        print(f"Conectado exitosamente a {host}:{port}")
        
        while True:
            # Leer entrada del usuario
            message = input("Mensaje: ")
            
            if message == ".":
                break
            
            # Enviar mensaje al servidor
            sock.send((message + "\n").encode('ascii'))
            
            # Recibir respuesta del servidor
            response = sock.recv(1024).decode('ascii').strip()
            print(f"Echo del servidor: {response}")
        
        sock.close()
        print("Conexión cerrada")
        
    except socket.error as e:
        print(f"Error en cliente echo: {e}")

# =============================================================================
# EJERCICIOS 5-6: Servidor básico con mensaje
# =============================================================================

def basic_server(port):
    """
    Servidor básico que acepta conexiones y envía un mensaje de bienvenida.
    
    Implementa los ejercicios 5 y 6 del documento.
    El servidor acepta conexiones, envía un mensaje y cierra la conexión.
    
    Args:
        port (int): Puerto en el que el servidor escuchará
    """
    print(f"\n=== Servidor básico iniciando en puerto {port} ===")
    
    try:
        # Crear socket servidor
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Permitir reutilizar la dirección (evita errores de "Address already in use")
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Vincular el socket al puerto
        server_sock.bind(('', port))
        
        # Escuchar conexiones (máximo 5 en cola)
        server_sock.listen(5)
        
        print(f"Servidor atendiendo en el puerto {port}")
        print("Presione Ctrl+C para detener el servidor")
        
        while True:
            try:
                # Aceptar conexión entrante
                client_sock, client_addr = server_sock.accept()
                
                print(f"Nueva conexión desde {client_addr[0]}:{client_addr[1]}")
                
                # Enviar mensaje de bienvenida
                welcome_msg = f"Se ha conectado al socket servidor en puerto {port}\n"
                welcome_msg += f"Hora de conexión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                client_sock.send(welcome_msg.encode('ascii'))
                
                # Cerrar conexión con el cliente
                client_sock.close()
                print(f"Conexión con {client_addr[0]}:{client_addr[1]} cerrada")
                
            except KeyboardInterrupt:
                print("\nDeteniendo servidor...")
                break
            except socket.error as e:
                print(f"Error en conexión: {e}")
        
        server_sock.close()
        
    except socket.error as e:
        print(f"Error del servidor: {e}")

def basic_client(host, port):
    """
    Cliente que se conecta al servidor básico y muestra el mensaje recibido.
    
    Complementa el ejercicio 6, actuando como cliente del servidor básico.
    
    Args:
        host (str): Dirección del servidor
        port (int): Puerto del servidor
    """
    print(f"\n=== Cliente básico conectando a {host}:{port} ===")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Recibir mensaje del servidor
        data = sock.recv(1024).decode('ascii')
        print("Mensaje del servidor:")
        print(data)
        
        sock.close()
        
    except socket.error as e:
        print(f"Error del cliente básico: {e}")

# =============================================================================
# EJERCICIO 7: Sistema de mensajería
# =============================================================================

class MessageServer:
    """
    Servidor de mensajería que permite comunicación entre múltiples clientes.
    
    Implementa el Ejercicio 7 del documento.
    Los clientes pueden enviar mensajes que se retransmiten a otros clientes conectados.
    """
    
    def __init__(self, port):
        self.port = port
        self.clients = []  # Lista de sockets de clientes conectados
        self.running = True
        self.lock = threading.Lock()  # Para acceso seguro a la lista de clientes
    
    def handle_client(self, client_sock, client_addr):
        """
        Maneja la comunicación con un cliente específico.
        
        Args:
            client_sock: Socket del cliente
            client_addr: Dirección del cliente
        """
        print(f"Cliente {client_addr[0]}:{client_addr[1]} conectado")
        
        # Enviar mensaje de bienvenida
        welcome = f"Bienvenido al servidor de mensajería\nClientes conectados: {len(self.clients)}\n"
        welcome += "Comandos disponibles:\n"
        welcome += "  /list - Ver clientes conectados\n"
        welcome += "  /quit - Desconectarse\n"
        welcome += "  Cualquier otro texto se enviará como mensaje\n\n"
        
        try:
            client_sock.send(welcome.encode('utf-8'))
            
            while self.running:
                # Recibir mensaje del cliente
                data = client_sock.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                
                if message == "/quit":
                    break
                elif message == "/list":
                    client_list = f"Clientes conectados: {len(self.clients)}\n"
                    client_sock.send(client_list.encode('utf-8'))
                else:
                    # Retransmitir mensaje a todos los otros clientes
                    full_message = f"[{client_addr[0]}:{client_addr[1]}]: {message}\n"
                    self.broadcast_message(full_message, exclude=client_sock)
        
        except socket.error as e:
            print(f"Error con cliente {client_addr[0]}:{client_addr[1]}: {e}")
        
        finally:
            # Remover cliente de la lista
            with self.lock:
                if client_sock in self.clients:
                    self.clients.remove(client_sock)
            
            client_sock.close()
            print(f"Cliente {client_addr[0]}:{client_addr[1]} desconectado")
    
    def broadcast_message(self, message, exclude=None):
        """
        Envía un mensaje a todos los clientes conectados.
        
        Args:
            message (str): Mensaje a enviar
            exclude: Socket a excluir del broadcast (generalmente el remitente)
        """
        with self.lock:
            clients_to_remove = []
            
            for client in self.clients:
                if client != exclude:
                    try:
                        client.send(message.encode('utf-8'))
                    except socket.error:
                        # Cliente desconectado, marcar para eliminación
                        clients_to_remove.append(client)
            
            # Remover clientes desconectados
            for client in clients_to_remove:
                self.clients.remove(client)
    
    def start(self):
        """Inicia el servidor de mensajería."""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('', self.port))
            server_sock.listen(10)
            
            print(f"Servidor de mensajería iniciado en puerto {self.port}")
            print("Presione Ctrl+C para detener")
            
            while self.running:
                try:
                    client_sock, client_addr = server_sock.accept()
                    
                    # Agregar cliente a la lista
                    with self.lock:
                        self.clients.append(client_sock)
                    
                    # Crear hilo para manejar el cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                
                except KeyboardInterrupt:
                    print("\nDeteniendo servidor de mensajería...")
                    self.running = False
                    break
            
            server_sock.close()
            
        except socket.error as e:
            print(f"Error del servidor de mensajería: {e}")

def message_client(host, port):
    """
    Cliente para el sistema de mensajería.
    
    Permite al usuario enviar y recibir mensajes en tiempo real.
    
    Args:
        host (str): Dirección del servidor
        port (int): Puerto del servidor
    """
    print(f"\n=== Cliente de mensajería conectando a {host}:{port} ===")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Función para recibir mensajes en un hilo separado
        def receive_messages():
            while True:
                try:
                    data = sock.recv(1024)
                    if not data:
                        break
                    print(data.decode('utf-8'), end='')
                except socket.error:
                    break
        
        # Iniciar hilo receptor
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Bucle principal para enviar mensajes
        print("Conectado al servidor de mensajería")
        print("Escriba sus mensajes (Ctrl+C para salir):")
        
        while True:
            try:
                message = input()
                if message:
                    sock.send((message + "\n").encode('utf-8'))
                    if message == "/quit":
                        break
            except KeyboardInterrupt:
                sock.send("/quit\n".encode('utf-8'))
                break
        
        sock.close()
        
    except socket.error as e:
        print(f"Error del cliente de mensajería: {e}")

# =============================================================================
# EJERCICIO 8: Sistema de transferencia de archivos
# =============================================================================

class FileTransferServer:
    """
    Servidor para transferencia de archivos entre clientes.
    
    Implementa el Ejercicio 8 del documento.
    Los clientes pueden listar archivos disponibles y descargarlos.
    """
    
    def __init__(self, port, shared_directory="shared_files"):
        self.port = port
        self.shared_directory = shared_directory
        self.running = True
        
        # Crear directorio compartido si no existe
        if not os.path.exists(shared_directory):
            os.makedirs(shared_directory)
            print(f"Directorio compartido creado: {shared_directory}")
    
    def handle_client(self, client_sock, client_addr):
        """
        Maneja las solicitudes de transferencia de archivos de un cliente.
        
        Args:
            client_sock: Socket del cliente
            client_addr: Dirección del cliente
        """
        print(f"Cliente de archivos {client_addr[0]}:{client_addr[1]} conectado")
        
        try:
            # Enviar menú de comandos
            menu = "=== Servidor de Transferencia de Archivos ===\n"
            menu += "Comandos disponibles:\n"
            menu += "  LIST - Listar archivos disponibles\n"
            menu += "  GET <filename> - Descargar archivo\n"
            menu += "  QUIT - Desconectarse\n\n"
            
            client_sock.send(menu.encode('utf-8'))
            
            while self.running:
                # Recibir comando del cliente
                data = client_sock.recv(1024)
                if not data:
                    break
                
                command = data.decode('utf-8').strip().upper()
                
                if command == "QUIT":
                    break
                elif command == "LIST":
                    self.send_file_list(client_sock)
                elif command.startswith("GET "):
                    filename = command[4:].strip()
                    self.send_file(client_sock, filename)
                else:
                    error_msg = "Comando no reconocido. Use LIST, GET <filename>, o QUIT\n"
                    client_sock.send(error_msg.encode('utf-8'))
        
        except socket.error as e:
            print(f"Error con cliente de archivos {client_addr[0]}:{client_addr[1]}: {e}")
        
        finally:
            client_sock.close()
            print(f"Cliente de archivos {client_addr[0]}:{client_addr[1]} desconectado")
    
    def send_file_list(self, client_sock):
        """
        Envía la lista de archivos disponibles al cliente.
        
        Args:
            client_sock: Socket del cliente
        """
        try:
            files = os.listdir(self.shared_directory)
            
            if not files:
                response = "No hay archivos disponibles\n"
            else:
                response = "Archivos disponibles:\n"
                for i, filename in enumerate(files, 1):
                    file_path = os.path.join(self.shared_directory, filename)
                    file_size = os.path.getsize(file_path)
                    response += f"  {i}. {filename} ({file_size} bytes)\n"
            
            response += "\n"
            client_sock.send(response.encode('utf-8'))
            
        except Exception as e:
            error_msg = f"Error al listar archivos: {e}\n"
            client_sock.send(error_msg.encode('utf-8'))
    
    def send_file(self, client_sock, filename):
        """
        Envía un archivo específico al cliente.
        
        Args:
            client_sock: Socket del cliente
            filename: Nombre del archivo a enviar
        """
        file_path = os.path.join(self.shared_directory, filename)
        
        try:
            if not os.path.exists(file_path):
                error_msg = f"Archivo '{filename}' no encontrado\n"
                client_sock.send(error_msg.encode('utf-8'))
                return
            
            file_size = os.path.getsize(file_path)
            
            # Enviar información del archivo
            file_info = f"SENDING_FILE:{filename}:{file_size}\n"
            client_sock.send(file_info.encode('utf-8'))
            
            # Esperar confirmación del cliente
            confirmation = client_sock.recv(1024).decode('utf-8').strip()
            
            if confirmation == "READY":
                # Enviar contenido del archivo
                with open(file_path, 'rb') as f:
                    while True:
                        chunk = f.read(4096)  # Leer en chunks de 4KB
                        if not chunk:
                            break
                        client_sock.send(chunk)
                
                print(f"Archivo '{filename}' enviado exitosamente")
            
        except Exception as e:
            error_msg = f"Error al enviar archivo: {e}\n"
            client_sock.send(error_msg.encode('utf-8'))
    
    def start(self):
        """Inicia el servidor de transferencia de archivos."""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('', self.port))
            server_sock.listen(5)
            
            print(f"Servidor de archivos iniciado en puerto {self.port}")
            print(f"Directorio compartido: {self.shared_directory}")
            print("Presione Ctrl+C para detener")
            
            while self.running:
                try:
                    client_sock, client_addr = server_sock.accept()
                    
                    # Crear hilo para manejar el cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                
                except KeyboardInterrupt:
                    print("\nDeteniendo servidor de archivos...")
                    self.running = False
                    break
            
            server_sock.close()
            
        except socket.error as e:
            print(f"Error del servidor de archivos: {e}")

def file_transfer_client(host, port, download_directory="downloads"):
    """
    Cliente para transferencia de archivos.
    
    Permite listar y descargar archivos del servidor.
    
    Args:
        host (str): Dirección del servidor
        port (int): Puerto del servidor
        download_directory (str): Directorio local para descargas
    """
    print(f"\n=== Cliente de transferencia de archivos conectando a {host}:{port} ===")
    
    # Crear directorio de descargas si no existe
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
        print(f"Directorio de descargas creado: {download_directory}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Recibir menú del servidor
        menu = sock.recv(1024).decode('utf-8')
        print(menu)
        
        while True:
            try:
                command = input("Comando: ").strip()
                
                if not command:
                    continue
                
                sock.send(command.encode('utf-8'))
                
                if command.upper() == "QUIT":
                    break
                elif command.upper().startswith("GET "):
                    # Manejar descarga de archivo
                    self.handle_file_download(sock, download_directory)
                else:
                    # Recibir respuesta del servidor
                    response = sock.recv(4096).decode('utf-8')
                    print(response)
            
            except KeyboardInterrupt:
                sock.send("QUIT".encode('utf-8'))
                break
        
        sock.close()
        
    except socket.error as e:
        print(f"Error del cliente de archivos: {e}")
    
    def handle_file_download(self, sock, download_directory):
        """
        Maneja la descarga de un archivo del servidor.
        
        Args:
            sock: Socket conectado al servidor
            download_directory: Directorio donde guardar el archivo
        """
        try:
            # Recibir información del archivo
            file_info = sock.recv(1024).decode('utf-8').strip()
            
            if file_info.startswith("SENDING_FILE:"):
                parts = file_info.split(":")
                filename = parts[1]
                file_size = int(parts[2])
                
                print(f"Descargando '{filename}' ({file_size} bytes)...")
                
                # Confirmar que estamos listos para recibir
                sock.send("READY".encode('utf-8'))
                
                # Recibir y guardar el archivo
                file_path = os.path.join(download_directory, filename)
                
                with open(file_path, 'wb') as f:
                    bytes_received = 0
                    
                    while bytes_received < file_size:
                        chunk = sock.recv(min(4096, file_size - bytes_received))
                        if not chunk:
                            break
                        
                        f.write(chunk)
                        bytes_received += len(chunk)
                        
                        # Mostrar progreso
                        progress = (bytes_received / file_size) * 100
                        print(f"\rProgreso: {progress:.1f}%", end='', flush=True)
                
                print(f"\nArchivo descargado exitosamente: {file_path}")
            else:
                # Mensaje de error del servidor
                print(file_info)
        
        except Exception as e:
            print(f"Error durante la descarga: {e}")

# =============================================================================
# FUNCIONES DE DEMOSTRACIÓN Y MENÚ PRINCIPAL
# =============================================================================

def create_sample_files():
    """Crea archivos de ejemplo para el servidor de transferencia."""
    shared_dir = "shared_files"
    
    if not os.path.exists(shared_dir):
        os.makedirs(shared_dir)
    
    # Crear algunos archivos de ejemplo
    files_to_create = [
        ("ejemplo.txt", "Este es un archivo de ejemplo para transferencia.\nContiene varias líneas de texto.\n"),
        ("datos.csv", "nombre,edad,ciudad\nJuan,25,Concepción del Uruguay\nMaría,30,Buenos Aires\n"),
        ("info.md", "# Archivo Markdown\n\nEste es un ejemplo de archivo **Markdown**.\n\n- Item 1\n- Item 2\n")
    ]
    
    for filename, content in files_to_create:
        file_path = os.path.join(shared_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"Archivos de ejemplo creados en {shared_dir}")

def demo_menu():
    """Menú principal para demostrar todos los ejercicios."""
    print("\n" + "="*60)
    print("IMPLEMENTACIÓN DE SOCKETS TCP - LABORATORIO PRÁCTICO")
    print("Basado en el documento LAB_SocketsTCP.pdf")
    print("="*60)
    
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1.  Escanear puertos (Ejercicio 1)")
        print("2.  Información de conexión (Ejercicio 2)")
        print("3.  Cliente Daytime (Ejercicio 3)")
        print("4.  Cliente Echo (Ejercicio 4)")
        print("5.  Servidor básico (Ejercicios 5-6)")
        print("6.  Cliente básico (Ejercicios 5-6)")
        print("7.  Servidor de mensajería (Ejercicio 7)")
        print("8.  Cliente de mensajería (Ejercicio 7)")
        print("9.  Servidor de archivos (Ejercicio 8)")
        print("10. Cliente de archivos (Ejercicio 8)")
        print("11. Crear archivos de ejemplo")
        print("0.  Salir")
        
        try:
            option = input("\nSeleccione una opción: ").strip()
            
            if option == "0":
                print("¡Hasta luego!")
                break
            elif option == "1":
                host = input("Host a escanear (localhost): ").strip() or "localhost"
                scan_ports(host, 1, 100)  # Rango reducido para demo
            elif option == "2":
                host = input("Host (google.com): ").strip() or "google.com"
                port = int(input("Puerto (80): ").strip() or "80")
                connection_info(host, port)
            elif option == "3":
                host = input("Servidor daytime (time.nist.gov): ").strip() or "time.nist.gov"
                daytime_client(host)
            elif option == "4":
                host = input("Servidor echo (localhost): ").strip() or "localhost"
                port = int(input("Puerto (7): ").strip() or "7")
                echo_client(host, port)
            elif option == "5":
                port = int(input("Puerto del servidor (8000): ").strip() or "8000")
                basic_server(port)
            elif option == "6":
                host = input("Host del servidor (localhost): ").strip() or "localhost"
                port = int(input("Puerto del servidor (8000): ").strip() or "8000")
                basic_client(host, port)
            elif option == "7":
                port = int(input("Puerto del servidor de mensajería (9000): ").strip() or "9000")
                server = MessageServer(port)
                server.start()
            elif option == "8":
                host = input("Host del servidor (localhost): ").strip() or "localhost"
                port = int(input("Puerto del servidor (9000): ").strip() or "9000")
                message_client(host, port)
            elif option == "9":
                port = int(input("Puerto del servidor de archivos (9001): ").strip() or "9001")
                server = FileTransferServer(port)
                server.start()
            elif option == "10":
                host = input("Host del servidor (localhost): ").strip() or "localhost"
                port = int(input("Puerto del servidor (9001): ").strip() or "9001")
                file_transfer_client(host, port)
            elif option == "11":
                create_sample_files()
            else:
                print("Opción no válida. Intente nuevamente.")
        
        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario.")
            break
        except ValueError:
            print("Error: Ingrese un número válido.")
        except Exception as e:
            print(f"Error: {e}")

# =============================================================================
# FUNCIONES AUXILIARES Y UTILIDADES
# =============================================================================

def test_connection(host, port, timeout=5):
    """
    Prueba si es posible conectarse a un host y puerto específicos.
    
    Args:
        host (str): Host a probar
        port (int): Puerto a probar
        timeout (int): Tiempo límite en segundos
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_local_ip():
    """
    Obtiene la dirección IP local de la máquina.
    
    Returns:
        str: Dirección IP local
    """
    try:
        # Crear una conexión temporal para obtener la IP local
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(("8.8.8.8", 80))
        local_ip = temp_sock.getsockname()[0]
        temp_sock.close()
        return local_ip
    except:
        return "127.0.0.1"

def format_bytes(bytes_count):
    """
    Formatea un número de bytes en una representación legible.
    
    Args:
        bytes_count (int): Número de bytes
    
    Returns:
        str: Representación formateada (ej: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} TB"

# =============================================================================
# SERVIDORES DE PRUEBA LOCALES
# =============================================================================

class LocalDaytimeServer:
    """
    Implementación local del servidor daytime para pruebas.
    
    Proporciona la fecha y hora actual cuando un cliente se conecta.
    Útil para probar el cliente daytime sin depender de servidores externos.
    """
    
    def __init__(self, port=1313):  # Puerto alternativo para evitar privilegios
        self.port = port
        self.running = True
    
    def handle_client(self, client_sock, client_addr):
        """
        Maneja una conexión de cliente enviando la fecha y hora.
        
        Args:
            client_sock: Socket del cliente
            client_addr: Dirección del cliente
        """
        try:
            # Enviar fecha y hora actual
            current_time = datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
            response = f"{current_time}\r\n"
            
            client_sock.send(response.encode('ascii'))
            print(f"Enviado daytime a {client_addr[0]}:{client_addr[1]}: {current_time}")
            
        except socket.error as e:
            print(f"Error enviando daytime: {e}")
        finally:
            client_sock.close()
    
    def start(self):
        """Inicia el servidor daytime local."""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('', self.port))
            server_sock.listen(5)
            
            print(f"Servidor Daytime local iniciado en puerto {self.port}")
            print("Presione Ctrl+C para detener")
            
            while self.running:
                try:
                    client_sock, client_addr = server_sock.accept()
                    
                    # Manejar cliente en hilo separado
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                
                except KeyboardInterrupt:
                    print("\nDeteniendo servidor Daytime...")
                    self.running = False
                    break
            
            server_sock.close()
            
        except socket.error as e:
            print(f"Error del servidor Daytime: {e}")

class LocalEchoServer:
    """
    Implementación local del servidor echo para pruebas.
    
    Devuelve exactamente los mismos datos que recibe de cada cliente.
    Implementa el protocolo RFC862 para pruebas locales.
    """
    
    def __init__(self, port=1307):  # Puerto alternativo
        self.port = port
        self.running = True
    
    def handle_client(self, client_sock, client_addr):
        """
        Maneja una conexión de cliente implementando el protocolo echo.
        
        Args:
            client_sock: Socket del cliente
            client_addr: Dirección del cliente
        """
        print(f"Cliente echo conectado: {client_addr[0]}:{client_addr[1]}")
        
        try:
            while True:
                # Recibir datos del cliente
                data = client_sock.recv(1024)
                if not data:
                    break
                
                # Enviar los mismos datos de vuelta (echo)
                client_sock.send(data)
                
                # Log del mensaje
                message = data.decode('ascii', errors='ignore').strip()
                print(f"Echo para {client_addr[0]}:{client_addr[1]}: {message}")
        
        except socket.error as e:
            print(f"Error en cliente echo {client_addr[0]}:{client_addr[1]}: {e}")
        finally:
            client_sock.close()
            print(f"Cliente echo desconectado: {client_addr[0]}:{client_addr[1]}")
    
    def start(self):
        """Inicia el servidor echo local."""
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind(('', self.port))
            server_sock.listen(5)
            
            print(f"Servidor Echo local iniciado en puerto {self.port}")
            print("Presione Ctrl+C para detener")
            
            while self.running:
                try:
                    client_sock, client_addr = server_sock.accept()
                    
                    # Manejar cliente en hilo separado
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                
                except KeyboardInterrupt:
                    print("\nDeteniendo servidor Echo...")
                    self.running = False
                    break
            
            server_sock.close()
            
        except socket.error as e:
            print(f"Error del servidor Echo: {e}")

# =============================================================================
# HERRAMIENTAS DE DIAGNÓSTICO Y TESTING
# =============================================================================

def network_diagnostics():
    """
    Ejecuta diagnósticos básicos de red para verificar la conectividad.
    
    Útil para troubleshooting cuando los ejercicios no funcionan como esperado.
    """
    print("\n=== DIAGNÓSTICOS DE RED ===")
    
    # Información local
    print(f"IP local: {get_local_ip()}")
    print(f"Hostname local: {socket.gethostname()}")
    
    # Pruebas de conectividad básica
    test_hosts = [
        ("google.com", 80, "HTTP"),
        ("time.nist.gov", 13, "Daytime"),
        ("localhost", 22, "SSH (si disponible)")
    ]
    
    print("\nPruebas de conectividad:")
    for host, port, service in test_hosts:
        if test_connection(host, port, timeout=3):
            print(f"  ✓ {host}:{port} ({service}) - CONECTADO")
        else:
            print(f"  ✗ {host}:{port} ({service}) - NO DISPONIBLE")
    
    # Puertos locales comunes para pruebas
    print(f"\nPuertos locales sugeridos para pruebas:")
    suggested_ports = [8000, 8080, 9000, 9001, 1313, 1307]
    
    for port in suggested_ports:
        if test_connection("localhost", port, timeout=1):
            print(f"  Puerto {port}: EN USO")
        else:
            print(f"  Puerto {port}: DISPONIBLE")

def run_demo_suite():
    """
    Ejecuta una suite de demostración automatizada de todos los ejercicios.
    
    Inicia servidores locales y ejecuta clientes para demostrar funcionalidad.
    """
    print("\n=== SUITE DE DEMOSTRACIÓN AUTOMATIZADA ===")
    print("Esta demo iniciará varios servidores y ejecutará pruebas automatizadas.")
    
    # Crear archivos de ejemplo
    create_sample_files()
    
    print("\n1. Iniciando servidores de prueba...")
    
    # Iniciar servidores en hilos separados
    servers = []
    
    # Servidor Daytime
    daytime_server = LocalDaytimeServer(1313)
    daytime_thread = threading.Thread(target=daytime_server.start)
    daytime_thread.daemon = True
    daytime_thread.start()
    servers.append(("Daytime", 1313))
    
    # Servidor Echo
    echo_server = LocalEchoServer(1307)
    echo_thread = threading.Thread(target=echo_server.start)
    echo_thread.daemon = True
    echo_thread.start()
    servers.append(("Echo", 1307))
    
    # Dar tiempo a que los servidores se inicien
    time.sleep(2)
    
    print("Servidores iniciados:")
    for server_name, port in servers:
        print(f"  - {server_name} en puerto {port}")
    
    print("\n2. Ejecutando pruebas automatizadas...")
    
    # Prueba de escaneo de puertos
    print("\n--- Prueba: Escaneo de puertos ---")
    scan_ports("localhost", 1300, 1320)
    
    # Prueba de información de conexión
    print("\n--- Prueba: Información de conexión ---")
    connection_info("google.com", 80)
    
    # Prueba del cliente daytime
    print("\n--- Prueba: Cliente Daytime ---")
    daytime_client("localhost", 1313)
    
    print("\n=== DEMO COMPLETADA ===")
    print("Los servidores siguen ejecutándose en segundo plano.")
    print("Puede usar el menú principal para interactuar con ellos.")

# =============================================================================
# MENÚ EXTENDIDO CON OPCIONES ADICIONALES
# =============================================================================

def extended_menu():
    """Menú extendido con opciones adicionales y herramientas de diagnóstico."""
    print("\n" + "="*70)
    print("LABORATORIO AVANZADO DE SOCKETS TCP")
    print("Implementación completa con herramientas de diagnóstico")
    print("="*70)
    
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("EJERCICIOS BÁSICOS:")
        print("1.  Escanear puertos (Ejercicio 1)")
        print("2.  Información de conexión (Ejercicio 2)")
        print("3.  Cliente Daytime (Ejercicio 3)")
        print("4.  Cliente Echo (Ejercicio 4)")
        print("5.  Servidor básico (Ejercicios 5-6)")
        print("6.  Cliente básico (Ejercicios 5-6)")
        
        print("\nSISTEMAS AVANZADOS:")
        print("7.  Servidor de mensajería (Ejercicio 7)")
        print("8.  Cliente de mensajería (Ejercicio 7)")
        print("9.  Servidor de archivos (Ejercicio 8)")
        print("10. Cliente de archivos (Ejercicio 8)")
        
        print("\nSERVIDORES DE PRUEBA LOCALES:")
        print("11. Servidor Daytime local")
        print("12. Servidor Echo local")
        
        print("\nHERRAMIENTAS:")
        print("13. Crear archivos de ejemplo")
        print("14. Diagnóstico de red")
        print("15. Demo automatizada")
        print("16. Manual de uso")
        
        print("\n0.  Salir")
        
        try:
            option = input("\nSeleccione una opción: ").strip()
            
            if option == "0":
                print("¡Gracias por usar el laboratorio de Sockets TCP!")
                break
            elif option == "1":
                host = input("Host a escanear (localhost): ").strip() or "localhost"
                start = int(input("Puerto inicial (1): ").strip() or "1")
                end = int(input("Puerto final (100): ").strip() or "100")
                scan_ports(host, start, end)
            elif option == "2":
                host = input("Host (google.com): ").strip() or "google.com"
                port = int(input("Puerto (80): ").strip() or "80")
                connection_info(host, port)
            elif option == "3":
                host = input("Servidor daytime (localhost para local, time.nist.gov para externo): ").strip()
                if not host:
                    host = "localhost"
                    port = 1313
                else:
                    port = int(input("Puerto (13 para externo, 1313 para local): ").strip() or "13")
                daytime_client(host, port)
            elif option == "4":
                host = input("Servidor echo (localhost): ").strip() or "localhost"
                port = int(input("Puerto (1307 para local, 7 para externo): ").strip() or "1307")
                echo_client(host, port)
            elif option == "5":
                port = int(input("Puerto del servidor (8000): ").strip() or "8000")
                basic_server(port)
            elif option == "6":
                host = input("Host del servidor (localhost): ").strip() or "localhost"
                port = int(input("Puerto del servidor (8000): ").strip() or "8000")
                basic_client(host, port)
            elif option == "7":
                port = int(input("Puerto del servidor de mensajería (9000): ").strip() or "9000")
                server = MessageServer(port)
                server.start()
            elif option == "8":
                host = input("Host del servidor (localhost): ").strip() or "localhost"
                port = int(input("Puerto del servidor (9000): ").strip() or "9000")
                message_client(host, port)
            elif option == "9":
                port = int(input("Puerto del servidor de archivos (9001): ").strip() or "9001")
                server = FileTransferServer(port)
                server.start()
            elif option == "10":
                host = input("Host del servidor (localhost): ").strip() or "localhost"
                port = int(input("Puerto del servidor (9001): ").strip() or "9001")
                file_transfer_client(host, port)
            elif option == "11":
                port = int(input("Puerto del servidor Daytime local (1313): ").strip() or "1313")
                server = LocalDaytimeServer(port)
                server.start()
            elif option == "12":
                port = int(input("Puerto del servidor Echo local (1307): ").strip() or "1307")
                server = LocalEchoServer(port)
                server.start()
            elif option == "13":
                create_sample_files()
            elif option == "14":
                network_diagnostics()
            elif option == "15":
                run_demo_suite()
            elif option == "16":
                show_manual()
            else:
                print("Opción no válida. Intente nuevamente.")
        
        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario.")
            break
        except ValueError as e:
            print(f"Error: Ingrese un valor válido. ({e})")
        except Exception as e:
            print(f"Error inesperado: {e}")

def show_manual():
    """Muestra el manual de uso del laboratorio."""
    manual = """
=== MANUAL DE USO - LABORATORIO SOCKETS TCP ===

Este laboratorio implementa todos los ejercicios del documento LAB_SocketsTCP.pdf
utilizando Python en lugar de Java. Los conceptos y funcionalidades son idénticos.

EJERCICIOS IMPLEMENTADOS:

1. ESCANEO DE PUERTOS
   - Prueba conexiones a un rango de puertos en un host
   - Útil para descobrir servicios disponibles

2. INFORMACIÓN DE CONEXIÓN
   - Muestra detalles de una conexión TCP establecida
   - Equivalente a getInetAddress() y getPort() de Java

3. CLIENTE DAYTIME
   - Se conecta a un servidor que proporciona fecha/hora
   - Implementa el protocolo RFC867
   - Use localhost:1313 para servidor local

4. CLIENTE ECHO
   - Envía mensajes que el servidor devuelve idénticos
   - Implementa el protocolo RFC862
   - Use localhost:1307 para servidor local

5-6. SERVIDOR/CLIENTE BÁSICO
   - Servidor que acepta conexiones y envía mensaje
   - Cliente que se conecta y muestra el mensaje

7. SISTEMA DE MENSAJERÍA
   - Servidor multicliente para chat en tiempo real
   - Los mensajes se retransmiten a todos los clientes

8. TRANSFERENCIA DE ARCHIVOS
   - Servidor que permite descargar archivos
   - Cliente con comandos LIST y GET

SERVIDORES DE PRUEBA LOCALES:
- Daytime Server (puerto 1313): Proporciona fecha/hora
- Echo Server (puerto 1307): Devuelve mensajes recibidos

CONSEJOS DE USO:

1. Para pruebas locales, use siempre "localhost" como host
2. Los puertos altos (>1024) no requieren privilegios administrativos
3. Use Ctrl+C para detener servidores
4. Los servidores manejan múltiples clientes simultáneamente
5. Ejecute servidores en una terminal y clientes en otra

SOLUCIÓN DE PROBLEMAS:

- Si un puerto está ocupado, pruebe con otro número
- Para Windows, puede necesitar permitir Python en el firewall
- Use la opción de diagnóstico de red para verificar conectividad
- Los servidores externos (time.nist.gov) pueden no estar disponibles

EJEMPLOS DE USO TÍPICOS:

1. Ejecutar demo completa:
   Opción 15 → Se inician servidores locales y ejecutan pruebas

2. Chat entre dos usuarios:
   Terminal 1: Opción 7 → Puerto 9000
   Terminal 2: Opción 8 → localhost:9000
   Terminal 3: Opción 8 → localhost:9000

3. Transferir archivos:
   Terminal 1: Opción 13 (crear archivos)
   Terminal 2: Opción 9 → Puerto 9001
   Terminal 3: Opción 10 → localhost:9001

¡Presione Enter para continuar!
"""
    print(manual)
    input()

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Función principal que inicia la aplicación.
    
    Detecta si se ejecuta con argumentos de línea de comandos
    o si debe mostrar el menú interactivo.
    """
    if len(sys.argv) > 1:
        # Modo línea de comandos
        command = sys.argv[1].lower()
        
        if command == "scan" and len(sys.argv) >= 3:
            host = sys.argv[2]
            start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            end = int(sys.argv[4]) if len(sys.argv) > 4 else 1024
            scan_ports(host, start, end)
        
        elif command == "daytime" and len(sys.argv) >= 3:
            host = sys.argv[2]
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 13
            daytime_client(host, port)
        
        elif command == "echo" and len(sys.argv) >= 3:
            host = sys.argv[2]
            port = int(sys.argv[3]) if len(sys.argv) > 3 else 7
            echo_client(host, port)
        
        elif command == "server" and len(sys.argv) >= 3:
            port = int(sys.argv[2])
            basic_server(port)
        
        elif command == "msgserver" and len(sys.argv) >= 3:
            port = int(sys.argv[2])
            server = MessageServer(port)
            server.start()
        
        elif command == "fileserver" and len(sys.argv) >= 3:
            port = int(sys.argv[2])
            server = FileTransferServer(port)
            server.start()
        
        elif command == "demo":
            run_demo_suite()
        
        elif command == "help":
            print("Uso:")
            print("  python sockets_tcp.py                    - Menú interactivo")
            print("  python sockets_tcp.py scan <host>        - Escanear puertos")
            print("  python sockets_tcp.py daytime <host>     - Cliente daytime")
            print("  python sockets_tcp.py echo <host>        - Cliente echo")
            print("  python sockets_tcp.py server <puerto>    - Servidor básico")
            print("  python sockets_tcp.py msgserver <puerto> - Servidor mensajería")
            print("  python sockets_tcp.py fileserver <puerto> - Servidor archivos")
            print("  python sockets_tcp.py demo               - Demo automatizada")
        
        else:
            print("Comando no reconocido. Use 'help' para ver opciones.")
    
    else:
        # Modo interactivo
        try:
            extended_menu()
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")

if __name__ == "__main__":
    main()