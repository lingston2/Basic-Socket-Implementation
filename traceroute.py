from socket import *
import time
import struct

#Target
ServerDestinationIP = "127.0.0.1"
ServerDestinationPort = 55556
TargetAddress = (ServerDestinationIP, ServerDestinationPort)

#Testing using Google
TempDestIP = gethostbyname("google.com")
TempDestPort = 55556
TempAddress = (TempDestIP, TempDestPort)

#Set MaxHops, Initial TTL, and Message
MaxHopsLimit = 30
TimetoLive = 1
message_send = "PING"

#Looping until TTL Exceeds Max Hops
while TimetoLive <= MaxHopsLimit:

    #Create and setup UDP Sockets
    UDP_Socket = socket(AF_INET, SOCK_DGRAM)
    UDP_Socket.setsockopt(SOL_IP, IP_TTL, TimetoLive)

    #Create and setup ICMP Sockets
    ICMP_Socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
    ICMP_Socket.settimeout(1)

    #Declare Variables for CurrentHost and Tries
    CurrentAddress = None
    CurrentName = None
    TriesCount = 3

    #CreateBlankList for RTT
    RTT_List = []

    #Print the Number of TTL
    print(str(TimetoLive), end=' ')

    #Send and get Message 3 times
    while TriesCount>0:
        try:
            #Get time before sending message
            SendingTime = time.time()*1000

            #Send Message
            UDP_Socket.sendto(message_send.encode(), TargetAddress)

            #Getting Message
            _, CurrentAddress = ICMP_Socket.recvfrom(512)

            #Get time after receiving message
            ReceiveTime = time.time()*1000

            #Calculate RTT and Add it to the RTT_List
            RTT_Time = ReceiveTime-SendingTime
            RTT_List.append(RTT_Time)

            #Get Host's Address
            CurrentAddress = CurrentAddress[0]

            #Try and get Host's Name
            try:
                CurrentName = gethostbyaddr(CurrentAddress)[0]
            except error:
                CurrentName = CurrentAddress
            
            TriesCount = TriesCount-1
        
        #If Error then try again, put "* " in RTT_List
        except error:
            TriesCount = TriesCount-1
            RTT_List.append("*")

    #Close The Sockets
    UDP_Socket.close()
    ICMP_Socket.close()
    
    #Flag for if Host's Name/Address has been printed
    Host_Print = False

    #Printing RTT and Host's Name/Address
    Print_Count = 0
    while Print_Count < 3:
        if RTT_List != '*' and Host_Print == False and CurrentAddress != None:
            print(CurrentName + " (" + CurrentAddress + ")", end=' ')
            Host_Print = True
            
        print(str(RTT_List[Print_Count]), end=' ')
        if RTT_List[Print_Count] != "*":
            print("ms", end=' ')
        Print_Count= Print_Count+1
    
    #Print Newline
    print("")

    #Counter for TTL
    TimetoLive = TimetoLive+1

    #End Program if we reach the destination
    if CurrentAddress == ServerDestinationIP:
        break