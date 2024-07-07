from collections import deque
from datetime import datetime
import random
import time
import asyncio
import aiodocker
from utils.docker_utils import execute_command


class RR2Q:
    def __init__(self, commands, quantum=2, use_artificial_delay=False, min_delay=0.05, max_delay=0.15):
        self.commands = sorted(commands, key=lambda x: x['start_time'])
        self.quantum = quantum
        self.use_artificial_delay = use_artificial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay

    def run(self):
        current_time = 0
        queue = []
        results = []
        turnaround_times = []
        response_times = []
        first_response = {cmd['command']: None for cmd in self.commands}
        remaining_times = {cmd['command']: cmd['estimated_time'] for cmd in self.commands}
        
        pending_commands = self.commands[:]

        while pending_commands or queue:
            # Move arrived commands to the queue
            while pending_commands and pending_commands[0]['start_time'] <= current_time:
                queue.append(pending_commands.pop(0))

            if not queue:
                current_time = pending_commands[0]['start_time']
                continue

            command = queue.pop(0)
            
            # Apply artificial delay if enabled
            if self.use_artificial_delay:
                artificial_delay = random.uniform(self.min_delay, self.max_delay)
                time.sleep(artificial_delay)
                current_time += artificial_delay

            # Log response time for first execution of the command
            if first_response[command['command']] is None:
                first_response[command['command']] = max(0, current_time - command['start_time'])
                response_times.append(first_response[command['command']])

            # # Calculate time slice to execute
            # execution_time = min(remaining_times[command['command']], self.quantum)
            
            print(f"Ejecutando comando: {command['command']} a tiempo {current_time}")
            result, execution_time = execute_command(command['command'])
            
            remaining_times[command['command']] -= execution_time
            current_time += execution_time

            if remaining_times[command['command']] > 0:
                queue.append(command)
            else:
                turnaround_time = current_time - command['start_time']
                turnaround_times.append(turnaround_time)

                results.append({
                    'command': command['command'],
                    'result': result,
                    'start_time': command['start_time'],
                    'estimated_time': command['estimated_time'],
                    'actual_execution_time': execution_time,
                    'turnaround_time': turnaround_time,
                    'response_time': first_response[command['command']]
                })

        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        print("RESULTADOS DEL ROUND ROBIN 2Q")
        print("Resultados: \n", results)
        print("Tiempo de turnaround promedio: ", avg_turnaround_time)
        print("Tiempo de respuesta promedio: ", avg_response_time)

        return results, avg_turnaround_time, avg_response_time