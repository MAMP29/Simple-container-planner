import time
from utils.docker_utils import execute_command

# FCFS proccess implementation
class FCFS:
    def __init__(self, commands):
        self.commands = commands
        self.commands.sort(key=lambda x: x['start_time'])

    def run(self):
        start_time = time.time()
        results = []
        turnaround_times = []
        response_times = []
        current_time = 0

        for command in self.commands:
            # Avanzar el tiempo hasta el inicio programado del comando
            current_time = max(current_time, command['start_time'])

            # Calcular el response time
            response_time = current_time - command['start_time']
            response_times.append(response_time)

            print(f"Ejecutando comando: {command['command']}")
            result, execution_time = execute_command(command['command'])

            # Actualizar el tiempo actual
            current_time += execution_time

            # Calcular el turnaround time
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

        # Calcular promedios
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
        avg_response_time = sum(response_times) / len(response_times)

        total_execution_time = current_time
        return results, avg_turnaround_time, avg_response_time
