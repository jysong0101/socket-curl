import os
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.bufsize = 1024 * 10
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()

        self.DIR_PATH = './request'
        self.IMAGE_PATH = './images'
        self.createDir(self.DIR_PATH)
        self.createDir(self.IMAGE_PATH)

    def createDir(self, path):
        """디렉터리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def save_image(self, data, boundary):
        """멀티파트 이미지 데이터 처리 후 저장"""
        boundary = boundary.encode('utf-8')
        parts = data.split(boundary)
        for part in parts:
            if b"Content-Type: image/" in part:
                image_data = part.split(b'\r\n\r\n')[1].split(b'\r\n--')[0]
                now = datetime.now()
                image_filename = now.strftime("%Y-%m-%d-%H-%M-%S.jpg")
                with open(f"{self.IMAGE_PATH}/{image_filename}", 'wb') as f:
                    f.write(image_data)
                print(f"Image saved as {image_filename}")

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
                clnt_sock.settimeout(10.0)
                print("Request message...\n")

                request_data = b""
                try:
                    while True:
                        chunk = clnt_sock.recv(self.bufsize)
                        if not chunk:
                            break
                        request_data += chunk
                except socket.timeout:
                    print("Receive timeout, stopping data collection.")
                
                now = datetime.now()
                filename = now.strftime("%Y-%m-%d-%H-%M-%S.bin")
                with open(f"./request/{filename}", 'wb') as f:
                    f.write(request_data)
                print(f"Request saved as {filename}")

                boundary = request_data.split(b'boundary=')[1].split(b'\r\n')[0].decode('utf-8')

                self.save_image(request_data, boundary)

                clnt_sock.sendall(self.RESPONSE)

                clnt_sock.close()

        except KeyboardInterrupt:
            print("\nStop the server...")

        self.sock.close()

if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)
