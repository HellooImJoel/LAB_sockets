# Guía de Ejecución - Laboratorio Sockets TCP en Python

## Introducción

Este código implementa una suite completa de ejercicios prácticos sobre programación con sockets TCP, traduciendo conceptos tradicionalmente enseñados en Java al lenguaje Python. El laboratorio está diseñado como una herramienta educativa interactiva que permite a los estudiantes experimentar con diferentes aspectos de la comunicación de red de manera progresiva y práctica.

## Arquitectura del Código

El programa está estructurado en ocho ejercicios principales que van desde conceptos básicos hasta implementaciones más sofisticadas. Cada ejercicio se construye sobre los conocimientos adquiridos en los anteriores, creando una experiencia de aprendizaje gradual y coherente.

La arquitectura sigue un patrón modular donde cada funcionalidad está encapsulada en funciones y clases específicas. Esta organización facilita tanto el mantenimiento del código como la comprensión de cada concepto individual, permitiendo que los estudiantes se concentren en un aspecto particular de la programación con sockets sin perderse en la complejidad del conjunto.

## Formas de Ejecución

### Modo Interactivo (Recomendado para Aprendizaje)

La forma más educativa de usar este laboratorio es ejecutando el programa sin argumentos adicionales:

```bash
python tcp_sockets_python.py
```

Este comando iniciará un menú interactivo que presenta todas las opciones disponibles de manera organizada. El menú está diseñado pensando en el proceso de aprendizaje, presentando primero los ejercicios básicos y progresando hacia funcionalidades más avanzadas.

El sistema de menús guía al usuario a través de cada ejercicio, solicitando los parámetros necesarios como direcciones de host, números de puerto y otros configuraciones específicas. Esta aproximación interactiva es especialmente valiosa para estudiantes que están aprendiendo los conceptos por primera vez, ya que no necesitan memorizar sintaxis de línea de comandos complejas.

### Modo Línea de Comandos (Para Usuarios Avanzados)

Para usuarios más experimentados o para automatización, el programa también soporta ejecución directa mediante argumentos de línea de comandos. Algunos ejemplos incluyen:

```bash
# Escanear puertos en un host específico
python tcp_sockets_python.py scan localhost 1 100

# Conectarse a un servidor daytime
python tcp_sockets_python.py daytime time.nist.gov

# Iniciar un servidor básico en el puerto 8000
python tcp_sockets_python.py server 8000
```

Esta modalidad es útil cuando se desea integrar las funcionalidades en scripts más amplios o cuando se necesita ejecutar pruebas automatizadas.

## Ejercicios Implementados

### Ejercicios Básicos (1-4): Fundamentos de Conectividad

Los primeros cuatro ejercicios establecen los conceptos fundamentales de la programación con sockets. El **escáner de puertos** enseña cómo establecer conexiones básicas y manejar errores de conectividad. El ejercicio de **información de conexión** muestra cómo extraer metadatos importantes de las conexiones establecidas.

Los ejercicios de **cliente daytime** y **cliente echo** introducen la comunicación bidireccional y el manejo de protocolos estándar de internet. Estos ejercicios son especialmente valiosos porque conectan los conceptos teóricos con servicios reales que existen en internet.

### Ejercicios Intermedios (5-6): Arquitectura Cliente-Servidor

Los ejercicios cinco y seis marcan la transición hacia la creación de servicios propios. Aquí los estudiantes aprenden a implementar tanto el lado servidor como el lado cliente de una aplicación de red. Este es un momento crucial en el aprendizaje porque requiere pensar en ambos extremos de la comunicación simultáneamente.

### Ejercicios Avanzados (7-8): Sistemas Distribuidos

Los últimos ejercicios implementan sistemas más sofisticados que manejan múltiples clientes concurrentemente. El **sistema de mensajería** introduce conceptos de broadcasting y manejo de estado compartido, mientras que el **sistema de transferencia de archivos** enseña el manejo de datos binarios y protocolos de transferencia más complejos.

## Servidores de Prueba Locales

Una característica especialmente útil del laboratorio es la inclusión de servidores de prueba locales para los protocolos daytime y echo. Estos servidores permiten experimentar con los conceptos sin depender de servicios externos que pueden no estar disponibles o pueden tener restricciones de acceso.

Los servidores locales utilizan puertos alternativos (1313 para daytime, 1307 para echo) para evitar conflictos con servicios del sistema y eliminar la necesidad de privilegios administrativos.

## Consideraciones de Seguridad y Red

El código incluye múltiples mecanismos de manejo de errores y timeouts que enseñan buenas prácticas de programación de red. Los timeouts cortos en el escáner de puertos evitan que el programa se cuelgue en puertos que no responden, mientras que el manejo robusto de excepciones asegura que los errores de red no terminen abruptamente la ejecución.

El uso de puertos altos (superiores a 1024) en todos los servidores elimina la necesidad de ejecutar el programa con privilegios administrativos, haciendo el laboratorio más seguro y accesible.

## Herramientas de Diagnóstico

El programa incluye herramientas de diagnóstico que ayudan a identificar problemas de conectividad comunes. La función de **diagnóstico de red** verifica la conectividad básica y sugiere puertos disponibles para pruebas, mientras que la **demo automatizada** ejecuta una suite completa de pruebas para verificar que todo funciona correctamente.
