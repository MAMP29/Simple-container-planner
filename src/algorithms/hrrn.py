import random
import time
from utils.docker_utils import execute_command

class HRRN:
    def __init__(self, commands, use_artificial_delay=False, min_delay=0.05, max_delay=0.15):
        self.commands = sorted(commands, key=lambda x: x['start_time'])
        self.use_artificial_delay = use_artificial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay

    def calculate_response_ratio(self, waiting_time, service_time):
        return (waiting_time + service_time) / service_time

    def run(self):
        results = []
        turnaround_times = []
        response_times = []
        current_time = 0

        ready_queue = []

        while self.commands or ready_queue:
            # Mover comandos a la cola de listos si han llegado
            while self.commands and self.commands[0]['start_time'] <= current_time:
                ready_queue.append(self.commands.pop(0))

            if ready_queue:
                # Calcular ratios de respuesta
                for command in ready_queue:
                    waiting_time = current_time - command['start_time']
                    command['response_ratio'] = self.calculate_response_ratio(waiting_time, command['estimated_time'])

                # Seleccionar el comando con el mayor ratio de respuesta
                command_to_run = max(ready_queue, key=lambda x: x['response_ratio'])
                ready_queue.remove(command_to_run)

                # Aplicar retraso artificial si está activado
                if self.use_artificial_delay:
                    artificial_delay = random.uniform(self.min_delay, self.max_delay)
                    time.sleep(artificial_delay)
                    current_time += artificial_delay

                # Calcular el response time
                response_time = current_time - command_to_run['start_time']
                response_times.append(response_time)

                result, execution_time = execute_command(command_to_run['command'])

                current_time += execution_time
                turnaround_time = current_time - command_to_run['start_time']
                turnaround_times.append(turnaround_time)

                results.append({
                    'command': command_to_run['command'],
                    'result': result,
                    'start_time': command_to_run['start_time'],
                    'estimated_time': command_to_run['estimated_time'],
                    'actual_execution_time': execution_time,
                    'turnaround_time': turnaround_time,
                    'response_time': response_time
                })
            else:
                # Si no hay comandos listos, avanzar el tiempo
                if self.commands:
                    current_time = self.commands[0]['start_time']
                else:
                    break

        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return results, avg_turnaround_time, avg_response_time