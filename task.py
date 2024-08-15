from dataclasses import dataclass, field
from typing import Optional
import uuid

# The Task dataclass models a task submitted to the scheduler.
# Each task is assigned a unique task_id and has a command to be executed, a status, and any output produced.

@dataclass
class Task:
    command: str            # Shell command that the task will execute
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Auto-generate a unique task ID using UUID
    status: str = "PENDING"  # Default status is 'PENDING' until the task is executed
    output: Optional[str] = None  # Placeholder for the task output, None until execution is completed
