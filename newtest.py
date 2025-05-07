# import socket
# import time
# from pyModbusTCP.client import ModbusClient  # thư viện modbus client

# HOST = "192.168.1.10"  # IP robot
# PORT = 30001  # Port gửi
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Khởi tạo giao tiếp
# s.connect((HOST, PORT))  # Gửi yêu cầu kết nối
# time.sleep(1)
# f = open(
#     "Test_send_program_to_UR/a.script", "rb"
# )  # Mở chương trình script đã tạo trước đó
# l = f.read(4096)  # Đọc chương trình, lưu vào biến l
# s.sendall(l)  # Gửi chương trình cho robot
# # Khởi tạo Modbus client
# modbus_client = ModbusClient(host="192.168.1.10", port=502)

# try:
#     while True:
#         a = modbus_client.read_input_registers(
#             128, 3
#         )  # Đọc thanh ghi từ 128(vị trí X) đến 130(vị trí Z) (3 thanh ghi)
# finally:
#     # Đóng kết nối Modbus khi chương trình kết thúc
#     modbus_client.close()


# server.py

import socket
import time

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
host_server = "192.168.1.90"  # IP của PC
host_send = "192.168.1.10"  # IP robot
port_server = 41234  # Port server
port_send = 30002  # Port gữi


# =======================Gửi chương trình==============================#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Khởi tạo giao tiếp
# s.connect((host_send, port_send))  # Gửi yêu cầu kết nối
# time.sleep(1)
# f = open(
#     "Test_send_program_to_UR/a.script", "rb"
# )  # Mở chương trình script đã tạo trước đó
# l = f.read(4096)  # Đọc chương trình, lưu vào biến l
# s.sendall(l)  # Gửi chương trình cho robot
# time.sleep(1)
# ======================Đọc giá trị trả về====================#
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Khởi tạo giao tiếp
s1.bind((host_server, port_server))  # Khởi tạo server
s1.listen(1)  # 1 ở đây có nghĩa chỉ chấp nhận 1 kết nối
print("Server listening on port", port_server)

c, addr = s1.accept()  # Chấp nhận kết nối
print("Connect from ", str(addr))

while True:
    data = c.recv(4096)
    print(data)
    time.sleep(0.01)
c.close()
