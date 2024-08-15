import unittest
from task import Task

class TestTaskScheduler(unittest.TestCase):
    def test_task_creation(self):
        task = Task(command="echo Hello, World!")
        self.assertEqual(task.status, "PENDING")
        self.assertIsNotNone(task.task_id)

if __name__ == "__main__":
    unittest.main()
