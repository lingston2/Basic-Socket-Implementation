from socket import *
import time
import struct

#Declaration
i = 1
Received_Ping = 0
Total_Ping_RTT_Count = 0

# Self Server
# ServerDestinationIP = "127.0.0.1"
# ServerDestinationPort = 8080

#Target Server
ServerDestinationIP = "140.114.89.43"
ServerDestinationPort = 55556
TargetAddress = (ServerDestinationIP, ServerDestinationPort)

# Create UDP Socket, named CilentPingerSocket
CilentPingerSocket = socket(AF_INET, SOCK_DGRAM)

# Create ICMP Socket, Named CilentICMPSocket
CilentICMPSocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

#Set Timeout
CilentICMPSocket.settimeout(1)
CilentPingerSocket.settimeout(1)

#ICMP Message
def Print_ICMP_Message(ICMPType, ICMPCode):
    if ICMPType == 0:
        print("Echo Reply.")
    elif ICMPType == 3:
        print("Destination", end=' ')

        if ICMPCode == 0:
            print("net is unreachble.")
        elif ICMPCode == 1:
            print("host is unreachable.")
        elif ICMPCode == 2:
            print("protocol is unreachable.")
        elif ICMPCode == 3:
            print("port is unreachable.")
        elif ICMPCode == 4:
            print("fragmentation is needed and don't fragment was set.")
        elif ICMPCode == 5:
            print("source route failed.")
        elif ICMPCode == 6:
            print("network is unknown.")
        elif ICMPCode == 7:
            print("host is unknown.")
        elif ICMPCode == 8:
            print("source host is isolated.")
        elif ICMPCode == 9:
            print("communication with destination network is administratively prohibted.")
        elif ICMPCode == 10:
            print("communication with destination host is administratively prohibted.")
        elif ICMPCode == 11:
            print("network is unreachable for type of service.")
        elif ICMPCode == 12:
            print("host is unreachable for type of service.")
        elif ICMPCode == 13:
            print("communication is administrativeley prohibited.")
        elif ICMPCode == 14:
            print("Host precendece violation.")
        elif ICMPCode == 15:
            print("precended cutoff is in.")
        
    elif ICMPType == 4:
        print("Source quench.")
    elif ICMPType == 5:
        print("Redirect", end=' ')

        if ICMPCode == 0:
            print("diagram for the network (or subnet).")
        elif ICMPCode == 1:
            print("datagram for the host.")
        elif ICMPCode == 2:
            print("datagram for the type of service and network.")
        elif ICMPCode == 3:
            print("datagram for the type of service and host.")


    elif ICMPType == 8:
        print("Echo.")
    elif ICMPType == 9:
        print("Router advertisement.")
    elif ICMPType == 10:
        print("Router selection.")
    elif ICMPType == 11:
        #print("Time exceeded")

        if ICMPCode == 0:
            print("Time to Live exceeded in transit.")
        elif ICMPCode == 1:
            print("Fragment reassembly time exceeded.")
            

    elif ICMPType == 12:
        print("Parameter problem:", end=' ')

        if ICMPCode == 0:
            print("Pointer indicates the error.")
        elif ICMPCode == 1:
            print("Missing a required option.")
        elif ICMPCode == 2:
            print("Bad lenght.")
        
    elif ICMPType == 13:
        print("Timestamp.")
    elif ICMPType == 14:
        print("Timestamp reply.")
    elif ICMPType == 15:
        print("Information request.")
    elif ICMPType == 16:
        print("Information reply.")
    elif ICMPType == 17:
        print("Address mask request.")
    elif ICMPType == 18:
        print("Address mask reply.")
    elif ICMPType == 30:
        print("Traceroute.")
    
while i<11:
    #Message Content
    message_send = "PING"
    
    try:
        #print("UDP Writing")
        #Send Message
        CilentPingerSocket.sendto(message_send.encode(), TargetAddress)

        #print("ICMP Writing")
        #Receive ICMP Packets From Target
        RecICMPMessage ,ICMPserverAdd = CilentICMPSocket.recvfrom(1024)

        #Depack the Packet
        ICMP_Header = RecICMPMessage[20:28]
        ICMPtype, ICMPCode, ICMPCheckSum, ICMPp_id, ICMP_Sequence = struct.unpack('bbHHh', ICMP_Header)

        print("ICMP Info: type=" + str(ICMPtype) + ", code=" + str(ICMPCode) + ", message:", end=' ')
        Print_ICMP_Message(ICMPtype, ICMPCode)

        # print("ICMP END")

    #If did not get any Packet
    except:
        print("",end='')  

    #Count
    i = i+1


CilentPingerSocket.close()
CilentICMPSocket.close()