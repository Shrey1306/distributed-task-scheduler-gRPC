import grpc
import scheduler_pb2_grpc
import scheduler_pb2

# The client communicates with the task scheduler server to submit tasks and check task statuses.

# Function to submit a new task to the scheduler
def submit_task(command):
    # Establish a connection to the gRPC server running on localhost at port 50051
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub for the TaskScheduler service
        stub = scheduler_pb2_grpc.TaskSchedulerStub(channel)
        # Submit a task by sending a TaskRequest containing the shell command
        response = stub.SubmitTask(scheduler_pb2.TaskRequest(command=command))
        # Print the task_id returned by the server
        print(f"Task submitted with ID: {response.task_id}")
        return response.task_id

# Function to check the status of a submitted task by task_id
def check_status(task_id):
    # Establish a connection to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub for the TaskScheduler service
        stub = scheduler_pb2_grpc.TaskSchedulerStub(channel)
        # Request the status of the task by sending a TaskStatusRequest
        response = stub.GetTaskStatus(scheduler_pb2.TaskStatusRequest(task_id=task_id))
        # Print the current status and any output produced by the task
        print(f"Task Status: {response.status}")
        print(f"Task Output: {response.output}")

# Entry point for the client script
if __name__ == "__main__":
    # Submit a new task to the scheduler (example command: echo "Hello, World!")
    task_id = submit_task("echo Hello, World!")
    # Optionally check the task status after submission
    check_status(task_id)
