import random
import time
from collections import deque
from utils.docker_utils import execute_command

# SRT Process implementation 
class SRT:
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
        ready_queue = []
        pending_commands = deque(self.commands)
        current_command = None
        
        while pending_commands or ready_queue or current_command:
            current_time = time.time() - start_time

            # Mover comandos de pending a ready si ha llegado su tiempo de inicio
            while pending_commands and current_time >= pending_commands[0]['start_time']:
                command = pending_commands.popleft()
                command['remaining_time'] = command['estimated_time']
                command['first_run'] = True
                command['arrival_time'] = current_time
                ready_queue.append(command)

            # Si no hay comando actual, seleccionar el de menor tiempo restante
            if not current_command and ready_queue:
                current_command = min(ready_queue, key=lambda x: x['remaining_time'])
                ready_queue.remove(current_command)

                # Aplicar retraso artificial si está activado
                if self.use_artificial_delay:
                    artificial_delay = random.uniform(self.min_delay, self.max_delay)
                    time.sleep(artificial_delay)
                    current_time += artificial_delay

                if current_command['first_run']:
                    current_command['first_run'] = False
                    current_command['response_time'] = current_time - current_command['arrival_time']
                    response_times.append(current_command['response_time'])

            # Ejecutar el comando actual
            if current_command:
                if 'result' not in current_command:
                    print(f"Ejecutando: {current_command['command']} a tiempo {current_time}")
                    result, execution_time = execute_command(current_command['command'])
                    current_command['result'] = result
                    current_command['actual_execution_time'] = execution_time
                    current_command['remaining_time'] = 0  # El comando ha terminado
                    current_time = time.time() - start_time

                # El comando ha terminado
                turnaround_time = current_time - current_command['start_time']
                turnaround_times.append(turnaround_time)
                results.append({
                    'command': current_command['command'],
                    'result': current_command['result'],
                    'start_time': current_command['start_time'],
                    'estimated_time': current_command['estimated_time'],
                    'actual_execution_time': current_command['actual_execution_time'],
                    'turnaround_time': turnaround_time,
                    'response_time': current_command['response_time']
                })
                current_command = None

            # Si no hay nada que hacer, esperar un poco
            if not pending_commands and not ready_queue and not current_command:
                time.sleep(0.1)

        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        print("RESULTADOS DEL SRT")
        print("Resultados: \n", results)
        print("Tiempo de turnaround promedio: ", avg_turnaround_time)
        print("Tiempo de respuesta promedio: ", avg_response_time)

        return results, avg_turnaround_time, avg_response_time
    
    