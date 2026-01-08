def get_time(_):
    from datetime import datetime
    return datetime.now().strftime("%H:%M")

def remember(text):
    return f"I will remember that: {text}"
