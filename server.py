import socket
import hashlib
import os
import time

CHUNK_SIZE = 1024  # 1 KB chunks

def calculate_checksum(file_path):
    """Compute SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def send_file(conn, file_path):
    """Send file in chunks to the client."""
    if not os.path.exists(file_path):
        print("❌ Error: File not found!")
        conn.sendall(b"ERROR: File not found")
        return

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        print("❌ Error: The file is empty!")
        conn.sendall(b"ERROR: Empty file")
        return

    checksum = calculate_checksum(file_path)
    conn.sendall(f"{file_size}".encode().ljust(16))  # Send file size as 16-byte header

    print(f"📤 Sending file: {file_path} ({file_size} bytes)")

    try:
        with open(file_path, 'rb') as f:
            chunk_id = 0
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                conn.sendall(chunk_id.to_bytes(4, 'big') + chunk)
                print(f"✅ Sent chunk {chunk_id} ({len(chunk)} bytes)")
                chunk_id += 1
                time.sleep(0.01)  # Small delay to avoid overwhelming the network

        conn.sendall(b'END' + checksum.encode())  # Signal end of transmission
        print("✅ File sent successfully.")

    except Exception as e:
        print(f"❌ Error sending file: {e}")
        conn.sendall(b"ERROR: Unable to send file")

def start_server(host='127.0.0.1', port=65433):
    """Start the server and wait for a file request."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"🚀 Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"✅ Connected by {addr}")
                file_path = conn.recv(1024).decode().strip()
                if file_path:
                    print(f"📂 Requested file: {file_path}")
                    send_file(conn, file_path)

if __name__ == "__main__":
    start_server()
