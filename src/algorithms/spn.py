from collections import deque
import random
from utils.docker_utils import execute_command
import time

# SPN process implementation
class SPN:
    def __init__(self, commands, use_artificial_delay=False, min_delay=0.05, max_delay=0.15):
        self.commands = sorted(commands, key=lambda x: x['start_time'])
        self.use_artificial_delay = use_artificial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay

    def run(self):
        start_time = time.time()
        results = []
        turnaround_times = []
        response_times = []
        current_time = 0

        ready_queue = deque()
        pending_commands = deque(self.commands)

        while pending_commands or ready_queue:
            # Simular el paso del tiempo
            while pending_commands and (time.time() - start_time >= pending_commands[0]['start_time']):
                ready_queue.append(pending_commands.popleft())

            if ready_queue:
                next_command = min(ready_queue, key=lambda x: x['estimated_time'])
                ready_queue.remove(next_command)

                # Actualizar el tiempo actual
                current_time = max(current_time, next_command['start_time'])

                # Aplicar retraso artificial si está activado
                if self.use_artificial_delay:
                    artificial_delay = random.uniform(self.min_delay, self.max_delay)
                    time.sleep(artificial_delay)
                    current_time += artificial_delay

                response_time = current_time - next_command['start_time']
                response_times.append(response_time)

                result, execution_time = execute_command(next_command['command'])

                current_time += execution_time

                turnaround_time = current_time - next_command['start_time']
                turnaround_times.append(turnaround_time)

                results.append({
                    'command': next_command['command'],
                    'result': result,
                    'start_time': next_command['start_time'],
                    'estimated_time': next_command['estimated_time'],
                    'actual_execution_time': execution_time,
                    'turnaround_time': turnaround_time,
                    'response_time': response_time
                })
            else:
                if pending_commands:
                    time.sleep(0.01)  # Esperar un poco si no hay comandos listos
                else:
                    break  # Salir del bucle si no hay más comandos pendientes

        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return results, avg_turnaround_time, avg_response_time
        
