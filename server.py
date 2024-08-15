import grpc
from concurrent import futures
import subprocess
import scheduler_pb2_grpc
import scheduler_pb2
from task import Task

# Global dictionary to keep track of all submitted tasks by their task_id
tasks = {}

# The TaskSchedulerServicer class implements the gRPC service defined in scheduler.proto.
# It provides methods for submitting tasks and retrieving task statuses.
class TaskSchedulerServicer(scheduler_pb2_grpc.TaskSchedulerServicer):

    # Handles the SubmitTask RPC. Receives a TaskRequest, creates a Task object, and starts execution asynchronously.
    def SubmitTask(self, request, context):
        # Create a new task based on the incoming request's command
        task = Task(command=request.command)
        # Store the task in the global tasks dictionary, keyed by task_id
        tasks[task.task_id] = task
        print(f"Task submitted: {task.command} with ID {task.task_id}")
        # Execute the task asynchronously
        self._execute_task(task)
        # Return a TaskResponse containing the unique task_id
        return scheduler_pb2.TaskResponse(task_id=task.task_id)

    # Handles the GetTaskStatus RPC. Receives a TaskStatusRequest and returns the task's current status and output.
    def GetTaskStatus(self, request, context):
        # Retrieve the task from the global dictionary using the task_id
        task = tasks.get(request.task_id)
        # If the task is found, return its current status and output
        if task:
            return scheduler_pb2.TaskStatusResponse(
                status=task.status, output=task.output or ""
            )
        # If the task is not found, return a 'NOT_FOUND' status
        return scheduler_pb2.TaskStatusResponse(status="NOT_FOUND", output="")

    # Internal method to execute the task's command asynchronously.
    def _execute_task(self, task):
        # Function to run the shell command and capture the output
        def run_command():
            try:
                # Update task status to 'RUNNING'
                task.status = "RUNNING"
                # Run the shell command using subprocess, capturing both stdout and stderr
                result = subprocess.run(task.command, shell=True, capture_output=True, text=True)
                # Update the task's output and status upon completion
                task.output = result.stdout + result.stderr
                task.status = "COMPLETED"
            except Exception as e:
                # If an error occurs, mark the task as 'FAILED' and capture the exception message
                task.output = str(e)
                task.status = "FAILED"

        # Submit the task to a thread pool for asynchronous execution
        futures.ThreadPoolExecutor().submit(run_command)

# The serve function starts the gRPC server and listens for incoming connections.
def serve():
    # Create a gRPC server with a thread pool for handling multiple requests concurrently
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Register the TaskSchedulerServicer with the server
    scheduler_pb2_grpc.add_TaskSchedulerServicer_to_server(TaskSchedulerServicer(), server)
    # Bind the server to port 50051 for incoming connections
    server.add_insecure_port('[::]:50051')
    # Start the server and block until shutdown
    server.start()
    print("Server started on port 50051...")
    server.wait_for_termination()

# Entry point for starting the server
if __name__ == "__main__":
    serve()
