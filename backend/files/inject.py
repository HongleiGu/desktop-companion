from typing import List, Optional
from datetime import datetime
from models.files import ParsedFile
from models.message import Message
from typing import Literal
import uuid

def inject_file_context(messages: List[Message], parsed_files: List[ParsedFile]) -> List[Message]:
    # Build a single string containing all file contents
    file_texts = "\n\n".join(
        f"Filename: {file.filename}\nContent:\n{file.text}" for file in parsed_files
    )

    # Create a Pydantic Message object for the system message
    system_msg = Message(
        id=str(uuid.uuid4()),  # generate a unique ID
        role="system",
        content=f"The user provided the following files for reference:\n\n{file_texts}",
        timestamp=datetime.utcnow().isoformat(),
        name=None
    )

    # Return a new list with the system message at the front
    return [system_msg, *messages]
