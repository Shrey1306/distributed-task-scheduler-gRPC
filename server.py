import grpc
from concurrent import futures
import subprocess
import scheduler_pb2_grpc
import scheduler_pb2
from task import Task

tasks = {}

class TaskSchedulerServicer(scheduler_pb2_grpc.TaskSchedulerServicer):
    def SubmitTask(self, request, context):
        task = Task(command=request.command)
        tasks[task.task_id] = task
        print(f"Task submitted: {task.command} with ID {task.task_id}")
        self._execute_task(task)
        return scheduler_pb2.TaskResponse(task_id=task.task_id)

    def GetTaskStatus(self, request, context):
        task = tasks.get(request.task_id)
        if task:
            return scheduler_pb2.TaskStatusResponse(
                status=task.status, output=task.output or ""
            )
        return scheduler_pb2.TaskStatusResponse(status="NOT_FOUND", output="")

    def _execute_task(self, task):
        def run_command():
            try:
                task.status = "RUNNING"
                result = subprocess.run(task.command, shell=True, capture_output=True, text=True)
                task.output = result.stdout + result.stderr
                task.status = "COMPLETED"
            except Exception as e:
                task.output = str(e)
                task.status = "FAILED"
        
        # Run the command asynchronously
        futures.ThreadPoolExecutor().submit(run_command)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scheduler_pb2_grpc.add_TaskSchedulerServicer_to_server(TaskSchedulerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
