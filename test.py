import socket
import time
from Test_extract_robot_message.unpack_robot_msgs import Unpackage
from Test_extract_robot_message.unpack_ur_primary_msg import *

HOST = "192.168.1.120"
PORT = 30001
print("Starting program")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
time.sleep(1)
# f = open("F:/Py program/VSCode/Test_send_program_to_UR/test.script", "rb")
# l = f.read(4096)
# print(l)
# s.sendall(l)
print("End program")


# dataHEX = data.hex()
# totalsize = dataHEX[0:8]
# datatype = dataHEX[8:10]
# # check if the msg type is MESSAGE_TYPE_ROBOT_MESSAGE
# # if int(datatype, 16) == 20:
# #     msgType_2 = dataHEX[28:30]
# #     print(f"raw data：{dataHEX}")
# # Process and print data
# # print("Received:", data.decode("windows-1252"))

a = None
b = None
c = None
d = None
e = None
f = None
while True:
    data = s.recv(4096)
    unpack = unpackege(data)
    # if unpack.type == 16:

    #     print(unpack.ROBOT_MODE_DATA.isProgramRunning)
    #     print(unpack.JOINT_DATA.q_actual)
    #     # t = unpack.RobotModeData.
    #     # print("timestamp=", t)
    # elif unpack.type == 20:
    #     print(unpack.source_data)
    #     print(unpack.VERSION_MESSAGE.projectNameSize)
    #     print(unpack.VERSION_MESSAGE.projectName)
    #     print(unpack.VERSION_MESSAGE.majorVersion)
    #     print(unpack.VERSION_MESSAGE.minorVersion)
    #     print(unpack.VERSION_MESSAGE.bugfixVersion)
    #     print(unpack.VERSION_MESSAGE.buildNumber)
    #     print(unpack.VERSION_MESSAGE.buildDate)
    #     break
    # elif unpack.type == 25:

    # if unpack.type == 16:
    #     data_type_16 = "Project Name: {}\nMajor Version: {}\nMinor Version: {}\nBugfix Version: {}\nBuild Number:{}\nBuild Date: {}\n======================================\nTime Stamp = {}\nis Robot Power On: {}\nis Program Running: {}\nCartesian Position = {}\nSpeed Scaling = {}\n".format(
    #         a,
    #         b,
    #         c,
    #         d,
    #         e,
    #         f,
    #         unpack.ROBOT_MODE_DATA.timestamp,
    #         unpack.ROBOT_MODE_DATA.isRobotPowerOn,
    #         unpack.ROBOT_MODE_DATA.isProgramRunning,
    #         # unpack.CARTESIAN_INFO.CartesianPosition,
    #         unpack.JOINT_DATA.q_actual,
    #         unpack.ROBOT_MODE_DATA.targetSpeedFraction,
    #     )
    #     print(data_type_16)
    # elif unpack.type == 20:
    #     data_type_20 = "Project Name: {}\nMajor Version: {}\nMinor Version: {}\nBugfix Version: {}\nBuild Number:{}\nBuild Date: {}".format(
    #         unpack.VERSION_MESSAGE.projectName,
    #         unpack.VERSION_MESSAGE.majorVersion,
    #         unpack.VERSION_MESSAGE.minorVersion,
    #         unpack.VERSION_MESSAGE.bugfixVersion,
    #         unpack.VERSION_MESSAGE.buildNumber,
    #         unpack.VERSION_MESSAGE.buildDate,
    #     )
    #     print(data_type_20)
    #     a = unpack.VERSION_MESSAGE.projectName
    #     b = unpack.VERSION_MESSAGE.majorVersion
    #     c = unpack.VERSION_MESSAGE.minorVersion
    #     d = unpack.VERSION_MESSAGE.bugfixVersion
    #     e = unpack.VERSION_MESSAGE.buildNumber
    #     f = unpack.VERSION_MESSAGE.buildDate
    if unpack.type == 16:
        print("=============================================")
        print(unpack.ROBOT_MODE_DATA)
        print("=============================================")
        print(unpack.JOINT_DATA)
        print("=============================================")
        print(unpack.CARTESIAN_INFO)
        print("=============================================")
        print(unpack.TOOL_DATA)
        print("=============================================")
        print(unpack.KINEMATICS_INFO)
        print("=============================================")
        print(unpack.MASTERBOARD_DATA)
        print("=============================================")
        print(unpack.Forcemodedata)
    time.sleep(0.115)
    # print(unpack.get_package_length(data))
    # print(unpack.get_subpackage_length(data))
    # r = unpack.robot_mode_data(data)
    # print(r.timestamp)
    # print(r.isRobotPowerOn)
    # time.sleep(0.5)
s.close()
