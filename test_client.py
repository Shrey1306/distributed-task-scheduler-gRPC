import unittest
from client import submit_task, check_status

# Unit tests for client-side task submission and status checking functionality

class TestClient(unittest.TestCase):
    # Test that a task is successfully submitted and a valid task_id is returned
    def test_submit_task(self):
        task_id = submit_task("echo Test")  # Submit a simple shell command as a task
        self.assertIsNotNone(task_id)       # Verify that a valid task_id is returned

# Entry point for running unit tests
if __name__ == "__main__":
    unittest.main()
