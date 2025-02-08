import socket
import hashlib
import os

CHUNK_SIZE = 1024  # 1 KB chunks

def calculate_checksum(file_path):
    """Compute SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def receive_file(client_socket, file_path):
    """Receive file in chunks and verify integrity."""
    chunks = {}
    expected_checksum = None

    # Receive file size from the server (16-byte fixed header)
    file_size_data = client_socket.recv(16).decode().strip()
    if not file_size_data.isdigit():
        print("❌ Error: Invalid file size received.")
        return

    file_size = int(file_size_data)
    print(f"📥 Receiving file as {file_path} ({file_size} bytes)")

    received_size = 0
    while received_size < file_size:
        data = client_socket.recv(4 + CHUNK_SIZE)
        if len(data) < 4:  # Ensure we received at least chunk ID
            print("❌ Error: Received incomplete chunk header.")
            break

        chunk_id = int.from_bytes(data[:4], 'big')
        chunk_data = data[4:]

        if len(chunk_data) == 0:
            print(f"❌ Received an empty chunk {chunk_id}, stopping transfer.")
            break

        chunks[chunk_id] = chunk_data
        received_size += len(chunk_data)
        print(f"✅ Received chunk {chunk_id} ({len(chunk_data)} bytes)")

    # Receiving checksum
    data = b""
    while True:
        part = client_socket.recv(1024)
        if not part:
            break
        data += part
        if data.startswith(b'END'):
            expected_checksum = data[3:].decode()
            print("✅ Checksum received.")
            break

    if not chunks:
        print("❌ No data received, transfer failed.")
        return

    # Reassemble the file
    with open(file_path, 'wb') as f:
        for chunk_id in sorted(chunks.keys()):
            f.write(chunks[chunk_id])

    # Verify checksum
    actual_checksum = calculate_checksum(file_path)

    if actual_checksum == expected_checksum:
        print("🎉 Transfer Successful. Checksum verified.")
    else:
        print("❌ Transfer Failed. Checksum mismatch.")

def start_client(host='127.0.0.1', port=65433):
    """Start the client and request a file."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            file_path = input("📂 Enter the file path to download: ").strip()
            client_socket.sendall(file_path.encode())

            received_file_path = 'received_' + os.path.basename(file_path)
            receive_file(client_socket, received_file_path)

        except ConnectionRefusedError:
            print("❌ Error: Cannot connect to the server. Make sure the server is running.")

if __name__ == "__main__":
    start_client()
