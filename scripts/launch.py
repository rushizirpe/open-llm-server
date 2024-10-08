import subprocess
import time
import argparse
import requests
import os
import signal
import platform

def parse_arguments():
    parser = argparse.ArgumentParser(description='Manage server startup and status.')
    parser.add_argument('action', choices=['start', 'stop', 'status'], help='Action to perform: start, stop, or status')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host IP address to bind')
    parser.add_argument('--port', type=int, default=8888, help='Port number to bind')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (for start)')
    return parser.parse_args()

def start_server(host, port, reload):
    print("Server is Starting Up...")
    try:
        requests.get(f'http://{host}:{port}')
        print("Server is already running.")
        return
    except requests.ConnectionError:
        pass

    uvicorn_command = [
        'uvicorn', 'src.main:app',
        '--host', host,
        '--port', str(port),
    ]
    if reload:
        uvicorn_command.append('--reload')
        
    # Define log file path
    log_file = 'server.log'
    pid_file = 'server.pid'

    with open(log_file, 'a') as log:
        process = subprocess.Popen(
            uvicorn_command,
            stdout=log,
            stderr=log
        )
        with open(pid_file, 'w') as pid:
            pid.write(str(process.pid))

        
    timer = 0
    while timer < 600:
        try:
            requests.get(f'http://{host}:{port}')
        except requests.ConnectionError:
            time.sleep(1)
            timer += 1
            print(f"Elapsed Time: {timer} seconds", end="\r")
        else:
            print("\nServer started successfully.")
            return

    print("Error: Server startup timed out. Took more than 10 minutes.")

def stop_server():
    current_os = platform.system()
    try:
        if os.path.exists("server.pid"):
            with open("server.pid", 'r') as pid_file:
                pid = int(pid_file.read().strip())
                print(f"Found server process with PID: {pid} via server.pid file. Stopping the server...")
                if current_os == "Windows":
                    subprocess.run(["taskkill", "/PID", pid, "/F"])
                else:
                    os.kill(int(pid), signal.SIGTERM)

                print("Server stopped successfully.")
                return

        if current_os == "Windows":
            print("Searching for running Python processes on Windows system...")
            result = subprocess.run(
                ['tasklist', '/FO', 'CSV'],
                capture_output=True,
                text=True
            )
        else:
            print(
                "Searching for running Python processes on Unix-like system..."
            )
            result = subprocess.run(
                ["ps", "-aux"], capture_output=True, text=True
            )

        if result.returncode != 0:
            print("Error executing tasklist command.")
            return

        processes = result.stdout.splitlines()
        
        for line in processes:
            if "python" in line and "uvicorn" in line:
                if current_os == "Windows":
                    pid = line.split(",")[1].strip('"')
                else:
                    pid = line.split()[1]

                print(f"Found Python process with PID: {pid}. Stopping the server...")

                if current_os == "Windows":
                    subprocess.run(["taskkill", "/PID", pid, "/F"])
                else:
                    os.kill(int(pid), signal.SIGTERM)

                print("Server stopped successfully.")
                return
        
        print("No running Python server process found.")
        
    except Exception as e:
        print(f"An error occurred while trying to stop the server: {e}")

def check_server_status(host, port):
    try:
        response = requests.get(f'http://{host}:{port}')
        if response.status_code == 200:
            print("Server is running.")
        else:
            print(f"Server returned status code: {response.status_code}")
    except requests.ConnectionError:
        print("Server is not running or could not be reached.")

def main():
    args = parse_arguments()

    if args.action == 'start':
        start_server(args.host, args.port, args.reload)
    elif args.action == 'stop':
        stop_server()
    elif args.action == 'status':
        check_server_status(args.host, args.port)

if __name__ == '__main__':
    main()