# Resultados de las verificaciones del despliegue

Fecha: 19 de noviembre de 2026.
Servidor: servidor-inventari.
Entorno: Ubuntu Server 24.04.5 LTS con Python 3.12.3.

## Despliegues realizados

| Verificación | v1.0.2 | v1.1.0 |
| --- | --- | --- |
| Descarga del paquete publicado en GitHub Releases | Correcta | Correcta |
| Conexión del workflow mediante Tailscale | Correcta | Correcta |
| Transferencia del ZIP al servidor por SSH | Correcta | Correcta |
| Integridad del ZIP mediante unzip -t | Sin errores | Sin errores |
| Extracción en la carpeta de la versión | Correcta | Correcta |
| Ejecución de src/producto.py en Ubuntu | Correcta | Correcta |
| Comprobaciones funcionales del despliegue | 3 satisfactorias | 3 satisfactorias |
| Activación mediante el enlace actual | Correcta | Correcta |

## Comprobaciones funcionales

1. Creación de un producto:
   Se creó un producto con código P002, nombre Mouse, precio 180
   y existencia 5. Los cuatro atributos coincidieron con lo esperado.

2. Búsqueda sin distinguir mayúsculas:
   La búsqueda de MOUSE devolvió el producto Mouse.

3. Búsqueda sin coincidencias:
   La búsqueda de Monitor devolvió una lista vacía.

Estas tres comprobaciones se ejecutaron en Ubuntu desde deploy.yml.
Son diferentes de las siete pruebas unitarias utilizadas en la liberación.

## Resultado de ejecución

Ambas versiones mostraron:

- Código: P001.
- Nombre: Teclado.
- Precio: $350.0.
- Existencia: 20.

La versión v1.1.0 mostró además el encabezado:
Sistema de Inventario v1.1.0.

## Incidencias y correcciones

### Credencial de Tailscale no disponible

El primer intento no recibió la clave de autenticación.
Se verificó y guardó TAILSCALE_AUTHKEY en los secretos del repositorio.
En el siguiente intento, la conexión a Tailscale fue satisfactoria.

### Huella SSH del servidor

La transferencia falló con el mensaje:
ssh: host key fingerprint mismatch.

Se consultaron las huellas públicas directamente en Ubuntu y se
configuró la huella ECDSA del servidor en los dos pasos SSH de deploy.yml.
Una nueva ejecución completó el despliegue correctamente.

## Simulación de falla y recuperación

Con v1.1.0 activa, se renombró el archivo instalado
src/producto.py a src/producto.py.respaldo.

La ejecución mediante la ruta actual falló con:
[Errno 2] No such file or directory.

La falla fue provocada en la copia instalada para practicar la
recuperación; no fue un defecto del paquete publicado en GitHub Releases.

Se extrajo el ZIP conservado de v1.0.2 y se comprobó su ejecución.
Después se cambió el enlace actual para apuntar a version-v1.0.2.

Resultado observado:

- Ruta activa: /home/adri/sistema-inventario/version-v1.0.2.
- Ejecución correcta del programa desde la ruta actual.
- Información del producto mostrada nuevamente.

La recuperación se realizó manualmente por SSH.
Después de recuperarla se comprobó la ejecución del programa;
no se repitieron las tres comprobaciones funcionales.

## Estado final

La versión activa al finalizar la práctica de recuperación es v1.0.2.
La versión v1.1.0 permanece publicada en GitHub Releases.
Los paquetes de ambas versiones se conservan en el servidor.

## Evidencias de respaldo

Conservar junto con este documento:

- Capturas de las ejecuciones satisfactorias de GitHub Actions.
- Registros de transferencia, ejecución y verificaciones en Ubuntu.
- Captura de la falla simulada en v1.1.0.
- Captura de la ruta activa y ejecución después de recuperar v1.0.2.
