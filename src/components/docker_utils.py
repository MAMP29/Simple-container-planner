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
    RUN apk add --no-cache bash
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
def execute_command(comando):
    client = get_client()

    if not client:
        return "Error: no se pudo obtener el cliente de Docker"

    try:
        container = client.containers.run(
            "planner-base:latest", 
            command=["sh", "-c", comando],
            detach=True
        )
        container.wait()
        logs = container.logs().decode('utf-8')
        container.remove()
        return logs
    except Exception as e:
        print(f"Error al ejecutar el comando '{comando}' en el contenedor: {e}")
        return f"Error al ejecutar el comando '{comando}'"

if __name__ == "__main__":
    create_image()
    resultado = execute_command("ps -ef")
    print("Resultado del comando: ", resultado)