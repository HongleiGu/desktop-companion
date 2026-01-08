from collections import deque
import json
from pathlib import Path

class Memory:
    def __init__(self, short_term_limit=20, long_term_path="memory.json"):
        self.short_term = deque(maxlen=short_term_limit)
        self.long_term_path = Path(long_term_path)
        self.long_term = self._load_long_term()

    def _load_long_term(self):
        if self.long_term_path.exists():
            return json.loads(self.long_term_path.read_text())
        return []

    def save_long_term(self):
        self.long_term_path.write_text(json.dumps(self.long_term, indent=2))

    def add_short(self, role, content):
        self.short_term.append({"role": role, "content": content})

    def add_long(self, summary):
        self.long_term.append(summary)
        self.save_long_term()

    def context(self):
        return list(self.short_term)

    def recall(self):
        return self.long_term[-5:]  # simple heuristic
    
    
