import socket
import sys
import subprocess
import os

n=len(sys.argv)
type=int(sys.argv[1])
filename=sys.argv[2]
ADS_port=int(sys.argv[3])
buffersize=1024
ADS_ip=[] #list of ADS ips
counter=0
curr="List_of_" #curr is to check if the line is of the type of ADS we are looking for
f=open(filename,"r")
l=f.readlines()
for x in l:
    p=x.split(" ")
    if(counter==5):
        ADS_ip.append(p[1].strip())
        counter+=1
        if(type==1): #if type=1 then curr is List_of_ADS1
            curr+="ADS1"
    if(counter==6):
        ADS_ip.append(p[1].strip())
        counter+=1
        if(type==2): #if type=2 then curr is List_of_ADS2
            curr+="ADS2"
    if(counter==7):
        ADS_ip.append(p[1].strip())
        counter+=1
        if(type==3): #if type=3 then curr is List_of_ADS3
            curr+="ADS3"
    if(counter==8):
        ADS_ip.append(p[1].strip())
        counter+=1
        if(type==4): #if type=4 then curr is List_of_ADS4
            curr+="ADS4"
    if(counter==9):
        ADS_ip.append(p[1].strip())
        counter+=1
        if(type==5): #if type=5 then curr is List_of_ADS5
            curr+="ADS5"
    if(counter==10):
        ADS_ip.append(p[1].strip())
        counter+=1
        if(type==6): #if type=6 then curr is List_of_ADS6
            curr+="ADS6"
        break
    if(counter<5):
        counter+=1
f.close()
ADSfile=open("ADS_output.txt","a")
ADSfile.truncate(0)
UDPserversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
UDPserversocket.bind((ADS_ip[type-1],ADS_port))

#print("ADS-server running")
while(True):
    msgfromclient=UDPserversocket.recvfrom(buffersize) #receiving message from NR
    clientmessage=msgfromclient[0].decode()
    clientaddress=msgfromclient[1]
    if(clientmessage=="bye"):
        #ADSfile.write("query: "+clientmessage+" response: none\n")
        break
    c=0 #c is to check if the line is of the type of ADS we are looking for(c=1 means we found the ADS)
    msg="not found"
    f=open(filename,"r")
    l=f.readlines()
    for x in l:
        if(c==0):
            if(x.strip()==curr): #if the line is of the type of ADS we are looking for, then c=1
                c=1
                continue
        if(c==1):
            p=x.split(" ")
            q=x.split("_")
            #print("from ads-"+str(len(p))+" "+str(len(q)))
            if(len(q)==3 or len(q)==2): #loop until next ADS list line is reached or END_DATA is reached 
                break
            if(p[0].strip()==clientmessage): #check if the message from NR is present in the ADS list
                msg=p[1].strip() #if present, then send the corresponding IP address
                break
    f.close()
    ADSfile.write("query: "+clientmessage+" response: "+msg+"\n")
    UDPserversocket.sendto(msg.encode(),clientaddress)
    
ADSfile.close()
UDPserversocket.close()