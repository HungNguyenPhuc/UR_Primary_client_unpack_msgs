from collections import namedtuple
import struct
from datetime import datetime

lenght_header = ">I"
type_header = ">B"
# data_type_unit64_t = ">Q"
# data_type_bool = ">?"
# data_type_unsign_char = ">B"
# data_type_double = ">d"
# data_type_float = ">f"
# data_type_uint8_t = ">B"


class unpackege:

    def __init__(self, robot_data):
        self.length = self.get_package_length(robot_data)
        self.type = self.get_package_type(robot_data)
        self.robot_data = robot_data
        print("============================================")
        print("Robot package length = ", self.length)
        print("Robot package type = ", self.type)
        if self.type == 16:
            self.current_position = 10
            print("The message is robot state message!")
            robot_data = robot_data[5:]
            print("============================================")
            self.sublength = self.get_subpackage_length(robot_data)
            self.subtype = self.get_subpackage_type(robot_data)
            while self.current_position < self.length:
                if self.subtype == 0:
                    self.ROBOT_MODE_DATA = self.robot_mode_data(robot_data)
                elif self.subtype == 1:
                    self.JOINT_DATA = self.joint_data(robot_data)
                elif self.subtype == 2:
                    self.TOOL_DATA = self.tool_data(robot_data)
                elif self.subtype == 3:
                    self.MASTERBOARD_DATA = self.Masterboard_Data(robot_data)
                elif self.subtype == 4:
                    self.CARTESIAN_INFO = self.Cartesian_Info(robot_data)
                elif self.subtype == 5:
                    if self.sublength == 9:
                        self.KINEMATICS_INFO = self.Kinematics_Info_Single(robot_data)
                    else:
                        self.KINEMATICS_INFO = self.Kinematics_Info(robot_data)
                elif self.subtype == 6:
                    self.CONFIGURATION_DATA = self.Configuration_Data(robot_data)
                elif self.subtype == 7:
                    self.FORCE_MODE_DATA = self.Force_mode_data(robot_data)
                elif self.subtype == 8:
                    self.ADDITIONAL_INFO = self.Additional_Info(robot_data)
                elif self.subtype == 9:
                    self.CALIBRATION_DATA = self.Calibration_data(robot_data)
                self.current_position += self.sublength
                robot_data = robot_data[self.sublength :]
                self.sublength = self.get_subpackage_length(robot_data)
                self.subtype = self.get_subpackage_type(robot_data)

        elif self.type == 20:
            print("The message is robot message!")
            print("============================================")
            self.timestamp_rbmessages = self.get_timestamp_rbmessages(robot_data)
            self.source_data = self.get_source(robot_data)
            robot_data = robot_data[14:]
            self.subtype = self.get_subpackage_type1(robot_data)
            if self.subtype == 0:
                self.TEXT_MESSAGE = self.Text_Message(robot_data)
            elif self.subtype == 1:
                self.POPUP_MESSAGE = self.Popup_Message(robot_data)
            elif self.subtype == 3:
                self.VERSION_MESSAGE = self.Version_Message(robot_data)
            elif self.subtype == 5:
                self.SAFETY_MODE_MESSAGE = self.Safety_Mode_Message(robot_data)
            elif self.subtype == 6:
                self.ROBOT_COMM_MESSAGE = self.Robot_Comm_Message(robot_data)
            elif self.subtype == 7:
                self.KEY_MESSAGE = self.Key_Message(robot_data)
            elif self.subtype == 9:
                self.REQUEST_VALUE_MESSAGE = self.Request_Value_Message(robot_data)
            elif self.subtype == 10:
                self.RUNTIME_EXCEPTION_MESSAGE = self.Runtime_Exception_Message(
                    robot_data
                )
            elif self.subtype == 14:
                self.PROGRAM_THREADS_MESSAGE = self.Program_Threads_Message(robot_data)
        elif self.type == 25:
            print("The message is variable message!")
            print("============================================")
            self.timestamp_rbmessages = self.get_timestamp_rbmessages(robot_data)
            self.source_data = self.get_source(robot_data)
            robot_data = robot_data[14:]
            self.subtype = self.get_subpackage_type1(robot_data)
            if self.subtype == 0:
                self.GLOBAL_VARIABLES_SETUP_MESSAGE = (
                    self.Global_Variables_Setup_Message(robot_data)
                )
            elif self.subtype == 1:
                self.GLOBAL_VARIABLES_UPDATE_MESSAGE = (
                    self.Global_Variables_Update_Message(robot_data)
                )
            elif self.subtype == 2:
                self.VAR_MESSAGE = self.Var_Message(robot_data)

    def get_package_length(self, robot_data):
        """
        Extract the package length from the given robot data.
        Returns:
            int: The length of the package as an integer.
        """
        package_length = struct.unpack(lenght_header, robot_data[0:4])[0]
        return package_length

    def get_package_type(self, robot_data):
        """
        Extract the package type from the given robot data.
        Returns:
            int: The type of the package as an integer.
        """
        package_type = struct.unpack(type_header, robot_data[4:5])[0]
        return package_type

    def get_subpackage_length(self, robot_data):
        """
        Extract the subpackage length from the given robot data.
        Returns:
            int: The length of the package as an integer.
        """
        # subpackage_length = struct.unpack(lenght_header, robot_data[0:4])[0]
        subpackage_length = struct.unpack_from(lenght_header, robot_data, 4)[0]
        # print("length of subpackage = ", subpackage_length)
        return subpackage_length

    def get_subpackage_type(self, robot_data):
        """
        Extract the subpackage type from the given robot data.
        Returns:
            int: The type of the package as an integer.
        """
        # subpackage_type = struct.unpack(type_header, robot_data[4:5])[0]
        subpackage_type = struct.unpack_from(type_header, robot_data, 1)[0]
        # print("type of subpackage = ", subpackage_type)
        return subpackage_type

    def get_subpackage_type1(self, robot_data):
        """
        Extract the subpackage type from the given robot data.
        Returns:
            int: The type of the package as an integer.
        """
        subpackage_type1 = struct.unpack(">b", robot_data[0:1])[0]
        # print("type of subpackage = ", subpackage_type)
        return subpackage_type1

    def get_timestamp_rbmessages(self, robot_data):
        timestamp_rbmessages = struct.unpack(">Q", robot_data[5:13])[0]
        return timestamp_rbmessages

    def get_source(self, robot_data):
        source = struct.unpack(">b", robot_data[13:14])[0]
        return source

    def robot_mode_data(self, robot_data):
        dataformat = ">Q???????BBddB"
        (
            robot_timestamp,
            robot_isRealRobotConnected,
            robot_isRealRobotEnabled,
            robot_isRobotPowerOn,
            robot_isEmergencyStopped,
            robot_isProtectiveStopped,
            robot_isProgramRunning,
            robot_isProgramPaused,
            robot_robotMode,
            robot_controlMode,
            robot_targetSpeedFraction,
            robot_speedScaling,
            robot_reserved,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        robot_timestamp = datetime.fromtimestamp(robot_timestamp)
        return self.RobotModeData(
            robot_timestamp,
            robot_isRealRobotConnected,
            robot_isRealRobotEnabled,
            robot_isRobotPowerOn,
            robot_isEmergencyStopped,
            robot_isProtectiveStopped,
            robot_isProgramRunning,
            robot_isProgramPaused,
            robot_robotMode,
            robot_controlMode,
            robot_targetSpeedFraction,
            robot_speedScaling,
            robot_reserved,
        )

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
    JointData = namedtuple(
        "JointData",
        [
            "q_actual",
            "q_target",
            "qd_actual",
            "I_actual",
            "V_actual",
            "T_motor",
            "T_micro",
            "jointMode",
        ],
    )

    def joint_data(self, robot_data):
        dataformat = ">dddffffBdddffffBdddffffBdddffffBdddffffBdddffffB"
        (
            q_actual0,
            q_target0,
            qd_actual0,
            I_actual0,
            V_actual0,
            T_motor0,
            T_micro0,
            jointMode0,
            q_actual1,
            q_target1,
            qd_actual1,
            I_actual1,
            V_actual1,
            T_motor1,
            T_micro1,
            jointMode1,
            q_actual2,
            q_target2,
            qd_actual2,
            I_actual2,
            V_actual2,
            T_motor2,
            T_micro2,
            jointMode2,
            q_actual3,
            q_target3,
            qd_actual3,
            I_actual3,
            V_actual3,
            T_motor3,
            T_micro3,
            jointMode3,
            q_actual4,
            q_target4,
            qd_actual4,
            I_actual4,
            V_actual4,
            T_motor4,
            T_micro4,
            jointMode4,
            q_actual5,
            q_target5,
            qd_actual5,
            I_actual5,
            V_actual5,
            T_motor5,
            T_micro5,
            jointMode5,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        q_actual = (q_actual0, q_actual1, q_actual2, q_actual3, q_actual4, q_actual5)
        q_target = (q_target0, q_target1, q_target2, q_target3, q_target4, q_target5)
        qd_actual = (
            qd_actual0,
            qd_actual1,
            qd_actual2,
            qd_actual3,
            qd_actual4,
            qd_actual5,
        )
        I_actual = (I_actual0, I_actual1, I_actual2, I_actual3, I_actual4, I_actual5)
        V_actual = (V_actual0, V_actual1, V_actual2, V_actual3, V_actual4, V_actual5)
        T_motor = (T_motor0, T_motor1, T_motor2, T_motor3, T_motor4, T_motor5)
        T_micro = (T_micro0, T_micro1, T_micro2, T_micro3, T_micro4, T_micro5)
        jointMode = (
            jointMode0,
            jointMode1,
            jointMode2,
            jointMode3,
            jointMode4,
            jointMode5,
        )
        return self.JointData(
            q_actual,
            q_target,
            qd_actual,
            I_actual,
            V_actual,
            T_motor,
            T_micro,
            jointMode,
        )

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

    def tool_data(self, robot_data):
        dataformat = ">BBddfBffB"
        (
            analogInputRange0,
            analogInputRange1,
            analogInput0,
            analogInput1,
            toolVoltage48V,
            toolOutputVoltage,
            toolCurrent,
            toolTemperature,
            toolMode,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        return self.ToolData(
            analogInputRange0,
            analogInputRange1,
            analogInput0,
            analogInput1,
            toolVoltage48V,
            toolOutputVoltage,
            toolCurrent,
            toolTemperature,
            toolMode,
        )

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

    def Masterboard_Data(self, robot_data):
        dataformat = ">iiBBddbbddffffBBb"
        (
            digitalInputBits,
            digitalOutputBits,
            analogInputRange0,
            analogInputRange1,
            analogInput0,
            analogInput1,
            analogOutputDomain0,
            analogOutputDomain1,
            analogOutput0,
            analogOutput1,
            masterBoardTemperature,
            robotVoltage48V,
            robotCurrent,
            masterIOCurrent,
            safetyMode,
            InReducedMode,
            euromap67InterfaceInstalled,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        i = 5 + struct.calcsize(dataformat)
        if euromap67InterfaceInstalled == 0:
            euromapInputBits = None
            euromapOutputBits = None
            euromapVoltage24V = None
            euromapCurrent = None
            dataformat = ">IBBB"
            (
                URSoftwareOnly,
                operationalModeSelectorInput,
                threePositionEnablingDeviceInput,
                URSoftwareOnly2,
            ) = struct.unpack(
                dataformat, robot_data[i : i + struct.calcsize(dataformat)]
            )
        else:
            dataformat = ">IIffIBBB"
            (
                euromapInputBits,
                euromapOutputBits,
                euromapVoltage24V,
                euromapCurrent,
                URSoftwareOnly,
                operationalModeSelectorInput,
                threePositionEnablingDeviceInput,
                URSoftwareOnly2,
            ) = struct.unpack(
                dataformat, robot_data[i : i + struct.calcsize(dataformat)]
            )
        return self.MasterboardData(
            digitalInputBits,
            digitalOutputBits,
            analogInputRange0,
            analogInputRange1,
            analogInput0,
            analogInput1,
            analogOutputDomain0,
            analogOutputDomain1,
            analogOutput0,
            analogOutput1,
            masterBoardTemperature,
            robotVoltage48V,
            robotCurrent,
            masterIOCurrent,
            safetyMode,
            InReducedMode,
            euromap67InterfaceInstalled,
            euromapInputBits,
            euromapOutputBits,
            euromapVoltage24V,
            euromapCurrent,
            URSoftwareOnly,
            operationalModeSelectorInput,
            threePositionEnablingDeviceInput,
            URSoftwareOnly2,
        )

    CartesianInfo = namedtuple(
        "CartesianInfo",
        ["CartesianPosition", "TCPOffset"],
    )

    def Cartesian_Info(self, robot_data):
        dataformat = ">dddddddddddd"
        (
            X_p,
            Y_p,
            Z_p,
            Rx,
            Ry,
            Rz,
            TCPOffsetX,
            TCPOffsetY,
            TCPOffsetZ,
            TCPOffsetRx,
            TCPOffsetRy,
            TCPOffsetRz,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        CartesianPosition = (
            X_p,
            Y_p,
            Z_p,
            Rx,
            Ry,
            Rz,
        )
        TCPOffset = (
            TCPOffsetX,
            TCPOffsetY,
            TCPOffsetZ,
            TCPOffsetRx,
            TCPOffsetRy,
            TCPOffsetRz,
        )
        return self.CartesianInfo(
            CartesianPosition,
            TCPOffset,
        )

    KinematicsInfo = namedtuple(
        "KinematicsInfo",
        ["checksum", "DHtheta", "DHa", "Dhd", "Dhalpha", "calibration_status"],
    )
    KinematicsInfoSingle = namedtuple(
        "KinematicsInfoSingle",
        ["calibration_status"],
    )

    def Kinematics_Info_Single(
        self, robot_data
    ):  # Controller only sends joint info on change; therefore, adjust accordingly.
        dataformat = ">I"
        calibration_status = struct.unpack(
            dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)]
        )
        return self.KinematicsInfoSingle(calibration_status)

    def Kinematics_Info(self, robot_data):  # Controller sends joint info
        dataformat = ">IIIIIIddddddddddddddddddddddddI"
        (
            cheksum0,
            cheksum1,
            cheksum2,
            cheksum3,
            cheksum4,
            cheksum5,
            DHtheta0,
            DHtheta1,
            DHtheta2,
            DHtheta3,
            DHtheta4,
            DHtheta5,
            DHa0,
            DHa1,
            DHa2,
            DHa3,
            DHa4,
            DHa5,
            Dhd0,
            Dhd1,
            Dhd2,
            Dhd3,
            Dhd4,
            Dhd5,
            DHalpha0,
            DHalpha1,
            DHalpha2,
            DHalpha3,
            DHalpha4,
            DHalpha5,
            calibration_status,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        checksum = (
            cheksum0,
            cheksum1,
            cheksum2,
            cheksum3,
            cheksum4,
            cheksum5,
        )
        DHtheta = (
            DHtheta0,
            DHtheta1,
            DHtheta2,
            DHtheta3,
            DHtheta4,
            DHtheta5,
        )
        DHa = (
            DHa0,
            DHa1,
            DHa2,
            DHa3,
            DHa4,
            DHa5,
        )
        Dhd = (
            Dhd0,
            Dhd1,
            Dhd2,
            Dhd3,
            Dhd4,
            Dhd5,
        )
        DHalpha = (
            DHalpha0,
            DHalpha1,
            DHalpha2,
            DHalpha3,
            DHalpha4,
            DHalpha5,
        )

        return self.KinematicsInfo(
            checksum, DHa, Dhd, DHalpha, DHtheta, calibration_status
        )

    ConfigurationData = namedtuple(
        "ConfigurationData",
        [
            "jointLimit",
            "jointMaxSpeed",
            "jointMaxAcceleration",
            "vJointDefault",
            "aJointDefault",
            "vToolDefault",
            "aToolDefault",
            "eqRadius",
            "DHa",
            "Dhd",
            "DHalpha",
            "DHtheta",
            "masterboardVersion",
            "controllerBoxType",
            "robotType",
            "robotSubType",
        ],
    )

    def Configuration_Data(self, robot_data):
        dataformat = ">dddddddddddddddddddddddddddddddddddddddddddddddddddddIIII"
        (
            jointMinLimit0,
            jointMaxLimit0,
            jointMinLimit1,
            jointMaxLimit1,
            jointMinLimit2,
            jointMaxLimit2,
            jointMinLimit3,
            jointMaxLimit3,
            jointMinLimit4,
            jointMaxLimit4,
            jointMinLimit5,
            jointMaxLimit5,
            jointMaxSpeed0,
            jointMaxAcceleration0,
            jointMaxSpeed1,
            jointMaxAcceleration1,
            jointMaxSpeed2,
            jointMaxAcceleration2,
            jointMaxSpeed3,
            jointMaxAcceleration3,
            jointMaxSpeed4,
            jointMaxAcceleration4,
            jointMaxSpeed5,
            jointMaxAcceleration5,
            vJointDefault,
            aJointDefault,
            vToolDefault,
            aToolDefault,
            eqRadius,
            DHa0,
            DHa1,
            DHa2,
            DHa3,
            DHa4,
            DHa5,
            Dhd0,
            Dhd1,
            Dhd2,
            Dhd3,
            Dhd4,
            Dhd5,
            DHalpha0,
            DHalpha1,
            DHalpha2,
            DHalpha3,
            DHalpha4,
            DHalpha5,
            DHtheta0,
            DHtheta1,
            DHtheta2,
            DHtheta3,
            DHtheta4,
            DHtheta5,
            masterboardVersion,
            controllerBoxType,
            robotType,
            robotSubType,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        jointLimit = (
            (jointMinLimit0, jointMaxLimit0),
            (jointMinLimit1, jointMaxLimit1),
            (jointMinLimit2, jointMaxLimit2),
            (jointMinLimit3, jointMaxLimit3),
            (jointMinLimit4, jointMaxLimit4),
            (jointMinLimit5, jointMaxLimit5),
        )
        jointMaxSpeed = (
            jointMaxSpeed0,
            jointMaxSpeed1,
            jointMaxSpeed2,
            jointMaxSpeed3,
            jointMaxSpeed4,
            jointMaxSpeed5,
        )
        jointMaxAcceleration = (
            jointMaxAcceleration0,
            jointMaxAcceleration1,
            jointMaxAcceleration2,
            jointMaxAcceleration3,
            jointMaxAcceleration4,
            jointMaxAcceleration5,
        )
        DHa = (
            DHa0,
            DHa1,
            DHa2,
            DHa3,
            DHa4,
            DHa5,
        )
        Dhd = (
            Dhd0,
            Dhd1,
            Dhd2,
            Dhd3,
            Dhd4,
            Dhd5,
        )
        DHalpha = (
            DHalpha0,
            DHalpha1,
            DHalpha2,
            DHalpha3,
            DHalpha4,
            DHalpha5,
        )
        DHtheta = (
            DHtheta0,
            DHtheta1,
            DHtheta2,
            DHtheta3,
            DHtheta4,
            DHtheta5,
        )
        return self.ConfigurationData(
            jointLimit,
            jointMaxSpeed,
            jointMaxAcceleration,
            vJointDefault,
            aJointDefault,
            vToolDefault,
            aToolDefault,
            eqRadius,
            DHa,
            Dhd,
            DHalpha,
            DHtheta,
            masterboardVersion,
            controllerBoxType,
            robotType,
            robotSubType,
        )

    Forcemodedata = namedtuple(
        "Forcemodedata",
        [
            "F_xyz",
            "Fr_xyz",
            "robotDexterity",
        ],
    )

    def Force_mode_data(self, robot_data):
        dataformat = ">ddddddd"
        (
            Fx,
            Fy,
            Fz,
            Frx,
            Fry,
            Frz,
            robotDexterity,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        F_xyz = (
            Fx,
            Fy,
            Fz,
        )
        Fr_xyz = (
            Frx,
            Fry,
            Frz,
        )
        return self.Forcemodedata(F_xyz, Fr_xyz, robotDexterity)

    AdditionalInfo = namedtuple(
        "AdditionalInfo",
        ["tpButtonState", "freedriveButtonEnabled", "IOEnabledFreedrive", "reserved"],
    )

    def Additional_Info(self, robot_data):
        dataformat = ">B??B"
        (tpButtonState, freedriveButtonEnabled, IOEnabledFreedrive, reserved) = (
            struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        )
        return self.AdditionalInfo(
            tpButtonState, freedriveButtonEnabled, IOEnabledFreedrive, reserved
        )

    CalibrationData = namedtuple(
        "CalibrationData",
        [
            "CF_xyz",
            "CFr_xyz",
        ],
    )

    def Calibration_data(
        self, robot_data
    ):  # This package is used internally by Universal Robots software only and should be skipped.
        dataformat = ">dddddd"
        (
            CFx,
            CFy,
            CFz,
            CFrx,
            CFry,
            CFrz,
        ) = struct.unpack(dataformat, robot_data[5 : 5 + struct.calcsize(dataformat)])
        CF_xyz = (
            CFx,
            CFy,
            CFz,
        )
        CFr_xyz = (
            CFrx,
            CFry,
            CFrz,
        )
        return self.CalibrationData(CF_xyz, CFr_xyz)

    VersionMessage = namedtuple(
        "VersionMessage",
        [
            "projectNameSize",
            "projectName",
            "majorVersion",
            "minorVersion",
            "bugfixVersion",
            "buildNumber",
            "buildDate",
        ],
    )

    def Version_Message(self, robot_data):
        # dataformat = ">bsBBiis"
        dataformat = ">b"
        (projectNameSize,) = struct.unpack(
            dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)]
        )
        i = 1 + struct.calcsize(dataformat)
        # format_data = robot_data[i:]
        char_array_length = projectNameSize
        format_string = "{}s".format(char_array_length)
        projectName = struct.unpack_from(format_string, robot_data, i)[0].decode(
            "utf-8"
        )
        # format_data = format_data[char_array_length:]
        i1 = i + projectNameSize
        dataformat = ">BBii"
        (
            majorVersion,
            minorVersion,
            bugfixVersion,
            buildNumber,
        ) = struct.unpack_from(dataformat, robot_data, i1)
        i2 = i1 + struct.calcsize(dataformat)
        # i = struct.calcsize(dataformat)
        # format_data = format_data[i:]
        # char_array_length = self.length - (struct.calcsize(">bBBii") + projectNameSize)
        char_array_length = self.length - (i2 + 14)
        # char_array_length = self.length - (len(robot_data) - len(format_data))
        # print("format length=", char_array_length)
        format_string = "{}s".format(char_array_length)
        buildDate = struct.unpack_from(format_string, robot_data, i2)[0].decode("utf-8")
        return self.VersionMessage(
            projectNameSize,
            projectName,
            majorVersion,
            minorVersion,
            bugfixVersion,
            buildNumber,
            buildDate,
        )

    SafetyModeMessage = namedtuple(
        "SafetyModeMessage",
        [
            "robotMessageCode",
            "robotMessageArgument",
            "safetyModeType",
            "reportDataType",
            "reportData",
        ],
    )

    def Safety_Mode_Message(self, robot_data):
        dataformat = ">iiBII"
        (
            robotMessageCode,
            robotMessageArgument,
            safetyModeType,
            reportDataType,
            reportData,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        return self.SafetyModeMessage(
            robotMessageCode,
            robotMessageArgument,
            safetyModeType,
            reportDataType,
            reportData,
        )

    RobotCommMessage = namedtuple(
        "RobotCommMessage",
        [
            "robotMessageCode",
            "robotMessageArgument",
            "robotMessageReportLevel",
            "robotMessageDataType",
            "robotMessageData",
            "robotCommTextMessage",
        ],
    )

    def Robot_Comm_Message(self, robot_data):
        dataformat = ">iiiII"
        (
            robotMessageCode,
            robotMessageArgument,
            robotMessageReportLevel,
            robotMessageDataType,
            robotMessageData,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        i = 1 + struct.calcsize(dataformat)
        char_array_length = self.length - (i + 14)
        format_string = "{}s".format(char_array_length)
        robotCommTextMessage = struct.unpack_from(format_string, robot_data, i).decode(
            "utf-8"
        )
        return self.RobotCommMessage(
            robotMessageCode,
            robotMessageArgument,
            robotMessageReportLevel,
            robotMessageDataType,
            robotMessageData,
            robotCommTextMessage,
        )

    KeyMessage = namedtuple(
        "KeyMessage",
        [
            "robotMessageCode",
            "robotMessageArgument",
            "robotMessageTitleSize",
            "robotMessageTitle",
            "keyTextMessage",
        ],
    )

    def Key_Message(self, robot_data):
        dataformat = ">iiB"
        (
            robotMessageCode,
            robotMessageArgument,
            robotMessageTitleSize,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        i = 1 + struct.calcsize(dataformat)
        char_array_length = robotMessageTitleSize
        format_string = "{}s".format(char_array_length)
        robotMessageTitle = struct.unpack_from(format_string, robot_data, i)[0].decode(
            "utf-8"
        )
        i1 = i + robotMessageTitleSize
        char_array_length = self.length - (i1 + 14)
        format_string = "{}s".format(char_array_length)
        keyTextMessage = struct.unpack_from(format_string, robot_data, i1)[0].decode(
            "utf-8"
        )
        return self.KeyMessage(
            robotMessageCode,
            robotMessageArgument,
            robotMessageTitleSize,
            robotMessageTitle,
            keyTextMessage,
        )

    ProgramThreadsMessage = namedtuple(
        "ProgramThreadsMessage",
        [
            "labelId",
            "labelNameLength",
            "labelName",
            "threadNameLength",
            "threadName",
        ],
    )

    def Program_Threads_Message(self, robot_data):
        dataformat = ">ii"
        (
            labelId,
            labelNameLength,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        i = 1 + struct.calcsize(dataformat)
        char_array_length = labelNameLength
        format_string = "{}s".format(char_array_length)
        labelName = struct.unpack_from(format_string, robot_data, i)[0].decode("utf-8")
        i1 = i + labelNameLength
        dataformat = ">i"
        (threadNameLength) = struct.unpack(
            dataformat, robot_data[i1 : i1 + struct.calcsize(dataformat)]
        )
        i2 = i1 + struct.calcsize(dataformat)
        char_array_length = threadNameLength
        format_string = "{}s".format(char_array_length)
        threadName = struct.unpack_from(format_string, robot_data, i2)[0].decode(
            "utf-8"
        )
        return self.ProgramThreadsMessage(
            labelId,
            labelNameLength,
            labelName,
            threadNameLength,
            threadName,
        )

    PopupMessage = namedtuple(
        "PopupMessage",
        [
            "requestId",
            "requestedType",
            "warning",
            "error",
            "blocking",
            "popupMessageTitleSize",
            "popupMessageTitle",
            "popupTextMessage",
        ],
    )

    def Popup_Message(self, robot_data):
        dataformat = ">II???B"
        (
            requestId,
            requestedType,
            warning,
            error,
            blocking,
            popupMessageTitleSize,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        i = 1 + struct.calcsize(dataformat)
        char_array_length = popupMessageTitleSize
        format_string = "{}s".format(char_array_length)
        popupMessageTitle = struct.unpack_from(format_string, robot_data, i)[0].decode(
            "utf-8"
        )
        i1 = i + popupMessageTitleSize
        char_array_length = self.length - (i1 + 14)
        format_string = "{}s".format(char_array_length)
        popupTextMessage = struct.unpack_from(format_string, robot_data, i1)[0].decode(
            "utf-8"
        )
        return self.PopupMessage(
            requestId,
            requestedType,
            warning,
            error,
            blocking,
            popupMessageTitleSize,
            popupMessageTitle,
            popupTextMessage,
        )

    RequestValueMessage = namedtuple(
        "RequestValueMessage",
        [
            "requestId",
            "requestedType",
            "requestTextMessage",
        ],
    )

    def Request_Value_Message(self, robot_data):
        dataformat = ">II"
        (
            requestId,
            requestedType,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        i = 1 + struct.calcsize(dataformat)
        char_array_length = self.length - (i + 14)
        format_string = "{}s".format(char_array_length)
        requestTextMessage = struct.unpack_from(format_string, robot_data, i)[0].decode(
            "utf-8"
        )
        return self.RequestValueMessage(requestId, requestedType, requestTextMessage)

    TextMessage = namedtuple(
        "TextMessage",
        [
            "textTextMessage",
        ],
    )

    def Text_Message(self, robot_data):
        char_array_length = self.length - 14
        format_string = "{}s".format(char_array_length)
        textTextMessage = struct.unpack_from(format_string, robot_data, 1)[0].decode(
            "utf-8"
        )
        return self.TextMessage(textTextMessage)

    RuntimeExceptionMessage = namedtuple(
        "RuntimeExceptionMessage",
        [
            "scriptLineNumber",
            "scriptColumnNumber",
            "runtimeExceptionTextMessage",
        ],
    )

    def Runtime_Exception_Message(self, robot_data):
        dataformat = ">ii"
        (
            scriptLineNumber,
            scriptColumnNumber,
        ) = struct.unpack(dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)])
        i = 1 + struct.calcsize(dataformat)
        char_array_length = self.length - (i + 14)
        format_string = "{}s".format(char_array_length)
        runtimeExceptionTextMessage = struct.unpack_from(format_string, robot_data, i)[
            0
        ].decode("utf-8")
        return self.RuntimeExceptionMessage(
            scriptLineNumber,
            scriptColumnNumber,
            runtimeExceptionTextMessage,
        )

    VarMessage = namedtuple(
        "VarMessage",
        [
            "varMessageTitleSize",
            "varMessageTitle",
            "varTextMessage",
        ],
    )

    def Var_Message(self, robot_data):
        dataformat = ">B"
        (varMessageTitleSize,) = struct.unpack(
            dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)]
        )
        i = 1 + struct.calcsize(dataformat)
        char_array_length = varMessageTitleSize
        format_string = "{}s".format(char_array_length)
        varMessageTitle = struct.unpack_from(format_string, robot_data, i)[0].decode(
            "utf-8"
        )
        i1 = i + varMessageTitleSize
        char_array_length = self.length - (i1 + 14)
        format_string = "{}s".format(char_array_length)
        varTextMessage = struct.unpack_from(format_string, robot_data, i1)[0].decode(
            "utf-8"
        )
        return self.VarMessage(
            varMessageTitleSize,
            varMessageTitle,
            varTextMessage,
        )

    GlobalVariablesSetupMessage = namedtuple(
        "GlobalVariablesSetupMessage",
        [
            "startIndex",
            "variableNames",
        ],
    )

    def Global_Variables_Setup_Message(self, robot_data):
        dataformat = ">H"
        (startIndex) = struct.unpack(
            dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)]
        )
        i = 1 + struct.calcsize(dataformat)
        char_array_length = self.length - (i + 14)
        format_string = "{}s".format(char_array_length)
        variableNames = struct.unpack_from(format_string, robot_data, i)[0].decode(
            "utf-8"
        )
        return self.GlobalVariablesSetupMessage(startIndex, variableNames)

    GlobalVariablesUpdateMessage = namedtuple(
        "GlobalVariablesUpdateMessage",
        [
            "startIndex",
            "variableNames",
        ],
    )

    def Global_Variables_Update_Message(self, robot_data):
        dataformat = ">HB"
        (startIndex, variableNames) = struct.unpack(
            dataformat, robot_data[1 : 1 + struct.calcsize(dataformat)]
        )
        return self.GlobalVariablesUpdateMessage(startIndex, variableNames)


if __name__ == "__main__":
    import socket
    import time

    HOST = "127.0.0.1"
    PORT = 30001
    print("Starting program")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    time.sleep(1)
    f = open("Test_send_program_to_UR/test.script", "rb")
    l = f.read(4096)
    print(l)
    s.sendall(l)
    print("End program")
    while 1:
        # Loop forever, receive 4096 bytes of data (enough to store any packet)
        data = s.recv(4096)
        aa = unpackege(data)
