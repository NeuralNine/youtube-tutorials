import socket

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("<MAC address of the PC you are connecting to>", 4))

print(f"Connected!")

try:
    while True:
        message = input("Enter message: ")
        client.send(message.encode('utf-8'))
        data = client.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")

except OSError:
    pass

print("Disconnected")

client.close()
