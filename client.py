import socket
import sys
import subprocess
import os
buffersize=1024
#sendmsg="Hello from Client"
#bytessendmsg=bytes(sendmsg,'utf-8')
n=len(sys.argv)
if(n<3):
    print("Error-Less arguments")
    
elif(os.path.isfile(sys.argv[1])==False):
    print("Error-File not found")    #errors

else:
  filename=sys.argv[1]
  k=int(sys.argv[2])
  p=subprocess.Popen(["python", "NR.py",filename,str(k+53)]) #starting the servers using subprocess module
  p=subprocess.Popen(["python", "RDS.py",filename,str(k+54)])
  p=subprocess.Popen(["python", "TDS.py","1",filename,str(k+55)])
  p=subprocess.Popen(["python", "TDS.py","2",filename,str(k+56)])
  p=subprocess.Popen(["python", "ADS.py","1",filename,str(k+57)])
  p=subprocess.Popen(["python", "ADS.py","2",filename,str(k+58)])
  p=subprocess.Popen(["python", "ADS.py","3",filename,str(k+59)])
  p=subprocess.Popen(["python", "ADS.py","4",filename,str(k+60)])
  p=subprocess.Popen(["python", "ADS.py","5",filename,str(k+61)])
  p=subprocess.Popen(["python", "ADS.py","6",filename,str(k+62)])
  f=open(filename,"r") #open test file to read the ip addresses
  l=f.readlines()
  serverip=" "
  for x in l:
    p=x.split(" ")
    if(p[0]=="NR"):
        serverip=p[1].strip()    #getting out the NR server ip
        break
  f.close()
  serveraddressport=(serverip,k+53) #NR is the server
  UDPclientsocket=socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
  while(True):
      sendmsg=input("Enter server name(or bye to exit):")
      if(sendmsg=='bye'): #if bye then send bye to all servers and exit
          counter=0
          f=open(filename,"r") #open test file to read the ip addresses
          l=f.readlines()      #read the file
          for x in l:
            p=x.split(" ")
            if(p[0]=="NR"):   
               serverip=p[1].strip()
               counter+=1
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+53)) #send bye to NR server
            if(p[0]=="RDS"):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+54)) #send bye to RDS server
            if(p[0]=="TDS_com"):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+55)) #send bye to TDS_com server
            if(p[0]=="TDS_edu"):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+56)) #send bye to TDS_edu server
            if(counter==4):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+57)) #send bye to ADS1 server
            if(counter==5):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+58)) #send bye to ADS2 server
            if(counter==6):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+59)) #send bye to ADS3 server
            if(counter==7):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+60)) #send bye to ADS4 server
            if(counter==8):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+61)) #send bye to ADS5 server
            if(counter==9):
               counter+=1
               serverip=p[1].strip()
               UDPclientsocket.sendto(str.encode(sendmsg),(serverip,k+62))   #send bye to ADS6 server
               break
          f.close()
          break
      bytestosend=str.encode(sendmsg) #send the encoded server name to NR server
      UDPclientsocket.sendto(bytestosend,serveraddressport) 
      msgfromserver=UDPclientsocket.recvfrom(buffersize) #receive the response from NR server
      if(msgfromserver[0].decode()=="not found"): #if not found then print not found
          print("No DNS record found")
      else:
        msg = "DNS mapping: {}".format(msgfromserver[0].decode()) #else print the response
        print(msg)
  UDPclientsocket.close() #close the socket