import socket, struct


def main():

    # Establish connection to controller
    HOST = "127.0.0.1"
    PORT = 30002

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((HOST, PORT))

    while 1:
        # Loop forever, receive 4096 bytes of data (enough to store any packet)
        data = (
            "\x00\x00\x02\xAA\x10\x00\x00\x00/\x00\x00\x00\x00\x02>\xA1\xF5\x00\x01\x01\x01\x00\x00\x00\x00\x07\x00?\xF0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xF0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFB\x01\xBF\xF7"
            "B\xD0Q\x10\xB4`\xBF\xF7"
            "B\x84\xDF\xCE"
            "1P\x00\x00\x00\x00\x00\x00\x00\x00>\x9A\xB0\x01"
            "B>\xA9\xFC"
            "B\x01z\xDD"
            "A\xC1\xC6\xAA\xFD\xC0\x00i\x9A\xE8\x88Z0\xC0\x00i\x98J\x0E"
            "A\f\x00\x00\x00\x00\x00\x00\x00\x00@\xC0\xC6\x01"
            "B?\xA3\xD7"
            "B\x06\x14\x7F"
            "A\xBE"
            "2\x12\xFD\xBF\xE5\xD7V\xA2!h\xC0\xBF\xE5\xD7\xA1<%J@\x80\x00\x00\x00\x00\x00\x00\x00@z\xF0vB>\xD9\x17"
            "B\f\x99\x9E"
            "A\xD3\xD2R\xFD\xBF\xFF\x82\xDDQ\x10\xB4`\xBF\xFF\x82\xDE\x00\xD1\xB7\x18\x00\x00\x00\x00\x00\x00\x00\x00>\xD2*\x01"
            "B?\x17\x8D"
            "B\x15z\xDD"
            "A\xCC\xA4Q\xFD?\xF8\x1E"
            "9@\x00\x00\x00?\xF8\x1D\xD1\xA2\x1E\xA3Z\x00\x00\x00\x00\x00\x00\x00\x00\xBD\xD3P\x01"
            "B?\x84\x19"
            "B\x1F=lA\xC0*\xBC\xFD?\xF4\xB9\xDD\x00\x00\x00\x00?\xF4\xB9\xB6o\x93"
            "5\xD2\x00\x00\x00\x00\x00\x00\x00\x00=\xA9\xF8\x01"
            "B?E\xA2"
            "B%Q\xE7"
            "A\xABZ\xDC\xFD\x00\x00\x00"
            "e\x04\xBF\xB3"
            "8\xFF\x8D\xB0\x97\xBA\xBF\xEE&\xC5\xCE~D-?\xE2W\xCF\x92\x04\x8Ar\xBF\xFB\x8DT.\x19\xEEJ\xC0\x04\x9A\xBDl\xF2"
            "1e?\xB2\xFE\x12\xEA\xC7`\x1C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xCD\xD2\xF1\xA9\xFB\xE7m\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            "5\t\xC0\x13N\xEC\t;bg?\xB7\xA5\xC7?J\xFE\xD1\xBF\xF9k\xCC\xE4\x16\x1B,\xBF\xD0\x0B\x9C~G\xB1\x04?\xF2"
            "f^\xB1]f\x9F\xBF\xF0\x84\xED(\x18\xBF\xE2\x00\x00\x00K\x03\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01?\xA2\x90\b\x00\x00\x00\x00?\xB1\x87\xF8\x00\x00\x00\x00\x00\x00?pbM\xE0\x00\x00\x00?pbM\xE0\x00\x00\x00"
            "B\x15"
            "D\x00"
            "B@\x85S?7UD\xBE\xB7\x14H\x01\x00\x00\x88\xCE\x84\x9C\x00\x00\x01\x00\x00\x00%\x02\x01\x01?\xA7\xE7\xFD \x00\x00\x00?\xA7m\x96\xC0\x00\x00\x00"
            "C\xE2\x9C\x05\x00;\xC4\x9B\xA6@\xE0\x00\x00\xFD\x00\x00\x00=\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\xA5"
            "A\xC4"
            "f\x81\xD2\x97\x00\x00\x00\t\b\x00\x01\x00\x01\x00\x00\x00+\n\x88\xCE\x84\x9C\x00\x00?\xA0\xE9\xDA"
            "b\xC9n\x95\xBF\xD1\xFDg\x94"
            "f\x0B&?\xE5p\x03hRq\xD7\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        # initialise i to keep track of position in packet
        i = 0
        if data:
            # Print title to screen
            print("*******")
            print("UR Controller Primary Client Interface Reader")
            print("*******")
            # extract packet length, timestamp and packet type from start of packet and print to screen
            packlen = (struct.unpack("!i", data[0:4]))[0]
            timestamp = (struct.unpack("!Q", data[10:18]))[0]
            packtype = (struct.unpack("!b", data[4:5]))[0]
            print("packet length: " + str(packlen))
            print("timestamp: " + str(timestamp))
            print("packet type: " + str(packtype))
            print("*******")

            if packtype == 16:
                # if packet type is Robot State, loop until reached end of packet
                while i + 5 < packlen:

                    # extract length and type of message and print if desired
                    msglen = (struct.unpack("!i", data[5 + i : 9 + i]))[0]
                    msgtype = (struct.unpack("!b", data[9 + i : 9 + i + 1]))[0]

                    # print 'packet length: ' + str(msglen)
                    # print 'message type: ' + str(msgtype)
                    # print '*******'

                    if msgtype == 1:
                        # if message is joint data, create a list to store angles
                        angle = [0] * 6
                        j = 0
                        while j < 6:
                            # cycle through joints and extract only current joint angle (double precision)  then print to screen
                            # bytes 10 to 18 contain the j0 angle, each joint's data is 41 bytes long (so we skip j*41 each time)
                            angle[j] = (
                                struct.unpack(
                                    "!d", data[10 + i + (j * 41) : 18 + i + (j * 41)]
                                )
                            )[0]
                            print("Joint " + str(j) + " angle : " + str(angle[j]))
                            j = j + 1

                        print("*******")

                    elif msgtype == 4:
                        # if message type is cartesian data, extract doubles for 6DOF pos of TCP and print to sc    reen
                        x = (struct.unpack("!d", data[10 + i : 18 + i]))[0]
                        y = (struct.unpack("!d", data[18 + i : 26 + i]))[0]
                        z = (struct.unpack("!d", data[26 + i : 34 + i]))[0]
                        rx = (struct.unpack("!d", data[34 + i : 42 + i]))[0]
                        ry = (struct.unpack("!d", data[42 + i : 50 + i]))[0]
                        rz = (struct.unpack("!d", data[50 + i : 58 + i]))[0]

                        print("X:  " + str(x))
                        print("Y:  " + str(y))
                        print("Z:  " + str(z))
                        print("RX: " + str(rx))
                        print("RY: " + str(ry))
                        print("RZ: " + str(rz))
                        print("*******\n")
                    # increment i by the length of the message so move onto next message in packet
                    i = msglen + i


if __name__ == "__main__":
    import sys

    main()
