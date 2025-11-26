import json
import os

class Todo:
    def __init__(self, path='todo.db'):
        self.path = path
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path,'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def _save(self):
        with open(self.path,'w') as f:
            json.dump(self.tasks, f)

    def add(self, task):
        self.tasks.append({"task": task, "done": False})
        self._save()

    def list(self):
        return [t['task'] for t in self.tasks if not t['done']]

    def complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['done'] = True
            self._save()
