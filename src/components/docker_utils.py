import docker 
import io

# function to get docker client
def get_client():
    return docker.from_env()

# function to create the image if not exists
def create_image():
    client = get_client()
    image_name = "planner-base:latest"

    try:
        client.images.get(image_name)
        print(f"La imagen {image_name} ya existe.")

    except docker.errors.ImageNotFound:
        print(f"La imagen {image_name} no existe. Creando...")
        dockerfile='''
        FROM alpine:latest
        RUN apk add --no-cache bash
        '''
        #build image
        client.images.build(fileobj=io.BytesIO(dockerfile.encode('utf-8')), tag=image_name)
        print(f"La imagen {image_name} ha sido creada.")

# function to execute a command in the container
def execute_command(comando):
    client = get_client()
    container = client.containers.run(
        "planner-base:latest", 
        command=["sh", "-c", comando],
        detach=True
    )
    container.wait()
    resultado = container.logs().decode('uft-8')
    container.remove()
    return resultado
