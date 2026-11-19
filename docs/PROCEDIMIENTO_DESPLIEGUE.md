# Procedimiento de despliegue y recuperación

Fecha de la práctica: 19 de noviembre de 2026.

Repositorio:
https://github.com/adrideveloper080/sistema-inventario

## 1. Identificar la versión publicada

Consultar GitHub Releases y seleccionar el paquete generado por
release.yml, con nombre sistema-inventario-<version>.zip.

En esta práctica se utilizaron:

| Versión | Commit de la versión | Paquete |
| --- | --- | --- |
| v1.0.2 | ab2c469 | sistema-inventario-v1.0.2.zip |
| v1.1.0 | e327cbc | sistema-inventario-v1.1.0.zip |

La liberación ejecuta pruebas y publica el paquete.
El despliegue descarga ese paquete existente y lo instala en Ubuntu.

## 2. Preparar la máquina de destino

En Windows se creó la máquina virtual Servidor-Inventario mediante
VirtualBox, con 4 GB de RAM, 2 CPU virtuales y disco virtual de 25 GB.

Se instaló Ubuntu Server 24.04.5 LTS y se creó el usuario adri.
El nombre del servidor quedó como servidor-inventari.

En Ubuntu se prepararon las herramientas:

```bash
sudo apt update
sudo apt install openssh-server curl unzip
sudo systemctl enable --now ssh
systemctl is-active ssh
python3 --version
```

Resultados observados: SSH activo y Python 3.12.3 disponible.

## 3. Acceder desde Windows por SSH

Se configuró una regla NAT de VirtualBox:
127.0.0.1:2222 en Windows hacia el puerto 22 de Ubuntu.

Con la VM encendida, la regla se agregó desde Git Bash de Windows:

```bash
"/c/Program Files/Oracle/VirtualBox/VBoxManage.exe" controlvm "Servidor-Inventario" natpf1 "ssh,tcp,127.0.0.1,2222,,22"
```

Esta regla se crea una sola vez; no se repite si ya existe.

Para iniciar sesión desde Git Bash de Windows:

```bash
ssh -p 2222 adri@127.0.0.1
```

Después de iniciar sesión, los comandos escritos en esa terminal
se ejecutan en Ubuntu.

## 4. Comprobar manualmente el paquete

En Ubuntu se descargó y comprobó v1.0.2:

```bash
mkdir -p ~/sistema-inventario
cd ~/sistema-inventario
curl -fL -o sistema-inventario-v1.0.2.zip https://github.com/adrideveloper080/sistema-inventario/releases/download/v1.0.2/sistema-inventario-v1.0.2.zip
unzip -t sistema-inventario-v1.0.2.zip
unzip sistema-inventario-v1.0.2.zip -d version-v1.0.2
python3 version-v1.0.2/src/producto.py
```

La ejecución mostró los datos del producto correctamente.

## 5. Conectar Ubuntu a Tailscale

En Ubuntu:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Se abrió el enlace de autenticación en el navegador de Windows,
utilizando la cuenta de GitHub adrideveloper080.

Después se comprobó la conexión:

```bash
tailscale status
```

El servidor recibió la IP de Tailscale 100.120.63.115.

En los controles de acceso se definió tag:ci, administrada por
autogroup:admin, y se permitió a esa etiqueta acceder únicamente
al puerto TCP 22 de 100.120.63.115.
Se conservó el acceso de los dispositivos asociados a los usuarios.

Para el workflow se generó una clave de autenticación reutilizable,
efímera, con tag:ci y caducidad de siete días.
Cuando expire, deberá generarse otra y actualizar su secreto en GitHub.

## 6. Preparar la autenticación SSH

En Git Bash de Windows se generó una clave dedicada, sin contraseña
de paso para permitir su uso automático:

```bash
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -C "github-actions-inventario" -f ~/.ssh/inventario_deploy
ssh-copy-id -i ~/.ssh/inventario_deploy.pub -p 2222 adri@127.0.0.1
```

Estos comandos de generación se realizan durante la preparación;
no es necesario generar una clave nueva para cada despliegue.

Se comprobó el acceso con la clave:

```bash
ssh -i ~/.ssh/inventario_deploy -o IdentitiesOnly=yes -o PasswordAuthentication=no -p 2222 adri@127.0.0.1 "whoami && hostname"
```

El servidor respondió con adri y servidor-inventari.

## 7. Configurar los secretos de GitHub Actions

En el repositorio se abrió:
Settings → Secrets and variables → Actions → New repository secret.

