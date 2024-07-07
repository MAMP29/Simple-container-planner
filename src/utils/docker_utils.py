import asyncio
import aiodocker
import docker 
import io

# Funcion para obtener el docker client
def get_client():
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        print(f"Error al obtener el cliente de Docker: {e}")
        return None

# Funcion para crear la imagen para las ejecuciones, en caso de no existir
def create_image():
    client = get_client()

    if not client:
        return 

    image_name = "planner-base:latest"

    dockerfile = '''
    FROM alpine:latest
    RUN apk update && apk add --no-cache stress-ng coreutils
    CMD ["/bin/sh"]
    '''
        
    try:
        client.images.get(image_name)
        print(f"La imagen {image_name} ya existe.")

    except docker.errors.ImageNotFound:
        print(f"La imagen {image_name} no existe. Creando...")
       
        try:
            #build image
            client.images.build(fileobj=io.BytesIO(dockerfile.encode('utf-8')), tag=image_name)
            print(f"La imagen {image_name} ha sido creada.")
        
        except Exception as e:
            print(f"Error al crear la imagen {image_name}: {e}")

def create_database_container():
    client = get_client()

    if not client:
        return
        
    container_name = "planner-database"
    image_name = "docker.dragonflydb.io/dragonflydb/dragonfly"

    # Verifica si el contenedor ya está en ejecución
    try:
        container = client.containers.get(container_name)
        if container.status == 'running':
            print(f"El contenedor {container_name} ya está en funcionamiento.")
            return
        else:
            container.start()
            print(f"El contenedor {container_name} ha sido iniciado.")
            return
    except docker.errors.NotFound:
        print(f"El contenedor {container_name} no existe. Creando y ejecutando...")
        
    # Iniciar el contenedor
    try:
        client.containers.run(
            image_name,
            name=container_name,
            network_mode="host",
            ulimits=[docker.types.Ulimit(name="memlock", soft=-1, hard=-1)],
            detach=True
        )
        print(f"El contenedor {container_name} ha sido creado y ejecutado.")
    except Exception as e:
        print(f"Error al crear el contenedor {container_name}: {e}")


def stop_database_container():
    client = get_client()

    if not client:
        return

    container_name = "planner-database"

    # Verifica si el contenedor ya está en ejecución para detenerlo
    try:
        container = client.containers.get(container_name)
        if container.status == 'running':
            container.stop()
            print(f"El contenedor {container_name} ha sido detenido.")
        else:
            print(f"El contenedor {container_name} no está en funcionamiento.")

    except docker.errors.NotFound:
        print(f"El contenedor {container_name} no existe.")

    except Exception as e:
        print(f"Error al detener el contenedor {container_name}: {e}")
    

# Función para ejecutar el comando en el contenedor
async def execute_command_async(comando, max_log_size=1024*1024):
    async with aiodocker.Docker() as docker:
        config = {
            "Image": "planner-base:latest",
            "Cmd": ["sh", "-c", comando],
            "AttachStdout": True,
            "AttachStderr": True,
        }
        container = await docker.containers.create(config=config)
        await container.start()
        
        start_time = asyncio.get_event_loop().time()
        
        logs = []
        log_size = 0
        truncated = False
        async for log in container.log(stdout=True, stderr=True, follow=True):
            log_size += len(log)
            if log_size > max_log_size:
                if not truncated:
                    logs.append("\n... [Log truncado debido al tamaño] ...")
                    truncated = True
            else:
                logs.append(log)


        result = "".join(logs)
        
        await container.wait()
        end_time = asyncio.get_event_loop().time()
        
        await container.delete(force=True)
        
        execution_time = end_time - start_time
        return result, execution_time

def execute_command(comando):
    async def run():
        return await execute_command_async(comando)
    return asyncio.run(run())

if __name__ == "__main__":
    # create_image()
    # resultado, tiempo = execute_command("ls -l")
    # print("Resultado del comando: ", resultado, " Tiempo: ", tiempo)
    create_database_container()