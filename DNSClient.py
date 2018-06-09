import socket
from Message import DNSMessageFormat


class DNSClient:
    def __init__(self, server="8.8.8.8"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self.connectServer(server)

    def connectServer(self, server):
        try:
            self.socket.connect((server, 53))
        except Exception:
            print("kết nối thất bại!")
            return False
        self.server = server
        return True

    def sendQuery(self, request,type):
        message = DNSMessageFormat()
        query = message.encode(request, type)
        self.socket.send(query)
        try:
            responce = self.socket.recv(1024)
        except Exception:
            print("Không phản hồi!")
            exit(0)
        message.decode(responce)

        if len(message.answers) > 0:
            message.print_result()
        else:
            print("Không xác định")
            
    def disconnect(self):
        self.socket.close()


if __name__ == "__main__":
    choice = 0
    type = 0
    while( True ):
        print()
        print("Nhập vào lựa chọn của bạn")
        print("1: Phân giải tên miền thành địa chỉ IP")
        print("2: Phân giải địa chỉ IP thành tên miền")
        print("3: Thoát")
        try:
            choice = int(input())
        except Exception:
            print("Bạn phải nhập vào một số nguyên từ 1 đến 3")
        if choice == 1:
            type = 1
            client = DNSClient()
            domain = input("Nhập vào tên miền: ")
            client.sendQuery(domain, type)
        elif choice == 2:
            type = 12
            client = DNSClient()
            domain = input("Nhập vào địa chỉ IP: ")
            client.sendQuery(domain, type)
        elif choice == 3:
            print("BYE BYE!")
            client.disconnect()
            break
    