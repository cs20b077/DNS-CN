import socket
import sys
import subprocess
import os

n=len(sys.argv) #number of arguments
filename=sys.argv[1]   #filename
NRport=int(sys.argv[2]) #port number
buffersize=1024
f=open(filename,"r") #open file
l=f.readlines()
localip=""
RDS_ip=""
for x in l:
    p=x.split(" ")
    if(p[0]=="NR"): #get local ip
        localip=p[1].strip()
    elif(p[0]=="RDS"): #get RDS ip
        RDS_ip=p[1].strip()
        break
f.close()
#print(localip)
#print(NRport)
UDPserversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) #create socket
UDPserversocket.bind((localip,NRport))  #bind socket

#print("NR-server running")
NRfile=open("NR_output.txt","a")
NRfile.truncate(0)
randomsocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) #create socket

while(True):
    msgfromclient=UDPserversocket.recvfrom(buffersize) #receive message from client
    clientmessage=msgfromclient[0].decode() #decode message
    clientaddress=msgfromclient[1] #get client address
    if(clientmessage=="bye"): #if client sends bye, then break
        #NRfile.write("query: "+clientmessage+" response: none\n")
        break
    
    #send to rds
    bytestosend=str.encode(clientmessage) #encode message
    randomsocket.sendto(bytestosend,(RDS_ip,NRport+1)) #send to RDS
    msgfrom_rds=randomsocket.recvfrom(buffersize) #receive message from RDS
    if(msgfrom_rds[0].decode()=="not found"): #if RDS sends not found, then send not found to client
        UDPserversocket.sendto(msgfrom_rds[0],clientaddress) #send not found to client
        continue
    msg=(msgfrom_rds[0].decode()).split("+")   #split message with + to get ip and port
    TDSaddress=msg[0]  #get TDS ip
    TDSport=msg[1] #get TDS port
    
    #send to TDS
    randomsocket.sendto(bytestosend,(TDSaddress,int(TDSport))) #send to TDS
    msgfrom_tds=randomsocket.recvfrom(buffersize) #receive message from TDS
    if(msgfrom_tds[0].decode()=="not found"): #if TDS sends not found, then send not found to client
        UDPserversocket.sendto(msgfrom_tds[0],clientaddress) #send not found to client
        continue
    msg=(msgfrom_tds[0].decode()).split("+") #split message with + to get ip and port
    ADSaddress=msg[0]   #get ADS ip
    ADSport=msg[1]  #get ADS port
    
    #send to ADS
    randomsocket.sendto(bytestosend,(ADSaddress,int(ADSport))) #send servername to corresponding ADS
    msgfrom_ads=randomsocket.recvfrom(buffersize)   #receive message from ADS
    msg=msgfrom_ads[0].decode() #decode message
    #clientMsg = "Message from Client: {}".format(message)
    #clientIP  = "Client IP Address: {}".format(address)
    #print(clientMsg)
    # print(clientIP)
    
    NRfile.write("query: "+clientmessage+" response: "+msg+"\n")
    UDPserversocket.sendto(msg.encode(),clientaddress) #send message to client
    
NRfile.close()
UDPserversocket.close()
randomsocket.close()