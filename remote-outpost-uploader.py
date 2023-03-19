import time
import queue
import paramiko
import threading
import argparse
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define global variables
queue_lock = threading.Lock()
file_queue = queue.Queue()
bandwidth_limit = None
transport = None

# Define event handler for file system events
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Add new file to queue
        with queue_lock:
            file_queue.put(event.src_path)

# Define function to upload files to remote server
def upload_file(filename):
    global transport
    try:
        if not transport:
            # Connect to remote server using SSH
            transport = paramiko.Transport(('server_address', 22))
            if key_filename:
                # Authenticate using SSH key
                key = paramiko.RSAKey.from_private_key_file(key_filename)
                transport.connect(username='username', pkey=key)
            else:
                # Authenticate using username and password
                transport.connect(username='username', password='password')
        # Open SFTP session
        sftp = transport.open_sftp()
        # Upload file
        sftp.put(filename, '/remote/path/' + filename)
        sftp.close()
        print('File uploaded successfully:', filename)
    except paramiko.ssh_exception.SSHException as e:
        # Handle network interruption
        print('Network error:', e)
        transport = None
        time.sleep(5)  # Wait for network to come back
        with queue_lock:
            file_queue.put(filename)
    except Exception as e:
        print('Error:', e)

# Define function to limit bandwidth
def limit_bandwidth():
    global bandwidth_limit
    if bandwidth_limit:
        # Limit bandwidth using tc command
        os.system('tc qdisc add dev eth0 root tbf rate ' + str(bandwidth_limit) + 'kbit burst 32kbit latency 400ms')

# Define command line arguments
parser = argparse.ArgumentParser(description='Monitor directory for new files and upload them to remote SSH server.')
parser.add_argument('directory', metavar='directory', type=str, help='Directory to monitor')
parser.add_argument('--limit', metavar='limit', type=int, help='Bandwidth limit in kbps')
parser.add_argument('--key', metavar='key', type=str, help='SSH private key file')

if __name__ == '__main__':
    # Parse command line arguments
    args = parser.parse_args()
    directory = args.directory
    bandwidth_limit = args.limit
    key_filename = args.key

    # Start bandwidth limiting thread
    if bandwidth_limit:
        t = threading.Thread(target=limit_bandwidth)
        t.daemon = True
        t.start()

    # Start file system event monitoring
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()

    # Monitor file queue and upload new files
    while True:
        if not file_queue.empty():
            filename = file_queue.get()
            upload_thread = threading.Thread(target=upload_file, args=(filename,))
            upload_thread.start()

        time.sleep(1)

    # Clean up
    observer.stop()
    observer.join()
    if transport:
        transport.close()
