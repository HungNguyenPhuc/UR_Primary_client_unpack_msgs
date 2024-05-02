from collections import namedtuple
import struct
import logging

# Define constants
LENGTH_FORMAT = ">I"
TYPE_FORMAT = ">B"


class Unpackage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def unpack_data(self, robot_data):
        """
        Unpack the robot data according to the specified structure.
        """
        index = 0
        unpacked_data = []
        first_package = True

        while index < len(robot_data):
            if first_package:
                # Unpack package length and package type
                package_length = struct.unpack(
                    LENGTH_FORMAT, robot_data[index : index + 4]
                )[0]
                package_type = struct.unpack(
                    TYPE_FORMAT, robot_data[index + 4 : index + 5]
                )[0]
                index += 5
                first_package = False

            # Unpack subpackage length and subpackage type
            subpackage_length = struct.unpack(
                LENGTH_FORMAT, robot_data[index : index + 4]
            )[0]
            subpackage_type = struct.unpack(
                TYPE_FORMAT, robot_data[index + 4 : index + 5]
            )[0]
            index += 5

            # Extract subpackage data based on subpackage type

            if subpackage_type == 0:  # Robot mode data
                unpacked_data.append(self.robot_mode_data(robot_data, index))
            elif subpackage_type == 1:  # Joint data
                unpacked_data.append(self.joint_data(subpackage_data))
            elif subpackage_type == 2:  # Tool data
                unpacked_data.append(self.tool_data(subpackage_data))
            elif subpackage_type == 3:  # Master board data
                unpacked_data.append(self.Masterboard_Data(subpackage_data))
            elif subpackage_type == 4:  # Cartesian info
                unpacked_data.append(self.Cartesian_Info(subpackage_data))
            # Add more elif clauses for other subpackage types

            # Move index to the start of the next package
            index += subpackage_length
        print(unpacked_data)
        return unpacked_data

    RobotModeData = namedtuple(
        "RobotModeData",
        [
            "timestamp",
            "isRealRobotConnected",
            "isRealRobotEnabled",
            "isRobotPowerOn",
            "isEmergencyStopped",
            "isProtectiveStopped",
            "isProgramRunning",
            "isProgramPaused",
            "robotMode",
            "controlMode",
            "targetSpeedFraction",
            "speedScaling",
            "reserved",
        ],
    )

    def robot_mode_data(self, robot_data, index):
        """
        Extract and unpack data related to robot mode from the given robot_data.
        """
        dataformat = ">Q???????BBddB"
        subpackage_data = robot_data[index : index + struct.calcsize(dataformat)]

        try:
            unpacked_data = struct.unpack(dataformat, subpackage_data)
            return self.RobotModeData(*unpacked_data)
        except struct.error as e:
            self.logger.error("Failed to unpack robot mode data: %s", e)
            return None

    JointData = namedtuple(
        "JointData",
        [
            "q_actual",
            "q_target",
            "qd_actual",
            "I_actual",
            "V_actual",
            "T_motor",
            "jointMode",
        ],
    )

    def joint_data(self, subpackage_data):
        """
        Extract and unpack data related to joint information from the given robot_data.
        """
        dataformat = ">dddfffB"
        try:
            unpacked_data = struct.unpack(dataformat, subpackage_data)
            return self.JointData(*unpacked_data)
        except struct.error as e:
            self.logger.error("Failed to unpack joint data: %s", e)
            return None

    ToolData = namedtuple(
        "ToolData",
        [
            "analogInputRange0",
            "analogInputRange1",
            "analogInput0",
            "analogInput1",
            "toolVoltage48V",
            "toolOutputVoltage",
            "toolCurrent",
            "toolTemperature",
            "toolMode",
        ],
    )

    def tool_data(self, subpackage_data):
        """
        Extract and unpack data related to tool information from the given robot_data.
        """
        dataformat = ">BBddfBffB"
        try:
            unpacked_data = struct.unpack(dataformat, subpackage_data)
            return self.ToolData(*unpacked_data)
        except struct.error as e:
            self.logger.error("Failed to unpack tool data: %s", e)
            return None

    MasterboardData = namedtuple(
        "MasterboardData",
        [
            "digitalInputBits",
            "digitalOutputBits",
            "analogInputRange0",
            "analogInputRange1",
            "analogInput0",
            "analogInput1",
            "analogOutputDomain0",
            "analogOutputDomain1",
            "analogOutput0",
            "analogOutput1",
            "masterBoardTemperature",
            "robotVoltage48V",
            "robotCurrent",
            "masterIOCurrent",
            "safetyMode",
            "InReducedMode",
            "euromap67InterfaceInstalled",
            "euromapInputBits",
            "euromapOutputBits",
            "euromapVoltage24V",
            "euromapCurrent",
            "URSoftwareOnly",
            "operationalModeSelectorInput",
            "threePositionEnablingDeviceInput",
            "URSoftwareOnly2",
        ],
    )

    def Masterboard_Data(self, subpackage_data):
        """
        Extract and unpack data related to tool information from the given robot_data.
        """
        dataformat = ">iiBBddccddffffBBIBBBIIffIBBB"
        try:
            unpacked_data = struct.unpack(dataformat, subpackage_data)
            return self.MasterboardData(*unpacked_data)
        except struct.error as e:
            self.logger.error("Failed to unpack tool data: %s", e)
            return None

    CartesianInfo = namedtuple(
        "CartesianInfo",
        [
            "X",
            "Y",
            "Z",
            "Rx",
            "Ry",
            "Rz",
            "TCPOffsetX",
            "TCPOffsetY",
            "TCPOffsetZ",
            "TCPOffsetRx",
            "TCPOffsetRy",
            "TCPOffsetRz",
        ],
    )

    def Cartesian_Info(self, subpackage_data):
        """
        Extract and unpack data related to tool information from the given robot_data.
        """
        dataformat = ">dddddddddddd"
        try:
            unpacked_data = struct.unpack(dataformat, subpackage_data)
            return self.CartesianInfo(*unpacked_data)
        except struct.error as e:
            self.logger.error("Failed to unpack tool data: %s", e)
            return None

    # KinematicsInfo = namedtuple(
    #     "KinematicsInfo",
    #     ["checksum", "DHtheta", "DHa", "Dhd", "Dhalpha", "calibration_status"],
    # )

    # def Kinematics_Info(self, subpackage_data):
    #     """
    #     Extract and unpack data related to tool information from the given robot_data.
    #     """
    #     dataformat = ">dddddddddddd"
    #     try:
    #         unpacked_data = struct.unpack(dataformat, subpackage_data)
    #         return self.KinematicsInfo(*unpacked_data)
    #     except struct.error as e:
    #         self.logger.error("Failed to unpack tool data: %s", e)
    #         return None
