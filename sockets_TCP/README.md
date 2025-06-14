# Laboratorio de Sockets TCP en Python

## Descripción General

Este proyecto implementa una suite completa de ejercicios prácticos de sockets TCP en Python, basado en el documento académico `LAB_SocketsTCP.pdf`. El código está diseñado para enseñar los conceptos fundamentales de programación con sockets TCP a través de ejemplos prácticos e interactivos.

## Estructura del Proyecto

### Arquitectura del Código

El proyecto está organizado en ocho ejercicios principales, cada uno construyendo sobre los conceptos del anterior:

**Ejercicio 1: Escaner de Puertos** - Introduce el concepto básico de conexión TCP y manejo de errores.

**Ejercicio 2: Información de Conexión** - Enseña a extraer metadatos de las conexiones establecidas.

**Ejercicio 3: Cliente Daytime** - Demuestra la recepción de datos de un servidor.

**Ejercicio 4: Cliente Echo** - Implementa comunicación bidireccional básica.

**Ejercicios 5-6: Servidor y Cliente Básico** - Introduce el desarrollo de servidores TCP.

**Ejercicio 7: Sistema de Mensajería** - Demuestra el manejo de múltiples clientes simultáneos.

**Ejercicio 8: Transferencia de Archivos** - Implementa un protocolo de aplicación completo.

## Análisis Detallado por Ejercicio

### Ejercicio 1: Escaner de Puertos (`scan_ports`)

```python
def scan_ports(host, start_port=1, end_port=1024):
```

**Propósito Educativo**: Este ejercicio enseña los fundamentos de la conexión TCP, incluyendo el manejo de excepciones y timeouts.

**Conceptos Clave**:
- **Creación de Sockets**: Utiliza `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` para crear un socket TCP.
- **Manejo de Timeouts**: Implementa `sock.settimeout(0.1)` para evitar bloqueos prolongados.
- **Detección de Puertos Abiertos**: Usa `connect_ex()` que retorna 0 para conexiones exitosas.
- **Gestión de Recursos**: Cierra cada socket después de la prueba para evitar agotamiento de recursos.

**Aplicación Práctica**: Herramienta útil para administradores de red y profesionales de seguridad para descubrir servicios disponibles en un host.

### Ejercicio 2: Información de Conexión (`connection_info`)

```python
def connection_info(host, port):
```

**Propósito Educativo**: Demuestra cómo extraer información detallada de una conexión TCP establecida.

**Conceptos Clave**:
- **Metadatos de Conexión**: Usa `getpeername()` para obtener información del extremo remoto.
- **Información Local**: Utiliza `getsockname()` para datos del extremo local.
- **Propiedades del Socket**: Accede a `family` y `type` para características del socket.

**Equivalencia con Java**: Replica la funcionalidad de `getInetAddress()` y `getPort()` de Java.

### Ejercicio 3: Cliente Daytime (`daytime_client`)

```python
def daytime_client(host, port=13):
```

**Propósito Educativo**: Introduce la recepción de datos desde un servidor, implementando un protocolo estándar.

**Conceptos Clave**:
- **Protocolo Daytime (RFC867)**: Servidor envía fecha/hora al establecer conexión.
- **Recepción de Datos**: Utiliza `recv(1024)` para leer datos del socket.
- **Decodificación**: Convierte bytes a string usando `decode('ascii')`.

**Servidor de Prueba Incluido**: El proyecto incluye `LocalDaytimeServer` para pruebas independientes.

### Ejercicio 4: Cliente Echo (`echo_client`)

```python
def echo_client(host, port=7):
```

**Propósito Educativo**: Demuestra comunicación bidireccional interactiva con un servidor.

**Conceptos Clave**:
- **Protocolo Echo (RFC862)**: Servidor devuelve exactamente los datos recibidos.
- **Comunicación Interactiva**: Bucle que permite al usuario enviar múltiples mensajes.
- **Codificación de Mensajes**: Convierte strings a bytes con `encode('ascii')`.

**Implementación del Servidor**: Incluye `LocalEchoServer` para pruebas locales completas.

### Ejercicios 5-6: Servidor y Cliente Básico

```python
def basic_server(port):
def basic_client(host, port):
```

**Propósito Educativo**: Transición de cliente a servidor, introduciendo conceptos de servidor TCP.

