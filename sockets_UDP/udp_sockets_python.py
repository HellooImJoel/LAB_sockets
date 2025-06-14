#!/usr/bin/env python3
"""
Implementación completa de Sockets UDP en Python
Basado en el documento LAB_Sockets_UDP.pdf

Este módulo implementa todas las funcionalidades presentadas en el documento:
- Creación de paquetes UDP (equivalente a DatagramPacket)
- Manejo de sockets UDP (equivalente a DatagramSocket)
- Envío y recepción de datagramas
- Ejercicios prácticos A, D, E, y F
"""

import socket
import sys
import json
import threading
import time
from typing import Optional, Tuple, Any
from dataclasses import dataclass, asdict


# =============================================================================
# CLASE MENSAJE (Ejercicio F)
# =============================================================================

@dataclass
class Mensaje:
    """
    Clase para encapsular mensajes UDP, similar al requerimiento del Ejercicio F.
    Permite serializar/deserializar datos complejos en datagramas UDP.
    """
    contenido: str
    timestamp: float
    remitente: str
    tipo: str = "texto"
    
    def to_array_bytes(self) -> bytes:
        """
        Convierte el mensaje a array de bytes para transmisión UDP.
        Utiliza JSON para serialización, lo que permite manejar estructuras complejas.
        """
        try:
            mensaje_dict = asdict(self)
            mensaje_json = json.dumps(mensaje_dict, ensure_ascii=False)
            return mensaje_json.encode('utf-8')
        except Exception as e:
            raise ValueError(f"Error al convertir mensaje a bytes: {e}")
    
    @classmethod
    def from_array_bytes(cls, datos: bytes) -> 'Mensaje':
        """
        Crea un objeto Mensaje desde un array de bytes recibido.
        Deserializa los datos JSON para reconstruir el mensaje original.
        """
        try:
            mensaje_json = datos.decode('utf-8')
            mensaje_dict = json.loads(mensaje_json)
            return cls(**mensaje_dict)
        except Exception as e:
            raise ValueError(f"Error al crear mensaje desde bytes: {e}")


# =============================================================================
# CLASE PAQUETE UDP (Equivalente a DatagramPacket)
# =============================================================================

class PaqueteUDP:
    """
    Clase que modela un Datagrama UDP, equivalente a DatagramPacket de Java.
    Encapsula los datos y metadatos necesarios para la transmisión UDP.
    """
    
    def __init__(self, datos: bytes, longitud: int, direccion: str, puerto: int):
        """
        Constructor del paquete UDP.
        
        Args:
            datos: Array de bytes con el contenido del datagrama
            longitud: Longitud de los datos válidos
            direccion: Dirección IP de destino
            puerto: Puerto de destino
        """
        self._datos = datos
        self._longitud = longitud
        self._direccion = direccion
        self._puerto = puerto
        self._offset = 0  # Offset inicial siempre 0 en esta implementación
    
    @property
    def datos(self) -> bytes:
        """Retorna los datos del paquete como array de bytes."""
        return self._datos
    
    @property
    def longitud(self) -> int:
        """Retorna la longitud de los datos válidos."""
        return self._longitud
    
    @property
    def direccion(self) -> str:
        """Retorna la dirección de destino."""
        return self._direccion
    
    @property
    def puerto(self) -> int:
        """Retorna el puerto de destino."""
        return self._puerto
    
    @property
    def offset(self) -> int:
        """Retorna el offset de los datos (siempre 0 en esta implementación)."""
        return self._offset
    
    def mostrar_info(self):
        """
        Muestra información detallada del paquete UDP.
        Equivalente a los System.out.println del ejemplo Java.
        """
        print("Paquete UDP:")
        print(f"Dirección Internet: {self._direccion}")
        print(f"Datos como bytes: {self._datos}")
        print(f"Datos como String: {self._datos.decode('utf-8', errors='ignore')}")
        print(f"Longitud: {self._longitud}")
        print(f"Offset: {self._offset}")
        print(f"Puerto: {self._puerto}")


# =============================================================================
# CLASE SOCKET UDP (Equivalente a DatagramSocket)
# =============================================================================

