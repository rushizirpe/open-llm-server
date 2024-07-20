import subprocess
import time
import argparse
import requests

def parse_arguments():
    parser = argparse.ArgumentParser(description='Manage server startup and status.')
    parser.add_argument('action', choices=['start', 'stop', 'status'], help='Action to perform: start, stop, or status')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host IP address to bind')
    parser.add_argument('--port', type=int, default=1234, help='Port number to bind')
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
        'uvicorn', 'app:app',
        '--host', host,
        '--port', str(port),
    ]
    if reload:
        uvicorn_command.append('--reload')

    subprocess.run(uvicorn_command)
    
    # subprocess.Popen(uvicorn_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # process = subprocess.Popen(uvicorn_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # output, _ = process.communicate()  # Wait for the process to complete and capture output
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

def stop_server(host, port):
    try:
        response = requests.get(f'http://{host}:{port}/shutdown')
        if response.status_code == 200:
            print("Server stopped successfully.")
        else:
            print(f"Failed to stop server. Status code: {response.status_code}")
    except requests.ConnectionError:
        print("Server is not running or could not be reached.")

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
        stop_server(args.host, args.port)
    elif args.action == 'status':
        check_server_status(args.host, args.port)
