from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class Task:
    command: str
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "PENDING"
    output: Optional[str] = None
