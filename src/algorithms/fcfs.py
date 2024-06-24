import time
from components.docker_utils import execute_command

# FCFS proccess implementation
class FCFS:
    def __init__(self,commands):
        self.commands = commands

        # Ordenar comandos por tiempo de inicio
        self.commands.sort(key=lambda x: x['start_time'])


    def run(self):
        start_time = time.time()
        results = []
        turnaround_times = []
        response_times = []

        for command in self.commands:
            # Esperar hasta el tiempo de inicio del comando
            while time.time() - start_time < command['start_time']:
                time.sleep(0.1)
        
            # Tiempo actual antes de ejecutar el comando
            actual_start_time = time.time()

            # Calcular el response time
            response_time = actual_start_time - start_time
            response_times.append(response_time)

            print(f"Ejecutando comando: {command['command']}")
            result = execute_command(command['command'])

            # Tiempo de finalización del comando
            finish_time = time.time()

            # Calcular el turnaround time
            turnaround_time = finish_time - actual_start_time
            turnaround_times.append(turnaround_time)

            results.append({
                'command': command['command'],
                'result': result,
                'start_time': command['start_time'],
                'estimated_time': command['estimated_time'],
                'turnaround_time': turnaround_time,
                'response_time': response_time
            })

        # Calcular promedios
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
        avg_response_time = sum(response_times) / len(response_times)

        return results, avg_turnaround_time, avg_response_time