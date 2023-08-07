import socket
import sys
import subprocess
import os

n=len(sys.argv) #number of arguments
filename=sys.argv[1]    #filename
RDSport=int(sys.argv[2])   #RDS port
buffersize=1024
localip=" "
TDScom_ip=" "
TDSedu_ip=" "
f=open(filename,"r")
l=f.readlines()
for x in l:
    p=x.split(" ")
    if(p[0]=="RDS"):  #RDS ip
        localip=p[1].strip()
    elif(p[0]=="TDS_com"): #TDS_com ip
        TDScom_ip=p[1].strip()
    elif(p[0]=="TDS_edu"):  #TDS_edu ip
        TDSedu_ip=p[1].strip()
        break
f.close()  
RDSfile=open("RDS_output.txt","a")
RDSfile.truncate(0)
UDPserversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) #creating socket
UDPserversocket.bind((localip,RDSport)) #binding socket

#print("RDS-server running")

while(True):
    msgfromclient=UDPserversocket.recvfrom(buffersize) #receiving message from client
    clientmessage=msgfromclient[0].decode() #decoding message
    clientaddress=msgfromclient[1] #client address
    if(clientmessage=="bye"): #if client sends bye, then break
        #RDSfile.write("query: "+clientmessage+" response: none\n")
        break
    temp=clientmessage.split(".") #splitting message
    msg=" "
    if(temp[2]=="com"): #if client message is com, then send TDScom_ip and TDSport
        TDSport=RDSport+1 #TDScom port
        msg=TDScom_ip+"+"+str(TDSport) #message is a string of ip+port
    elif(temp[2]=="edu"): #if client message is edu, then send TDSedu_ip and TDSport
        TDSport=RDSport+2 #TDSedu port
        msg=TDSedu_ip+"+"+str(TDSport) 
    else:
        msg="not found"
        #print("not found-RDS")
    RDSfile.write("query: "+clientmessage+" response: "+msg+"\n")
    UDPserversocket.sendto(msg.encode(),clientaddress)
    
RDSfile.close()
UDPserversocket.close()