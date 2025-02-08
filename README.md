# The-Classic-File-Transfer-Single-Client-
 How to Run and Prerequisites
1️⃣ Prerequisites
Before running the program, ensure you have:

✅ Python 3.7 or later installed. Check with:


python --version
or

python3 --version
✅ Two terminals or devices to run the server and client separately.
✅ A sample file (e.g., data.txt) available in the server's directory for transfer.
2️⃣ Running the Program
📌 Step 1: Start the Server
1️⃣ Open a terminal (Command Prompt, PowerShell, or Linux/macOS terminal).
2️⃣ Navigate to the directory containing server.py. Use:


cd /path/to/server/directory
3️⃣ Run the server:
python server.py
(or python3 server.py if python defaults to Python 2)

4️⃣ The server will start and wait for client connections:
🚀 Server listening on 127.0.0.1:65433
📌 Step 2: Start the Client
1️⃣ Open a new terminal (or use another machine).
2️⃣ Navigate to the directory containing client.py:


cd /path/to/client/directory
3️⃣ Run the client:

python client.py
4️⃣ The client will prompt you for a file name. Enter:
📂 Enter the file path to download: data.txt
3️⃣ Expected Output
✅ If Transfer is Successful:
Server Output:

🚀 Server listening on 127.0.0.1:65433
✅ Connected by ('127.0.0.1', 54321)
📂 Requested file: data.txt
📤 Sending file: data.txt (10240 bytes)
✅ Sent chunk 0 (1024 bytes)
✅ Sent chunk 1 (1024 bytes)
...
✅ Sent chunk 9 (1024 bytes)
✅ File sent successfully.
Client Output:

📂 Enter the file path to download: data.txt
📥 Receiving file as received_data.txt (10240 bytes)
✅ Received chunk 0 (1024 bytes)
✅ Received chunk 1 (1024 bytes)
...
✅ Received chunk 9 (1024 bytes)
✅ Checksum received.
🎉 Transfer Successful. Checksum verified.
4️⃣ Running on Different Machines (LAN or Remote)
If the client and server are on different machines, update server.py and client.py:

On the Server:
Find your local IP address:

ipconfig  # Windows
ifconfig  # Linux/macOS
Example output:
IPv4 Address: 192.168.1.100
Run the server with:
python server.py
On the Client:
Modify host in client.py:


start_client(host='192.168.1.100', port=65433)
Run:
python client.py
Now the client can connect to the server over LAN!

5️⃣ Troubleshooting
❌ Error: "Cannot connect to the server"
👉 Make sure the server is running before starting the client.
❌ Error: "File not found"
👉 Ensure the requested file exists in the server's directory.
❌ Error: "Checksum mismatch"
👉 The file might have been corrupted during transfer. Try again.