| Nombre | Contenido |
| --- | --- |
| DEPLOY_HOST | IP de Tailscale del servidor |
| DEPLOY_USER | adri |
| DEPLOY_PORT | 22 |
| DEPLOY_KEY | Clave privada SSH dedicada |
| TAILSCALE_AUTHKEY | Clave de autenticación de Tailscale |

Las claves privadas y de autenticación se guardaron como secretos.
No deben incorporarse al código, a capturas ni a documentos.

GitHub Actions accede por Tailscale al puerto 22.
El puerto 2222 se utiliza para el acceso local desde Windows.

## 8. Verificar la identidad del servidor

En Ubuntu se consultaron las huellas de las claves públicas:

```bash
for archivo in /etc/ssh/ssh_host_*_key.pub; do ssh-keygen -lf "$archivo" -E sha256; done
```

Se configuró la huella ECDSA verificada en los dos campos
fingerprint de deploy.yml:

SHA256:qyyl5t+SJPrT4RXsVQxG8BJ2cGlI01ZCt4InUotwBnk

Esto corrigió el error de discrepancia de huella observado
durante la primera transferencia.

## 9. Configurar el workflow de despliegue

El archivo versionado es .github/workflows/deploy.yml.

Se activa manualmente mediante workflow_dispatch y permite
seleccionar la versión publicada.

El workflow realiza estas operaciones:

1. Descarga el ZIP correspondiente desde GitHub Releases.
2. Comprueba el ZIP y muestra su SHA-256.
3. Conecta el ejecutor de GitHub Actions a Tailscale.
4. Transfiere el ZIP por SSH a la carpeta paquetes de Ubuntu.
5. Comprueba y extrae el paquete en version-<version>.
6. Ejecuta src/producto.py en Ubuntu.
7. Ejecuta tres comprobaciones funcionales.
8. Si los pasos anteriores terminan correctamente, actualiza el
   enlace actual para apuntar a la versión desplegada.

El ZIP no se vuelve a generar durante el despliegue.
Las carpetas de otras versiones y los paquetes se conservan.

## 10. Ejecutar y comprobar el despliegue

Mantener Windows conectado a Internet y la máquina virtual encendida.

En GitHub:

1. Abrir Actions → Despliegue del Sistema de Inventario.
2. Pulsar Run workflow.
3. Seleccionar main y la versión publicada.
4. Iniciar la ejecución.
5. Revisar el trabajo desplegar y sus registros.

Primero se desplegó v1.0.2 y después v1.1.0.
Ambas ejecuciones completaron las tres comprobaciones funcionales.

En Ubuntu se puede comprobar la versión activa:

```bash
readlink -f ~/sistema-inventario/actual
python3 ~/sistema-inventario/actual/src/producto.py
ls -lh ~/sistema-inventario/paquetes/
```

## 11. Simular un problema en la versión nueva

Este paso corresponde exclusivamente al ejercicio controlado.

Después de confirmar que actual apuntaba a version-v1.1.0,
se renombró el archivo principal de esa copia instalada:

```bash
mv -n ~/sistema-inventario/version-v1.1.0/src/producto.py ~/sistema-inventario/version-v1.1.0/src/producto.py.respaldo
python3 ~/sistema-inventario/actual/src/producto.py
```

La ejecución falló con No such file or directory.
Los paquetes originales permanecieron intactos.

## 12. Recuperar la versión anterior

En Ubuntu se recuperó v1.0.2 desde el ZIP conservado:

```bash
unzip -o ~/sistema-inventario/paquetes/sistema-inventario-v1.0.2.zip -d ~/sistema-inventario/version-v1.0.2
python3 ~/sistema-inventario/version-v1.0.2/src/producto.py
```

Después de comprobar que funcionaba, se activó:

```bash
ln -sfn ~/sistema-inventario/version-v1.0.2 ~/sistema-inventario/actual
readlink -f ~/sistema-inventario/actual
python3 ~/sistema-inventario/actual/src/producto.py
```

La ruta activa volvió a version-v1.0.2 y el programa mostró
los datos del producto correctamente.

La recuperación fue manual por SSH. No implicó modificar
las etiquetas ni eliminar las versiones de GitHub Releases.

## 13. Conservar las evidencias

Guardar capturas y registros de:

- Release seleccionada y paquete descargado.
- Preparación y configuración de Ubuntu.
- Workflow de despliegue satisfactorio.
- Transferencia del paquete al servidor.
- Ejecución y comprobaciones funcionales.
- Falla simulada en v1.1.0.
- Activación y ejecución de v1.0.2 después de recuperarla.

Documentos complementarios:

- [Requisitos del entorno](REQUISITOS_ENTORNO.md).
- [Resultados de las verificaciones](RESULTADOS_VERIFICACIONES.md).
