# Requisitos del entorno de despliegue

## Objetivo

Desplegar el Sistema de Inventario desde un paquete publicado en
GitHub Releases hacia una máquina virtual Ubuntu mediante GitHub Actions.

## Configuración utilizada

| Componente | Configuración |
| --- | --- |
| Equipo anfitrión | Windows con 16 GB de RAM y virtualización habilitada |
| Plataforma de virtualización | Oracle VirtualBox |
| Máquina virtual | Servidor-Inventario |
| Sistema operativo de destino | Ubuntu Server 24.04.5 LTS, 64 bits |
| Recursos asignados a la VM | 4 GB de RAM, 2 CPU virtuales y disco virtual de 25 GB |
| Nombre del servidor | servidor-inventari |
| Usuario de despliegue | adri |
| Intérprete | Python 3.12.3 |

Los recursos indicados corresponden a la configuración utilizada
en la práctica; no representan mínimos medidos de la aplicación.

## Software necesario

- Python 3 para ejecutar el sistema.
- OpenSSH Server para recibir conexiones y transferencias.
- Tailscale para comunicar GitHub Actions con la máquina virtual.
- unzip para extraer y comprobar los paquetes.
- curl para realizar descargas manuales.
- Git y Git Bash en Windows para administrar el repositorio.

La aplicación utiliza la biblioteca estándar de Python.
No requiere instalar paquetes adicionales con pip.

## Conectividad y autenticación

- La máquina virtual debe estar encendida y disponer de Internet.
- SSH debe estar activo en el puerto 22 de Ubuntu.
- El servidor debe estar conectado a Tailscale.
- GitHub Actions utiliza una clave SSH autorizada para el usuario adri.
- La etiqueta tag:ci tiene acceso al puerto TCP 22 del servidor.
- Las credenciales se almacenan en los secretos de GitHub Actions.

Secretos utilizados:
DEPLOY_HOST, DEPLOY_USER, DEPLOY_PORT, DEPLOY_KEY y TAILSCALE_AUTHKEY.

## Archivos y ejecución

- Paquetes: /home/adri/sistema-inventario/paquetes/
- Versiones: /home/adri/sistema-inventario/version-<version>/
- Enlace a la versión activa: /home/adri/sistema-inventario/actual
- Comando de ejecución:
  python3 /home/adri/sistema-inventario/actual/src/producto.py

El sistema es una aplicación de consola que termina después de mostrar
la información; no requiere un servidor web ni un servicio permanente.