class SocketUDP:
    """
    Clase que implementa un Socket UDP, equivalente a DatagramSocket de Java.
    Proporciona métodos para enviar y recibir datagramas UDP.
    """
    
    def __init__(self, puerto_local: Optional[int] = None):
        """
        Constructor del socket UDP.
        
        Args:
            puerto_local: Puerto local para bind. Si es None, se asigna automáticamente.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._puerto_local = puerto_local
        self._direccion_local = "0.0.0.0"  # Escucha en todas las interfaces
        self._conectado = False
        self._direccion_remota = None
        self._puerto_remoto = None
        
        # Si se especifica puerto local, hacer bind
        if puerto_local is not None:
            try:
                self._socket.bind((self._direccion_local, puerto_local))
                print(f"Socket UDP vinculado al puerto {puerto_local}")
            except OSError as e:
                raise ConnectionError(f"No se pudo vincular al puerto {puerto_local}: {e}")
    
    def conectar(self, direccion_remota: str, puerto_remoto: int):
        """
        Simula una 'conexión' UDP para especificar destino por defecto.
        UDP es sin conexión, pero esto establece un destino predeterminado.
        """
        self._direccion_remota = direccion_remota
        self._puerto_remoto = puerto_remoto
        self._conectado = True
        print(f"Socket 'conectado' a {direccion_remota}:{puerto_remoto}")
    
    def enviar(self, paquete: PaqueteUDP):
        """
        Envía un paquete UDP al destino especificado.
        
        Args:
            paquete: PaqueteUDP a enviar
        """
        try:
            direccion_destino = (paquete.direccion, paquete.puerto)
            bytes_enviados = self._socket.sendto(paquete.datos[:paquete.longitud], direccion_destino)
            print(f"Enviados {bytes_enviados} bytes a {direccion_destino}")
            return bytes_enviados
        except Exception as e:
            raise ConnectionError(f"Error al enviar paquete: {e}")
    
    def recibir(self, tamaño_buffer: int = 1024) -> PaqueteUDP:
        """
        Recibe un paquete UDP. El socket se bloquea hasta recibir datos.
        
        Args:
            tamaño_buffer: Tamaño máximo del buffer de recepción
            
        Returns:
            PaqueteUDP con los datos recibidos
        """
        try:
            datos, direccion_origen = self._socket.recvfrom(tamaño_buffer)
            direccion_ip, puerto_origen = direccion_origen
            
            # Crear un PaqueteUDP con los datos recibidos
            paquete_recibido = PaqueteUDP(
                datos=datos,
                longitud=len(datos),
                direccion=direccion_ip,
                puerto=puerto_origen
            )
            
            print(f"Recibidos {len(datos)} bytes desde {direccion_origen}")
            return paquete_recibido
            
        except Exception as e:
            raise ConnectionError(f"Error al recibir paquete: {e}")
    
    def establecer_timeout(self, timeout_ms: int):
        """
        Establece timeout para operaciones de socket.
        
        Args:
            timeout_ms: Timeout en milisegundos
        """
        timeout_segundos = timeout_ms / 1000.0
        self._socket.settimeout(timeout_segundos)
        print(f"Timeout establecido en {timeout_ms} milisegundos")
    
    def establecer_buffer_envio(self, tamaño: int):
        """Establece el tamaño del buffer de envío."""
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, tamaño)
    
    def establecer_buffer_recepcion(self, tamaño: int):
        """Establece el tamaño del buffer de recepción."""
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, tamaño)
    
    def obtener_info_socket(self):
        """
        Muestra información completa del socket.
        Equivalente al ejemplo de mostrar datos del socket en Java.
        """
        try:
            direccion_local, puerto_local = self._socket.getsockname()
            buffer_envio = self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            buffer_recepcion = self._socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            timeout = self._socket.gettimeout()
            
            print("=== Información del Socket UDP ===")
            print(f"Dirección Local: {direccion_local}")
            print(f"Puerto Local: {puerto_local}")
            print(f"Dirección Remota: {self._direccion_remota if self._conectado else 'No conectado'}")
            print(f"Puerto Remoto: {self._puerto_remoto if self._conectado else 'No conectado'}")
            print(f"Buffer de envío: {buffer_envio} bytes")
            print(f"Buffer de recepción: {buffer_recepcion} bytes")
            print(f"Timeout: {timeout * 1000 if timeout else 'Sin timeout'} milisegundos")
            print("=================================")
            
        except Exception as e:
            print(f"Error al obtener información del socket: {e}")
    
    def cerrar(self):
        """Cierra el socket UDP."""
        self._socket.close()
        print("Socket UDP cerrado")


# =============================================================================
# EJERCICIO A: Crear un Datagrama UDP desde línea de comandos
# =============================================================================

def ejercicio_a():
    """
    Implementa el Ejercicio A: crear un datagrama UDP con parámetros de línea de comandos.
    Uso: python script.py ejercicio_a <host> <puerto> <datos>
    """
    print("=== EJERCICIO A: Crear Datagrama UDP ===")
    
    if len(sys.argv) < 5:
        print("Uso: python script.py ejercicio_a <host> <puerto> <datos>")
        print("Ejemplo: python script.py ejercicio_a 127.0.0.1 80 'Hola mundo'")
        return
    
    try:
        host = sys.argv[2]
        puerto = int(sys.argv[3])
        datos = sys.argv[4]
        
        # Convertir datos a bytes
        buffer_datos = datos.encode('utf-8')
        
        # Crear el paquete UDP
        paquete_udp = PaqueteUDP(
            datos=buffer_datos,
            longitud=len(buffer_datos),
            direccion=host,
            puerto=puerto
        )
        
        # Mostrar información del paquete
        paquete_udp.mostrar_info()
        
    except ValueError as e:
        print(f"Error: Puerto debe ser un número entero: {e}")
    except Exception as e:
        print(f"Error al crear el datagrama: {e}")


# =============================================================================
# EJERCICIO D: Crear Socket UDP con configuraciones específicas
# =============================================================================

def ejercicio_d():
    """
    Implementa el Ejercicio D: crear socket UDP con configuraciones específicas.
    """
    print("=== EJERCICIO D: Configurar Socket UDP ===")
    
    try:
        # Crear socket UDP sin puerto específico (se asigna automáticamente)
        socket_udp = SocketUDP()
        
        # Configurar buffers
        socket_udp.establecer_buffer_envio(800)
        socket_udp.establecer_buffer_recepcion(800)
        
        # Establecer timeout
        socket_udp.establecer_timeout(1000)  # 1000 milisegundos
        
        # Simular conexión para poder mostrar datos remotos
        socket_udp.conectar("127.0.0.1", 81)
        
        # Mostrar información del socket
        socket_udp.obtener_info_socket()
        
        # Cerrar socket
        socket_udp.cerrar()
        
    except Exception as e:
        print(f"Error en ejercicio D: {e}")


# =============================================================================
# EJERCICIO E: Leer paquetes UDP en puerto específico
# =============================================================================

def ejercicio_e():
    """
    Implementa el Ejercicio E: leer paquetes UDP en el puerto 8080 y mostrarlos como string.
    Nota: Cambiado de puerto 80 a 8080 para evitar problemas de permisos.
    """
    print("=== EJERCICIO E: Servidor UDP - Escuchar en Puerto 8080 ===")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        # Crear socket UDP vinculado al puerto 8080
        servidor = SocketUDP(puerto_local=8080)
        servidor.establecer_timeout(5000)  # Timeout de 5 segundos
        
        print("Servidor UDP iniciado. Esperando mensajes...")
        
        while True:
            try:
                # Recibir paquete
                paquete_recibido = servidor.recibir(1024)
                
                # Convertir datos a string
                mensaje = paquete_recibido.datos.decode('utf-8', errors='ignore')
                
                print(f"\n--- Mensaje Recibido ---")
                print(f"Desde: {paquete_recibido.direccion}:{paquete_recibido.puerto}")
                print(f"Contenido: {mensaje}")
                print(f"Longitud: {paquete_recibido.longitud} bytes")
                print("------------------------")
                
            except socket.timeout:
                print("Timeout - Sin mensajes recibidos")
                continue
                
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        if 'servidor' in locals():
            servidor.cerrar()


# =============================================================================
# EJERCICIO F: Aplicaciones para enviar y recibir mensajes usando clase Mensaje
# =============================================================================

def cliente_mensajes():
    """
    Aplicación cliente para enviar mensajes usando la clase Mensaje.
    """
    print("=== CLIENTE DE MENSAJES UDP ===")
    
    try:
        # Crear socket cliente
        cliente = SocketUDP()
        
        while True:
            # Solicitar datos al usuario
            contenido = input("Ingrese el mensaje (o 'quit' para salir): ")
            if contenido.lower() == 'quit':
                break
            
            remitente = input("Ingrese su nombre: ")
            
            # Crear mensaje
            mensaje = Mensaje(
                contenido=contenido,
                timestamp=time.time(),
                remitente=remitente,
                tipo="texto"
            )
            
            # Convertir a bytes
            datos_mensaje = mensaje.to_array_bytes()
            
            # Crear paquete UDP
            paquete = PaqueteUDP(
                datos=datos_mensaje,
                longitud=len(datos_mensaje),
                direccion="127.0.0.1",
                puerto=8080
            )
            
            # Enviar mensaje
            cliente.enviar(paquete)
            print("Mensaje enviado correctamente")
            
    except KeyboardInterrupt:
        print("\nCliente detenido por el usuario")
    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        if 'cliente' in locals():
            cliente.cerrar()


def servidor_mensajes():
    """
    Aplicación servidor para recibir mensajes usando la clase Mensaje.
    """
    print("=== SERVIDOR DE MENSAJES UDP ===")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        # Crear servidor
        servidor = SocketUDP(puerto_local=8080)
        
        print("Servidor de mensajes iniciado en puerto 8080...")
        
        while True:
            try:
                # Recibir paquete
                paquete_recibido = servidor.recibir(2048)
                
                # Deserializar mensaje
                mensaje = Mensaje.from_array_bytes(paquete_recibido.datos)
                
                # Mostrar mensaje formateado
                timestamp_legible = time.strftime('%Y-%m-%d %H:%M:%S', 
                                                 time.localtime(mensaje.timestamp))
                
                print(f"\n{'='*50}")
                print(f"MENSAJE RECIBIDO")
                print(f"{'='*50}")
                print(f"De: {mensaje.remitente}")
                print(f"Fecha: {timestamp_legible}")
                print(f"Tipo: {mensaje.tipo}")
                print(f"Contenido: {mensaje.contenido}")
                print(f"Origen: {paquete_recibido.direccion}:{paquete_recibido.puerto}")
                print(f"{'='*50}\n")
                
            except socket.timeout:
                continue
            except json.JSONDecodeError:
                print("Mensaje recibido no es un objeto Mensaje válido")
            except Exception as e:
                print(f"Error al procesar mensaje: {e}")
                
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error en el servidor: {e}")
    finally:
        if 'servidor' in locals():
            servidor.cerrar()


# =============================================================================
# EJEMPLOS ADICIONALES Y DEMOSTRACIONES
# =============================================================================

def demo_envio_simple():
    """
    Demostración simple de envío de datagrama UDP.
    Equivalente al ejemplo de envío a www.google.com del documento.
    """
    print("=== DEMO: Envío Simple de Datagrama ===")
    
    try:
        # Crear datos para enviar
        datos = "Estos son los datos del datagrama desde Python"
        buffer_datos = datos.encode('utf-8')
        
        # Crear paquete UDP (usando puerto 80 de Google)
        paquete = PaqueteUDP(
            datos=buffer_datos,
            longitud=len(buffer_datos),
            direccion="8.8.8.8",  # DNS público de Google
            puerto=53  # Puerto DNS
        )
        
        # Crear socket y enviar
        socket_cliente = SocketUDP()
        bytes_enviados = socket_cliente.enviar(paquete)
        
        print(f"Datagrama enviado exitosamente: {bytes_enviados} bytes")
        
        # Cerrar socket
        socket_cliente.cerrar()
        
    except Exception as e:
        print(f"Error en demo de envío: {e}")


def mostrar_ayuda():
    """Muestra la ayuda con todos los comandos disponibles."""
    print("=== SISTEMA DE SOCKETS UDP EN PYTHON ===")
    print("Basado en el documento LAB_Sockets_UDP.pdf")
    print()
    print("Comandos disponibles:")
    print("  ejercicio_a <host> <puerto> <datos>  - Crear y mostrar datagrama UDP")
    print("  ejercicio_d                          - Configurar socket UDP")
    print("  ejercicio_e                          - Servidor UDP en puerto 8080")
    print("  cliente                              - Cliente de mensajes")
    print("  servidor                             - Servidor de mensajes")
    print("  demo                                 - Demostración de envío simple")
    print("  ayuda                                - Mostrar esta ayuda")
    print()
    print("Ejemplos:")
    print("  python script.py ejercicio_a 127.0.0.1 8080 'Hola mundo'")
    print("  python script.py servidor    # En una terminal")
    print("  python script.py cliente     # En otra terminal")


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """
    Función principal que maneja la ejecución del programa según argumentos.
    """
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return
    
    comando = sys.argv[1].lower()
    
    if comando == "ejercicio_a":
        ejercicio_a()
    elif comando == "ejercicio_d":
        ejercicio_d()
    elif comando == "ejercicio_e":
        ejercicio_e()
    elif comando == "cliente":
        cliente_mensajes()
    elif comando == "servidor":
        servidor_mensajes()
    elif comando == "demo":
        demo_envio_simple()
    elif comando == "ayuda":
        mostrar_ayuda()
    else:
        print(f"Comando no reconocido: {comando}")
        mostrar_ayuda()


if __name__ == "__main__":
    main()
