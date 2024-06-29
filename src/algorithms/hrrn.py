from utils.docker_utils import execute_command

class HRRN:
    def __init__(self, commands):
        self.commands = commands

    def calculate_response_ratio(self, waiting_time, service_time):
        return (waiting_time + service_time) / service_time

    def run(self):
        results = []
        turnaround_times = []
        response_times = []
        current_time = 0

        while self.commands:

            # Calcular los tiempos de espera
            for command in self.commands:
                command["waiting_time"] = current_time - command["start_time"]

            # Calcular el ratio de respuesta
            for command in self.commands:
                command["response_ratio"] = self.calculate_response_ratio(
                    command["waiting_time"], command["estimated_time"]
                )

            # Seleccionar el comando con el mayor radio de respuesta
            command_to_run = max(self.commands, key=lambda x: x["response_ratio"])

            # Ejecuta el comando y mide el tiempo de ejecución
            result, execution_time = execute_command(command_to_run["command"])

            if result is None:
                self.commands.remove(command_to_run)
                continue

            turnaround_time = current_time + execution_time
            response_time = current_time

            results.append({
                "command": command_to_run["command"],
                "result": result,
                "start_time": command_to_run["start_time"],
                "estimated_time": command_to_run["estimated_time"],
                "turnaround_time": turnaround_time,
                "response_time": response_time
            })

            turnaround_times.append(turnaround_time)
            response_times.append(response_time)

            current_time += execution_time

            # Remove the command from the list
            self.commands.remove(command_to_run)

        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        return results, avg_turnaround_time, avg_response_time