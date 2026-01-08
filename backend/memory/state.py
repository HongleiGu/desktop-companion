class AgentState:
    def __init__(self):
        self.mood = "calm"
        self.affinity = 0.0  # relationship metric

    def update_from_text(self, text: str):
        if "thank" in text.lower():
            self.affinity += 0.1
            self.mood = "happy"

    def describe(self):
        return f"Mood: {self.mood}, Affinity: {self.affinity:.2f}"
