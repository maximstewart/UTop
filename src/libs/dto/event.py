# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports



@dataclass
class Event:
    topic: str
    content: str
    raw_content: str