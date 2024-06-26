from collections import deque
from components.docker_utils import execute_command
import time

# SPN process implementation
class SPN:
    def __init__(self, commands):
        self.commands = commands


    def run(self):
        start_time = time.time()
        results = []
        turnaround_times = []
        response_times = []

        # Lista de comandos que están listos para ser ejecutados, un deque para facil acceso y manipulación
        ready_queue = deque()

        # Lista de comandos que aún no han llegado
        pending_commands = deque(self.commands)

            
        while pending_commands or ready_queue:

            # Mover comandos de pending a ready si ha llegado su tiempo de inicio
            while pending_commands and (time.time() - start_time >= pending_commands[0]['start_time']):
                ready_queue.append(pending_commands.popleft())

            if ready_queue:

                # Seleccionar el comando con el menor tiempo estimado
                next_command = min(ready_queue, key=lambda x: x['estimated_time'])
                ready_queue.remove(next_command)

                # Tiempo actual antes de ejecutar el comando
                actual_start_time = time.time()

                # Calcular el response time
                response_time = actual_start_time - start_time
                response_times.append(response_time)

                print(f"Ejecutando comando: {next_command['command']}")
                result = execute_command(next_command['command'])

                # Tiempo de finalización del comando
                finish_time = time.time()

                # Calcular el turnaround time
                turnaround_time = finish_time - actual_start_time
                turnaround_times.append(turnaround_time)


                results.append({
                    'command': next_command['command'],
                    'result': result,
                    'start_time': next_command['start_time'],
                    'estimated_time': next_command['estimated_time'],
                    'turnaround_time': turnaround_time,
                    'response_time': response_time
                })

            else:
                # Si no hay comandos listos, esperar un poco antes de reintentar
                time.sleep(0.1)
            
        # Calcular promedios
        avg_response_time = sum(response_times) / len(response_times)
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)

        return results, avg_turnaround_time, avg_response_time

        








        