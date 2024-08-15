import unittest
from task import Task

# Unit tests for the Task dataclass and server-side functionality

class TestTaskScheduler(unittest.TestCase):
    # Test that a Task object is created correctly with default values
    def test_task_creation(self):
        task = Task(command="echo Hello, World!")
        self.assertEqual(task.status, "PENDING")  # Verify the default status is 'PENDING'
        self.assertIsNotNone(task.task_id)        # Verify that the task_id is not None

# Entry point for running unit tests
if __name__ == "__main__":
    unittest.main()
