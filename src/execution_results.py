
class ExecutionResultsManager:
    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def delete_result(self, timestamp_id):
        self.results = [r for r in self.results if r["timestamp_id"] != timestamp_id]

    def get_results(self):
        return self.results

    def set_results(self, new_results):
        self.results = new_results

    def clear_results(self):
        self.results.clear()

execution_results_manager = ExecutionResultsManager()