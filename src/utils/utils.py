import os
import shlex
import subprocess
import time

# Aqui se pueden encontrar distintas funciones que sirven como soporte para el funcionamiento de la app

# Formatea el tiempo a un formato de horas, minutos y segundos, en caso de que los segundos dados sean menores a cero
# simplemente se redondean a dos decimales
def format_time(seconds):
    if seconds < 1:
        return f"{seconds:.2f} segundos"
    else:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    
# Clase para validar los comandos
class CommandValidator:
    @staticmethod
    def is_command_in_safe_directory(command_path):
        safe_directories = [
            '/bin', '/usr/bin', '/usr/local/bin',
            '/sbin', '/usr/sbin', '/usr/local/sbin',
            os.path.expanduser('~/.local/bin')  # Directorio común para comandos del usuario
        ]
        return any(command_path.startswith(directory) for directory in safe_directories)

    @staticmethod
    def validate_commands(commands):
        invalid_commands = []
        for command_data in commands:
            if not command_data['verify']:
                continue  # Saltar esta validación si 'verify' es falso
            command = command_data['command']
            command_name = shlex.split(command)[0]
            try:
                result = subprocess.run(['which', command_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if not CommandValidator.is_command_in_safe_directory(result.stdout.strip()):
                    invalid_commands.append(command)
            except subprocess.CalledProcessError:
                invalid_commands.append(command)
        return invalid_commands