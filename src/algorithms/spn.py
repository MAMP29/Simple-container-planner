from collections import deque
from utils.docker_utils import execute_command
import time

# SPN process implementation
class SPN:
    def __init__(self, commands):
        self.commands = commands
        self.commands.sort(key=lambda x: x['start_time'])

    def run(self):
        start_time = time.time()
        results = []
        turnaround_times = []
        response_times = []
        current_time = 0

        # Lista de comandos que están listos para ser ejecutados, un deque para fácil acceso y manipulación
        ready_queue = deque()

        # Lista de comandos que aún no han llegado
        pending_commands = deque(self.commands)

        while pending_commands or ready_queue:
            # Mover comandos de pending a ready si ha llegado su tiempo de inicio
            while pending_commands and (current_time >= pending_commands[0]['start_time']):
                ready_queue.append(pending_commands.popleft())

            if ready_queue:
                # Seleccionar el comando con el menor tiempo estimado
                next_command = min(ready_queue, key=lambda x: x['estimated_time'])
                ready_queue.remove(next_command)

                # Avanzar el tiempo hasta el inicio programado del comando
                current_time = max(current_time, next_command['start_time'])

                # Calcular el response time
                response_time = current_time - next_command['start_time']
                response_times.append(response_time)

                print(f"Ejecutando comando: {next_command['command']}")
                result, execution_time = execute_command(next_command['command'])

                # Actualizar el tiempo actual
                current_time += execution_time

                # Calcular el turnaround time
                turnaround_time = current_time - next_command['start_time']
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
                # Si no hay comandos listos, avanzar el tiempo al siguiente comando pendiente
                if pending_commands:
                    current_time = pending_commands[0]['start_time']
                else:
                    time.sleep(0.1)

        # Calcular promedios
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return results, avg_turnaround_time, avg_response_time
        








        