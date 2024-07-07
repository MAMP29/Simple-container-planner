import asyncio
import aiodocker
import docker 
import io

# function to get docker client
def get_client():
    try:
        client = docker.from_env()
        return client
    except docker.errors.DockerException as e:
        print(f"Error al obtener el cliente de Docker: {e}")
        return None

# function to create the image if not exists
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

# function to execute a command in the container
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
    create_image()
    resultado, tiempo = execute_command("ls -l")
    print("Resultado del comando: ", resultado, " Tiempo: ", tiempo)