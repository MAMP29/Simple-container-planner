import json
import redis

from execution_results import execution_results

class Connection():
    def __init__(self):
        self.connection = None

    def connect(self):
        print("Connecting to database...")
        try:
            self.connection = redis.Redis(host='localhost', port=6379, decode_responses=True)
            print("Connected to database.")
        except redis.exceptions.ConnectionError:
            print("Failed to connect to database.")
        

    # Save execution_results in the database
    def save_results(self, execution_results):
        print("Saving results...")
        self.connection.delete("execution_results")  # Clear existing data
        for i, result in enumerate(execution_results):
            serialized_result = json.dumps(result)
            self.connection.lpush("execution_results", serialized_result)
            print(f"Saved result {i}: {serialized_result}")
        print("Results saved successfully!")
        

    def load_results(self):
        global execution_results
        print("Loading results...")
        execution_results.clear()
        results = self.connection.lrange("execution_results", 0, -1)
        for result in results:
            deserialized_result = json.loads(result)
            execution_results.append(deserialized_result)
            print(f"Loaded result: {deserialized_result}")
        print("Results loaded successfully!")



    # Delete all execution_results from the database
    def clear_results(self):
        print("Deleting results...")
        self.connection.delete("execution_results")
        execution_results.clear()
        print("Results deleted successfully!")

    # Print results
    def print_results(self):
        print("Printing results...")
        for i, result in enumerate(execution_results):
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