**Conceptos del Servidor**:
- **Vinculación de Puerto**: `bind(('', port))` asocia el socket a un puerto específico.
- **Modo de Escucha**: `listen(5)` pone el socket en modo de escucha con cola de 5 conexiones.
- **Aceptación de Conexiones**: `accept()` bloquea hasta recibir una conexión.
- **Reutilización de Direcciones**: `SO_REUSEADDR` evita errores de "Address already in use".

**Flujo de Trabajo**: El servidor envía un mensaje de bienvenida con timestamp y cierra la conexión inmediatamente.

### Ejercicio 7: Sistema de Mensajería (`MessageServer`)

```python
class MessageServer:
```

**Propósito Educativo**: Introduce conceptos avanzados de concurrencia y manejo de múltiples clientes.

**Conceptos Avanzados**:
- **Programación Multihilo**: Cada cliente se maneja en un hilo separado usando `threading.Thread`.
- **Sincronización**: Utiliza `threading.Lock()` para acceso seguro a recursos compartidos.
- **Broadcast de Mensajes**: Implementa retransmisión de mensajes a todos los clientes conectados.
- **Gestión de Clientes**: Mantiene una lista de clientes activos y maneja desconexiones.

**Comandos Implementados**:
- `/list`: Muestra número de clientes conectados
- `/quit`: Desconecta al cliente
- Mensajes de texto: Se retransmiten a todos los demás clientes

**Arquitectura de Threads**: El servidor principal acepta conexiones mientras threads independientes manejan cada cliente.

### Ejercicio 8: Transferencia de Archivos (`FileTransferServer`)

```python
class FileTransferServer:
```

**Propósito Educativo**: Implementa un protocolo de aplicación completo con transferencia de datos binarios.

**Conceptos de Protocolo**:
- **Comandos Estructurados**: Implementa comandos `LIST`, `GET <filename>`, y `QUIT`.
- **Transferencia Binaria**: Maneja archivos en modo binario con `'rb'` y `'wb'`.
- **Protocolo de Confirmación**: Usa handshake con mensajes `SENDING_FILE` y `READY`.
- **Transferencia por Chunks**: Divide archivos grandes en bloques de 4KB para eficiencia.

**Gestión de Archivos**:
- **Directorio Compartido**: Utiliza `shared_files/` como repositorio de archivos.
- **Información de Archivos**: Proporciona nombre y tamaño antes de la transferencia.
- **Validación**: Verifica existencia de archivos antes de intentar envío.

**Cliente de Transferencia**: Incluye barra de progreso y manejo de errores robusto.

## Herramientas Auxiliares

### Servidores de Prueba Locales

El proyecto incluye implementaciones locales de servidores estándar para permitir pruebas independientes:

**LocalDaytimeServer**: Implementa RFC867 localmente, eliminando dependencia de servidores externos.

**LocalEchoServer**: Proporciona servidor echo local para pruebas de comunicación bidireccional.

### Herramientas de Diagnóstico

```python
def network_diagnostics():
def test_connection(host, port, timeout=5):
```

**Funcionalidades**:
- Prueba de conectividad a hosts remotos
- Detección de IP local
- Verificación de puertos disponibles
- Diagnóstico de problemas de red

### Utilidades del Sistema

```python
def create_sample_files():
def format_bytes(bytes_count):
```

**Propósito**: Facilitan la demostración y testing de las funcionalidades implementadas.

## Interfaces de Usuario

### Menú Interactivo

El proyecto incluye dos interfaces de menú:

**Menú Basic** (`demo_menu`): Interfaz simple para ejecutar ejercicios individuales.

**Menú Extendido** (`extended_menu`): Incluye herramientas de diagnóstico, servidores locales, y demo automatizada.

### Interfaz de Línea de Comandos

```bash
python tcp_sockets_python.py scan localhost
python tcp_sockets_python.py daytime time.nist.gov
python tcp_sockets_python.py server 8000
```

**Comandos Disponibles**:
- `scan <host>`: Ejecuta escaneo de puertos
- `daytime <host>`: Conecta a servidor daytime
- `echo <host>`: Inicia cliente echo
- `server <puerto>`: Inicia servidor básico
- `msgserver <puerto>`: Inicia servidor de mensajería
- `fileserver <puerto>`: Inicia servidor de archivos
- `demo`: Ejecuta demostración automatizada

## Características Técnicas

### Manejo de Concurrencia

El código implementa patrones de concurrencia apropiados para cada tipo de servidor:

**Servidores Simples**: Manejan un cliente a la vez (servidores básico, daytime, echo).

**Servidores Avanzados**: Utilizan threading para manejar múltiples clientes simultáneamente.

