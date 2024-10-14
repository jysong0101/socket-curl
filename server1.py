import os
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.bufsize = 1024
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()

        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)

    def createDir(self, path):
        """디렉터리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def run(self, ip, port):
        """서버 실행"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server...")
        print("\nCtrl+C for stopping the server\n")

        try:
            while True:
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(5.0)
                print("Request message...\n")

                request_data = clnt_sock.recv(self.bufsize)
                now = datetime.now()
                filename = now.strftime("%Y-%m-%d-%H-%M-%S.bin")
                with open(f"./request/{filename}", 'wb') as f:
                    f.write(request_data)
                print(f"Request saved as {filename}")

                clnt_sock.sendall(self.RESPONSE)

                clnt_sock.close()

        except KeyboardInterrupt:
            print("\nStop the server...")

        self.sock.close()

if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)
