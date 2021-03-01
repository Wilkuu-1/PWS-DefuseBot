#
#
#-----------------------------------------------------------------------------
# Anode - Cathode Connection Configuration File
# Versions: Anode_Server V1.1
# Import for network protocol settings and remote execution
#-----------------------------------------------------------------------------
import math

#++FUNC LINKS
#TODO find a safer way to execute functions
#WARNING: THIS EXECS THE STRINGS ENTERED, DON'T ENTER STUPID THINGS
ANfunc={
        0:("b2var(pac)"), #Default:process image
        2:("status(pac)" ),
        254:("self.ferr(254)"), #Raises error
        255:("break"), #Ends handle function
        }
CAfunc={
        0:("pass"),                     #Default:pass
        2:("keyset(pac,0)"),  #Key up
        3:("keyset(pac,1)"),  #Key down
        4:("setstatus(pac,2)"),  #Set a variable
        254:("ferr()"), #Raises unknown function error
        255:("break"),                 #Ends handle function
        }

#++END OF FUNC LINKS

#++NETWORK CONFIG
#Server setup
AADDR = ("192.168.178.30",21122)                    #Anode adress
MAX   = 65536                                  #Maximal packlet size
L_last= math.ceil(math.log(65536.0,256.0))
MBIG  = 255                                    #Maximal amount of MAX-sized(big) packlets (1 byte)
#Header length
HEADL = 1 +L_last+1 #size of /big/ + size of /last/ + size of /func/


#++END OF NETWORK CONFIG

#++NETWORK CODE

#Header functions
def MHEAD(leng,func=0): #Make a new header
    if leng > ((MBIG+1)*MAX):
        raise ValueError("PACKET TOO LARGE")
    big  = (math.floor((leng/MAX))) #amount of big paclets
    bigb = big.to_bytes(1,byteorder ='big',signed=False)
    last = leng-big*MAX
    lastb =last.to_bytes(L_last,byteorder ='big',signed=False) #size of last packlet
    func = func.to_bytes(1,byteorder='big',signed =False) #function to be called (0 for default)
    #Returns Header with layout: /big(1b)/last(2b)/func(1b)/
    head = b''.join([bigb,lastb,func])
    return head,big,last #also returns how much packlets to send

def RHEAD(head):        #Read a header
    if len(head) != HEADL:
        raise ValueError(f"INVALID HEADER LENGTH ({len(head)}/{HEADL})")
    big  = int.from_bytes(head[0:1]       ,byteorder='big', signed=False) #please patch if MBIG>255
    last = int.from_bytes(head[1:1+L_last],byteorder='big', signed=False)
    func = int.from_bytes(head[1+L_last:] ,byteorder='big', signed=False)
    return big,last,func

#Packet reciever
#Runs code from speciefied func links , see FUNC LINKS
def REC(conn,funclink=None):
    pac=[]
    head = conn.recv(4)
    big,last,func = RHEAD(head)   #get header
    conn.send(head)
    print(f"recieving {big+1} packlets")
    for p in range(big):
        pac.append(conn.recv(MAX)) #get big paclets
    pac.append(conn.recv(last))   #get last paclet
    pac= b''.join(pac)
    if funclink:#Check if funclink is given
        return funclink.get(func,(funclink.get(254))),pac,func #return things to eval
    else:
        return pac,func

#Packet Sender
def SND(conn,pac,func):
    head, big, last  = MHEAD(len(pac),func=func)
    conn.send(head)#send header
    if conn.recv(4) != head: print("ANCA: Sending packet missync")
    for x in range(0,big*MAX,MAX): #send big paclets
        conn.send(pac[x:x+MAX])
    conn.send(pac[:last])          #send last paclet

#++END OF NETWORK CODE
