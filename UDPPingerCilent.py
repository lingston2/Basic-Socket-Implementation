from socket import *
import time

#Declaration
i = 1
Received_Ping = 0
Total_Ping_RTT_Count = 0

# Self Server
ServerDestinationIP = "127.0.0.1" 
ServerDestinationPort = 8080   

# Target Server   
TargetAddress = (ServerDestinationIP, ServerDestinationPort)

# Create UDP Socket, named CilentPingerSocket
CilentPingerSocket = socket(AF_INET, SOCK_DGRAM)

#CilentPingerSocket.bind((ServerDestinationIP, ServerDestinationPort))

#Set Timeout
CilentPingerSocket.settimeout(1)

while i<11:
    #Time that the message was sent
    CurrentTime = time.time()*1000

    #Message Content
    message_send = 'PING ' + str(i) + ' ' + str(CurrentTime)

    #send the Message (Encoded) to the Target Address
    CilentPingerSocket.sendto(message_send.encode(), TargetAddress)
    try:
        #Receive Message from Target Server
        RecMessage, serverAdd = CilentPingerSocket.recvfrom(1024)

        #Get the Received Time for Message
        RecieveTime = time.time()*1000

        #Count Total Received Ping, RTT & Total Ping
        Received_Ping = Received_Ping+1
        RoundTripTime = RecieveTime-CurrentTime
        Total_Ping_RTT_Count= Total_Ping_RTT_Count+RoundTripTime

        #Print the Received Message "RecMessage" 
        print(RecMessage.decode()[0:4], " ", str(i), " ", RoundTripTime)

    #If Timeout, Print "Request Timed Out"
    except timeout:
        print ("Request Timed Out")
        #print(i)

    #Counter
    i = i+1
    #print(i)


print("Average RTT :", round(Total_Ping_RTT_Count/Received_Ping,3))
print("Packet Loss Rate: ", (10-Received_Ping)/10)

#Close the Socket
CilentPingerSocket.close()