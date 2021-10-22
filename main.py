from client import Client
from server import Server

if __name__ == '__main__':
    server = Server("Apple")
    c1 = Client(1, server)
    c2 = Client(2, server)

    server.show_clients()
    c1.send_voucher(str(500))
