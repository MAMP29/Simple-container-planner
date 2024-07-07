import json
import redis

from execution_results import execution_results_manager
from utils.docker_utils import create_database_container

class Connection():
    def __init__(self):
        self.connection = None

    def connect(self):
        print("Connecting to database...")
        create_database_container()
        try:
            self.connection = redis.Redis(host='localhost', port=6379, decode_responses=True)
            print("Connected to database.")
        except redis.exceptions.ConnectionError:
            print("Failed to connect to database.")
        

    def save_results(self, results):
        print("Saving results...")
        self.connection.delete("execution_results") 
        for i, result in enumerate(results):
            serialized_result = json.dumps(result)
            self.connection.lpush("execution_results", serialized_result)
        print("Results saved successfully!")
        

    def load_results(self):
        print("Loading results...")
        execution_results_manager.clear_results()
        results = self.connection.lrange("execution_results", 0, -1)
        for result in results:
            deserialized_result = json.loads(result)
            execution_results_manager.add_result(deserialized_result)
        print("Results loaded successfully!")
        return execution_results_manager.get_results()


    def clear_results(self):
        print("Deleting results...")
        self.connection.delete("execution_results")
        execution_results_manager.clear()
        print("Results deleted successfully!")

    def print_results(self):
        print("Printing results...")
        for i, result in enumerate(execution_results_manager.get_results()):
            print(f"Result {i+1}: {result}")
        print("Results printed successfully!")
        
    def delete_result_by_id(self, timestamp_id):
        print("Deleting result with timestamp_id:", timestamp_id)
        keys = self.connection.lrange("execution_results", 0, -1)
        for i, key in enumerate(keys):
            result = json.loads(key)
            if result["timestamp_id"] == timestamp_id:
                self.connection.lrem("execution_results", 1, key)
                break
        execution_results_manager.delete_result(timestamp_id)
        print("Result deleted successfully!")

db = Connection()


if __name__ == "__main__":
    db = Connection()
    db.connect()

    execution_results = []

    execution_results.append({
        "nombre": "Test",
        "algoritmo": "FCFS",
        "total_time": "00:00:10",
        "avg_turnaround_time": "00:00:05",
        "avg_response_time": "00:00:02",
        "commands": [
            {"command": "cmd1", "result": "result1", "start_time": 0, "estimated_time": 2, "turnaround_time": 2.0, "response_time": 1.0},
            {"command": "cmd2", "result": "result2", "start_time": 2, "estimated_time": 3, "turnaround_time": 3.0, "response_time": 1.5}
        ]
    })
    db.save_results()
    db.load_results()
    print(execution_results)  # Verificar que los datos se cargaron correctamente
    db.clear_results()