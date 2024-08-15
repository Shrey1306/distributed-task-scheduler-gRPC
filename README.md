# Distributed Task Scheduler

## Overview
This is a distributed task scheduler system that allows clients to submit tasks to a remote server, which executes the tasks asynchronously and returns the task status and output.

### Features
- **Task Submission**: Clients can submit shell commands as tasks to be executed by the server.
- **Task Monitoring**: Clients can check the status of their submitted tasks and retrieve the output once completed.
- **gRPC**: The communication between the client and server is handled using gRPC.
- **Dataclasses**: Tasks are represented using Python's `dataclass`.
- **Unit Testing**: The project includes unit tests for the server and client components.

### Setup

1. Install dependencies:
   pip install -r requirements.txt
2. Generate gRPC files:
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. scheduler.proto
3. Run the server
    python server.py
4. Run the client
    python client.py