**Sincronización**: Implementa locks para proteger recursos compartidos en entornos multihilo.

### Gestión de Errores

```python
try:
    # Operación de socket
except socket.error as e:
    print(f"Error de socket: {e}")
except KeyboardInterrupt:
    print("Interrumpido por usuario")
```

**Estrategia de Manejo**:
- Captura específica de `socket.error` para errores de red
- Manejo de `KeyboardInterrupt` para terminación limpia
- Gestión de `ValueError` para entrada de usuario inválida
- Cleanup automático de recursos (sockets, archivos)

### Compatibilidad de Protocolos

**Estándares Implementados**:
- RFC867 (Daytime Protocol)
- RFC862 (Echo Protocol)
- Protocolos personalizados para mensajería y transferencia de archivos

**Codificación**: Utiliza ASCII para protocolos de texto y binario para transferencia de archivos.

## Guía de Uso

### Instalación y Ejecución

```bash
# Clonar el proyecto
git clone [repository-url]

# Ejecutar menú interactivo
python tcp_sockets_python.py

# Ejecutar comando específico
python tcp_sockets_python.py demo
```

**Requisitos**: Python 3.6+ (utiliza solo bibliotecas estándar)

### Escenarios de Prueba Recomendados

**Prueba Local Completa**:
1. Ejecutar `python tcp_sockets_python.py demo` para iniciar servidores locales
2. Usar menú interactivo para probar cada ejercicio
3. Ejecutar múltiples instancias para probar concurrencia

**Prueba de Red Externa**:
1. Usar `scan_ports` con hosts remotos
2. Conectar a servidores daytime/echo públicos
3. Ejecutar diagnósticos de red

**Prueba de Mensajería**:
1. Terminal 1: Iniciar servidor de mensajería
2. Terminales 2-4: Conectar múltiples clientes
3. Probar broadcast de mensajes

### Solución de Problemas Comunes

**Puerto en Uso**: El código incluye `SO_REUSEADDR` para evitar errores de puerto ocupado.

**Timeouts**: Configurados apropiadamente para cada tipo de operación.

**Permisos**: Usa puertos altos (>1024) para evitar requerir privilegios administrativos.

**Firewall**: En Windows, puede ser necesario permitir Python en el firewall.

## Valor Educativo

### Progresión Pedagógica

El proyecto sigue una secuencia cuidadosamente diseñada:

**Fundamentos**: Comienza con conceptos básicos de conexión TCP.

**Comunicación**: Progresa a comunicación bidireccional.

**Servicios**: Introduce desarrollo de servidores.

**Concurrencia**: Avanza a sistemas multicliente.

**Protocolos**: Culmina con protocolos de aplicación completos.

### Conceptos de Programación Enseñados

**Sockets TCP**: Creación, configuración, y uso de sockets.

**Protocolos de Red**: Implementación de protocolos estándar e personalizados.

**Concurrencia**: Threading, sincronización, y recursos compartidos.

**Manejo de Errores**: Estrategias robustas para aplicaciones de red.

**Arquitectura Cliente-Servidor**: Patrones de diseño para sistemas distribuidos.

**Transferencia de Datos**: Manejo de datos de texto y binarios.

### Aplicaciones Prácticas

**Administración de Sistemas**: Herramientas de diagnóstico de red.

**Desarrollo de Aplicaciones**: Fundamentos para aplicaciones de red.

**Seguridad**: Comprensión de servicios de red y escaneo de puertos.

**Comunicaciones**: Implementación de sistemas de mensajería.

**Transferencia de Datos**: Protocolos de transferencia de archivos.

## Extensiones Posibles

### Mejoras de Seguridad

- Implementación de SSL/TLS
- Autenticación de usuarios
- Cifrado de mensajes

### Optimizaciones de Rendimiento

- Pool de threads para servidores
- Buffering avanzado
- Compresión de datos

### Funcionalidades Adicionales

- Interface gráfica de usuario
- Logging detallado
- Métricas de rendimiento
- Soporte para IPv6

## Conclusión

Este laboratorio de sockets TCP proporciona una base sólida para entender la programación de red en Python. Cada ejercicio está diseñado para enseñar conceptos específicos mientras construye hacia aplicaciones más complejas. El código incluye herramientas de diagnóstico, servidores de prueba, y múltiples interfaces de usuario para facilitar el aprendizaje y la experimentación.

La implementación sigue mejores prácticas de programación Python, incluyendo documentación exhaustiva, manejo robusto de errores, y arquitectura modular que facilita la comprensión y extensión del código.