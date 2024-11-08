# Simple container planner

## Requisitos
Para ejecutar SCP es aconsejable crear un entorno virtual en Python, con el fin de evitar incompatibilidades. *Es obligatorio tener Docker instalado en su dispositivo*, ya que la aplicación funciona mediante contenedores de Alpine en imágenes de Docker, al igual que la base de datos.

### Usuarios de Linux
Es necesario instalar varias librerías adicionales para hacer funcionar Flet. Consulte la [documentación oficial de Flet](https://flet.dev/docs/publish/linux/#prerequisites) para más detalles.

## Pasos de instalación
1. Crear y activar el entorno virtual de Python 
    ```
    python -m venv scp-env
    source scp-env/bin/activate
    ```
2. Clonar el repositorio
    ```
    git clone https://github.com/MAMP29/Simple-container-planner.git
    ```
3. Instalar dependencias
Es necesario que el entorno virtual cuente con las librerias utilizadas para ejecutar el programa, para ello debe de instalar las dependencias necesarias en la carpeta **requirements.txt**, simplemente mueva el archivo a la carpeta raíz del entorno, o desplácese hasta la ubicación, y ejecute el siguiente comando:
    ```
    pip install -r requirements.txt
    ```
3. Montar el contenedor de DragonflyDB
Monte el contenedor de DragonflyDB que se usará para el almacenamiento:
    ```
    docker run --name planner-database --network=host --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
    ```

Una vez montada, ya podrá ejecutar SCP, quizás la ejecución tarde unos cuantos segundos en abrirse, esto es porque debe crear la imagen de Alpine para los contenedores, es un proceso de una sola vez (a no ser que la imagen se elimine).
```
python main.py
```
