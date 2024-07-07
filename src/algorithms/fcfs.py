import random
import time
from utils.docker_utils import execute_command

# FCFS proccess implementation
class FCFS:
    def __init__(self, commands, use_artificial_delay=False, min_delay=0.05, max_delay=0.15):
        self.commands = sorted(commands, key=lambda x: x['start_time'])
        self.use_artificial_delay = use_artificial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay

    def run(self):
        results = []
        turnaround_times = []
        response_times = []

        start_time = time.time()
        current_time = 0

        for command in self.commands:
            while time.time() - start_time < command['start_time']:
                time.sleep(0.01)

            current_time = max(current_time, command['start_time'])

            if self.use_artificial_delay:
                artificial_delay = random.uniform(self.min_delay, self.max_delay)
                time.sleep(artificial_delay)
                current_time += artificial_delay

            response_time = current_time - command['start_time']
            response_times.append(response_time)

            print(f"Ejecutando comando: {command['command']} a tiempo {current_time}")
            result, execution_time = execute_command(command['command'])

            current_time += execution_time

            turnaround_time = current_time - command['start_time']
            turnaround_times.append(turnaround_time)

            results.append({
                'command': command['command'],
                'result': result,
                'start_time': command['start_time'],
                'estimated_time': command['estimated_time'],
                'actual_execution_time': execution_time,
                'turnaround_time': turnaround_time,
                'response_time': response_time
            })

        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if turnaround_times else 0

        print("RESULTADOS DEL FCFS")
        print("Resultados: \n", results)
        print("Tiempo de turnaround promedio: ", avg_turnaround_time)
        print("Tiempo de respuesta promedio: ", avg_response_time)

        return results, avg_turnaround_time, avg_response_time