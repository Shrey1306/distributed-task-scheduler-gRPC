import grpc
import scheduler_pb2_grpc
import scheduler_pb2

def submit_task(command):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = scheduler_pb2_grpc.TaskSchedulerStub(channel)
        response = stub.SubmitTask(scheduler_pb2.TaskRequest(command=command))
        print(f"Task submitted with ID: {response.task_id}")
        return response.task_id

def check_status(task_id):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = scheduler_pb2_grpc.TaskSchedulerStub(channel)
        response = stub.GetTaskStatus(scheduler_pb2.TaskStatusRequest(task_id=task_id))
        print(f"Task Status: {response.status}")
        print(f"Task Output: {response.output}")

if __name__ == "__main__":
    task_id = submit_task("echo Hello, World!")
    # Add a delay or check periodically in a real scenario
    check_status(task_id)
