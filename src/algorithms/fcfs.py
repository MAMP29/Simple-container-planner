import time
from utils.docker_utils import execute_command

# FCFS proccess implementation
class FCFS:
    def __init__(self, commands):
        self.commands = commands
        
        # Ordenar los comandos por tiempo de inicio
        self.commands.sort(key=lambda x: x['start_time'])

    def run(self):
        results = []
        turnaround_times = []
        response_times = []
        current_time = 0

        for command in self.commands:
            # Avanzar el tiempo hasta el inicio programado del comando
            if current_time < command['start_time']:
                current_time = command['start_time']

            # Calcular el response time (momento de inicio real menos el tiempo de inicio esperado)
            response_time = current_time - command['start_time']
            response_times.append(response_time)

            print(f"Ejecutando comando: {command['command']}")
            # Ejecutar el comando y obtener el resultado y tiempo de ejecución
            result, execution_time = execute_command(command['command'])

            # Actualizar el tiempo actual
            current_time += execution_time

            # Calcular el turnaround time (momento de finalización real menos el tiempo de inicio esperado)
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

        # Tiempo total de ejecución
        total_execution_time = current_time

        print("RESULTS OF FCFS")
        print("Results: \n", results)
        print("Turnaround times: \n", avg_turnaround_time)
        print("Response times: \n", avg_response_time)

        return results, avg_turnaround_time, avg_response_time
