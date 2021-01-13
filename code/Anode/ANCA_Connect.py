#
#
#-----------------------------------------------------------------------------
# Anode - Cathode Connection Configuration File 
# Versions: Anode_Server V1.1
# Import for network protocol settings and func functions 
#-----------------------------------------------------------------------------
import math

#++FUNC LINKS
#WARNING: THIS EVALS THE STRINGS ENTERED, DON'T ENTER STUPID THINGS
ANfunc={
        0:("func = b2var","args = (pac)"), #Default:process image
        1:("next = True"),
        254:("func = self.ferr","args = (head[2])"), #Raises error
        255:("func = break"), #Ends handle function 
        }
CAfunc={
        0:("func = pass")
        }

#++END OF FUNC LINKS

#++NETWORK CONFIG 
#Server setup 
AADDR = ("127.0.0.1",21122)  #Anode adress
MAX   = 65536       #Maximal packlet size
L_last= math.ceil(math.log(65536,255))
MBIG  = 255         #Maximal amount of MAX-sized(big) packlets (1 byte)
#Header length
HEADL = 1 +L_last+1 #size of /big/ + size of /last/ + size of /func/ 


#++END OF NETWORK CONFIG

#++NETWORK CODE

#Header functions
def MHEAD(leng,func=0): #Make a new header
    if leng > ((MBIG+1)*MAX):
        raise ValueError("PACKET TOO LARGE")
    big  = bytes(math.floor((leng/MAX))) #amount of big paclets
    last = (leng % MAX).to_bytes() #size of last packlet
    func = bytes(func) #function to be called (0 for default)
    #Layout: /big/last/func/
    return b''.join([big,last,func]),big,last #also returns how much packlets to send

def RHEAD(head):        #Read a header
    if len(head) != LHEAD:
        raise ValueError("INVALID HEADER LENGTH")
    big  = int.from_bytes(head[0],          signed=False) #please patch if MBIG>255
    last = int.from_bytes(head[1:1+L_last], signed=False)
    func = int.from_bytes(head[1+L_last:],  signed=False)
    return (big,last,func)

#Packet reciever
#Runs code from speciefied func links , see FUNC LINKS
def REC(conn,funclink=None):
    pac=b''
    head = RHEAD(self.request.recv(HEADL))   #get header
    for p in range(head[0]):
        pac = b''.join([pac,conn.recv(MAX)]) #get big paclets
    pac=b''.join([pac,conn.recv(head[1])])   #get last paclet
    if funclink:#Check if funclink is given
        func = print
        args = ("Blank function call, probably really bad")
        return funclink.get(head[2],(funklink.get(254))),pac,head #return things to eval

#Packet Sender
def SND(conn,pac,func):
    head, big, last  = MHEAD(len(pac),func=func)
    conn.send(head)                #send header
    for x in range(0,big*MAX,MAX): #send big paclets
        conn.send(pac[x:x+MAX])
    conn.send(pac[:last])          #send last paclet

#++END OF NETWORK CODE
