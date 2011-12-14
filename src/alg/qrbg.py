###### qrbg.py
# For accessing the quantum random bit generator at random.irb.hr
# (c) 2007 Brendan Burns
# Portions (c) 2007  Radomir Stevanovic and Rudjer Boskovic Institute.
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
###### Example Usage
# rand = qrbg("username", "password");
# print rand.getByte()
# print rand.getInt()
# print rand.getFloat()
# print rand.getDouble()
# for i in range(100):
#    print rand.getDouble()
######
from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack

class qrbg:
    bytes = []
    available = 0
    
    user = ""
    password = ""
    host = ""
    port = 0

    def __init__(self, user, password, host="random.irb.hr", port=1227,
            verbose=False):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.verbose = verbose

    def getUnsignedInt(self):
        if (self.available < 4):
            self.request(4096)
        field = unpack("!I", self.bytes[0:4])
        self.available -= 4
        self.bytes = self.bytes[4:]
        return field[0]

    def getInt(self):
        if (self.available < 4):
            self.request(4096)
        field = unpack("!i", self.bytes[0:4])
        self.available -= 4
        self.bytes = self.bytes[4:]
        return field[0]
        
    def getLong(self):
        if (self.available < 8):
            self.request(4096)
        field = unpack("!q", self.bytes[0:8]);
        self.available -= 8
        self.bytes = self.bytes[8:]
        return field[0]

    def getUnsignedLong(self):
        if (self.available < 8):
            self.request(4096)
        field = unpack("!Q", self.bytes[0:8]);
        self.available -= 8
        self.bytes = self.bytes[8:]
        return field[0]

    def getFloat(self):
        data = 0x3F800000 | (self.getInt() & 0x00FFFFFF)
        foo = pack("!i", data);
        fields = unpack("!f", foo);
        return fields[0]-1.0

    def getDouble(self):
        data = 0x3FF0000000000000l | (self.getLong() & 0x000FFFFFFFFFFFFFl);
        foo = pack("!q", data)
        field = unpack("!d", foo)
        return field[0] - 1.0
    
    def getUnsignedShort(self):
        if (self.available < 2):
            self.request(4096)
        field = unpack("!H", self.bytes[0:2])
        self.available -= 2
        self.bytes = self.bytes[2:]
        return field[0]

    def getShort(self):
        if (self.available < 2):
            self.request(4096)
        field = unpack("!h", self.bytes[0:2])
        self.available -= 2
        self.bytes = self.bytes[2:]
        return field[0]

    def getByte(self):
        if (self.available < 1):
            self.request(4096);
        self.available = self.available - 1
        result = ord(self.bytes[0]);
        self.bytes = self.bytes[1:]
        return result

    def request(self, size):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.host, self.port))
        contentSize = len(self.user)+len(self.password)+6;
        contentString = "!BHB"+str(len(self.user))+"sB"+str(len(self.password))+"sL"
        data = pack(contentString, 0, contentSize, len(self.user), self.user, len(self.password), self.password, size)
        sock.sendall(data)
        if self.verbose:
            print "Sent!"
        data = sock.recv(6)
        if len(data) != 6:
            # There was some kind of error, assuming
            # 2 bytes were received
            fields = unpack("!BB", str(data))
        else:
            fields = unpack("!BBL", str(data))
        if (fields[0] != 0):
            raise(ServiceDeniedError(fields[0],fields[1]))

        self.bytes = sock.recv(fields[2])
        self.available = len(self.bytes)
        if self.verbose:
            print "Received: "
            print self.available
        sock.close()



class ServiceDeniedError(Exception):
    SERVER_RESPONSES = \
    [
        "OK",
        "Service was shutting down",
        "Server was/is experiencing internal errors",
        "Service said we have requested some unsupported operation",
        "Service said we sent an ill-formed request packet",
        "Service said we were sending our request too slow",
        "Authentication failed",
        "User quota exceeded"
    ]
    
    SERVER_REMEDY = \
    [
        "None",
        "Try again later",
        "Try again later",
        "Upgrade your client software",
        "Upgrade your client software",
        "Check your network connection",
        "Check your login credentials",
        "Try again later, or contact Service admin to increase your quota(s)"
    ]

    def __init__(self, response, reason):
        self.response = response
        self.reason = reason

    def __str__(self):
        return self.SERVER_RESPONSES[self.response]+" : "+self.SERVER_REMEDY[self.response]

