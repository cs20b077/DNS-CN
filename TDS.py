import socket
import sys
import subprocess
import os

n=len(sys.argv)
type=int(sys.argv[1])
filename=sys.argv[2]
TDS_port=int(sys.argv[3])
buffersize=1024
TDS_ip=[] #list of TDS ips
f=open(filename,"r")
l=f.readlines()
for x in l:
    p=x.split(" ")
    if(p[0].strip()=="TDS_com"):
        TDS_ip.append(p[1].strip()) #appending TDS_com ip
    if(p[0].strip()=="TDS_edu"):
        TDS_ip.append(p[1].strip()) #appending TDS_edu ip
        break
f.close()
TDS_file=open("TDS_output.txt","a")
TDS_file.truncate(0)
UDPserversocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
UDPserversocket.bind((TDS_ip[type-1],TDS_port)) #binding TDS ip and port (ip depends on type of TDS,type=1 for TDS_com,type=2 for TDS_edu)

#print("TDS-server running")

while(True):
    msgfromclient=UDPserversocket.recvfrom(buffersize) #receiving message from NR
    clientmessage=msgfromclient[0].decode() #decoding message
    clientaddress=msgfromclient[1] #client address
    c=2 #c=2 for type=1 and c=1 for type=2
    if(type==2):
        c=1
    if(clientmessage=="bye"): #if client sends bye, then close this server
        #TDS_file.write("query: "+clientmessage+" response: none\n")
        break
    temp=clientmessage.split(".")
    temp1=temp[1].strip()+"."+temp[2].strip()
    counter=0
    msg=" "
    f=open(filename,"r")
    l=f.readlines()
    for x in l:
      p=x.split(" ")
      if(counter==5):
          if(temp1==p[0].strip()):
              msg=p[1].strip()+"+"+str(c+TDS_port) #message is a string of ip+port(of ADS1)
              break
          else:
              c+=1 #c is offset
              counter+=1
      elif(counter==6):
          if(temp1==p[0].strip()):
              msg=p[1].strip()+"+"+str(c+TDS_port) #message is a string of ip+port(of ADS2)
              break
          else:
              c+=1
              counter+=1
      elif(counter==7):
          if(temp1==p[0].strip()):
              msg=p[1].strip()+"+"+str(c+TDS_port) #message is a string of ip+port(of ADS3)
              break
          else:
              c+=1
              counter+=1
      elif(counter==8):
          if(temp1==p[0].strip()):
              msg=p[1].strip()+"+"+str(c+TDS_port) #message is a string of ip+port(of ADS4)
              break
          else:
              c+=1
              counter+=1
      elif(counter==9):
          if(temp1==p[0].strip()):
              msg=p[1].strip()+"+"+str(c+TDS_port) #message is a string of ip+port(of ADS5)
              break
          else:
              c+=1
              counter+=1
      elif(counter==10):
          if(temp1==p[0].strip()):
              msg=p[1].strip()+"+"+str(c+TDS_port) #message is a string of ip+port(of ADS6)
              break
          else:
              c+=1
              counter+=1
      elif(counter>10): #if such ADS file is not found
          msg="not found"
          #print("not found-TDS")
          break
      if(counter<5):
          counter+=1 #first 5 lines are not required(get to ADS)
    f.close()
    TDS_file.write("query: "+clientmessage+" response: "+msg+"\n")
    UDPserversocket.sendto(msg.encode(),clientaddress)
    
TDS_file.close()
UDPserversocket.close()