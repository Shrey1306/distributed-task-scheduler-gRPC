import unittest
from client import submit_task, check_status

class TestClient(unittest.TestCase):
    def test_submit_task(self):
        task_id = submit_task("echo Test")
        self.assertIsNotNone(task_id)

if __name__ == "__main__":
    unittest.main()
