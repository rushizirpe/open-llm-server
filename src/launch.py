import subprocess
import time
import argparse
import requests
import os
import signal

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
        'uvicorn', 'src.app:app',
        '--host', host,
        '--port', str(port),
    ]
    if reload:
        uvicorn_command.append('--reload')
        
    # uvicorn_command.append(">/dev/null")
    # subprocess.run(uvicorn_command)
    process = subprocess.Popen(
        uvicorn_command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # process = subprocess.Popen(uvicorn_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Wait for the process to complete and capture output
    # output, _ = process.communicate()  
    # if process.returncode != 0:
    #     print(f"Server startup error: {output.decode('utf-8')}")
    
    timer = 0
    while timer < 600:
        try:
            requests.get(f'http://{host}:{port}')
        except requests.ConnectionError:
            time.sleep(1)
            timer += 1
            print(f"Elapsed Time: {timer} seconds", end = "\r")
        else:
            print("Server started successfully.")
            return

    print("Error: Server startup timed out. Took more than 10 minutes.")

def stop_server():
    try:
        # Find the PID of the Python process running the server
        print("Searching for running Python processes...")
        result = subprocess.run(
            ['tasklist', '/FO', 'CSV'],
            capture_output=True,
            text=True
        )

        # Check if the command executed successfully
        if result.returncode != 0:
            print("Error executing tasklist command.")
            return

        # Split the output into lines
        processes = result.stdout.splitlines()
        
        # Look for the python process running the server
        for line in processes:
            if 'python.exe' in line:
                # Extract PID from the CSV format
                pid = line.split(',')[1].strip('"')
                print(f"Found Python process with PID: {pid}. Stopping the server...")
                
                # Kill the process
                subprocess.run(['taskkill', '/PID', pid, '/F'])
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

if __name__ == '__main__':
    args = parse_arguments()

    if args.action == 'start':
        start_server(args.host, args.port, args.reload)
    elif args.action == 'stop':
        stop_server()
    elif args.action == 'status':
        check_server_status(args.host, args.port)
