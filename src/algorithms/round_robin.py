from collections import deque
from datetime import datetime
import time
import asyncio
import aiodocker
from utils.docker_utils import execute_command


class RR2Q:
    def __init__(self, commands, quantum=2):
        self.commands = commands
        self.quantum = quantum

    async def run_command(self, command):
        async with aiodocker.Docker() as docker:
            config = {
                "Image": "planner-base:latest",
                "Cmd": ["sh", "-c", command],
                "AttachStdout": True,
                "AttachStderr": True,
            }
            container = await docker.containers.create(config=config)
            await container.start()

            start_time = asyncio.get_event_loop().time()
            execution_time = 0
            logs = []

            while True:
                chunk_start = asyncio.get_event_loop().time()
                try:
                    async for log in container.log(stdout=True, stderr=True, follow=True, until=chunk_start + self.quantum):
                        logs.append(log)
                except asyncio.TimeoutError:
                    pass

                execution_time += self.quantum
                if execution_time >= self.quantum:
                    break

            result = "".join(logs)
            await container.wait()
            await container.delete(force=True)
            end_time = asyncio.get_event_loop().time()

            turnaround_time = end_time - start_time
            return result, turnaround_time, execution_time

    def run(self):
        results = []
        total_turnaround_time = 0
        total_response_time = 0
        turnaround_times = []
        response_times = []

        for command in self.commands:
            result, turnaround_time, execution_time = asyncio.run(self.run_command(command['command']))
            total_turnaround_time += turnaround_time
            total_response_time += execution_time
            turnaround_times.append(turnaround_time)
            response_times.append(execution_time)
            results.append({
                'command': command['command'],
                'result': result,
                'start_time': command['start_time'],
                'estimated_time': command['estimated_time'],
                'turnaround_time': turnaround_time,
                'response_time': execution_time
            })

        avg_turnaround_time = total_turnaround_time / len(self.commands)
        avg_response_time = total_response_time / len(self.commands)

        return results, avg_turnaround_time, avg_response_time