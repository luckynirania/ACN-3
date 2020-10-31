import argparse 
import sys
import random

parser = argparse.ArgumentParser() 
parser.add_argument("-N", help = "number of input and output ports")
parser.add_argument("-B", help = "size of buffer")
parser.add_argument("-p", help = "probability")
parser.add_argument("-queue", help = "INQ | KONQ | iSLIP")
parser.add_argument("-K", help = "max K packets queued per output port")
parser.add_argument("-out", help = "output file")
parser.add_argument("-T", help = "max simulation time")  

args = parser.parse_args() 

if(len(sys.argv) != 15):
    print("format is : py .\program.py -N switchpoercount -B buffersize -p packetgenprob -queue INQ | KONQ | iSLIP -K knockout -out outputfile -T maxtimeslots")
    exit()

N = int(args.N) 
B = int(args.B) 
p = float(args.p) 
queue = str(args.queue) 
K = int(args.K) 
outputfile = str(args.out) 
T = int(args.T) 

class Packet:
    def __init__(self, frm, to, timestamp):
        self.frm = frm 
        self.to = to
        self.timestamp = timestamp
    def disp(self):
        return (self.frm, self.timestamp, self.to)


Buffer = 0
InputPort = []
for _ in range(N):
    InputPort.append([])

# Here starts packet generation part

def gen_packets(_):
    global Buffer
    for i in range(N):
        x = random.random()
        if x < p and Buffer < B:
            packet = Packet(i, int(random.random() * N), _ + (random.random()/10))
            InputPort[i].append(packet)
            Buffer += 1

# Here ends packet generation part

# Alogithm selection

if queue == 'INQ':
    print("INQ starts")
    # Here starts INQ
    for _ in range(T):
        # Generate the Packet for Ports
        gen_packets(_)

        # Calculate How many Input ports want to send packet to ouput port
    # Here ends INQ

# for each in InputPort:
#     print([i.disp() for i in each])

if queue == 'KUOQ':
    print("KUOQ starts")
    # Here starts KUOQ
    for _ in range(T):
        # Generate the Packet for Ports
        gen_packets(_)

    # Here ends KUOQ

if queue == 'iSLIP':
    print("iSLIP starts")
    # Here starts iSLIP
    for _ in range(T):
        # Generate the Packet for Ports
        gen_packets(_)

    # Here ends iSLIP
# INQ
'''
Read MaxTimeSlots, NumberofPorts from command line
Initilize of the variables InputPort, OutputPort, packetToOutputport

Repeat i=1 to MaxTimeSlots

	//Generate the Packet for Ports
	Repeat NumberofPorts time
		Generate RandNumber, 
		If RandNumber is less than the Probobility(PacketGenerateProb) and Buffer is not full then
			generate a packet and store it in InputPort
	Repeat End

	// Calculate How many Input ports want to send packet to ouput port
	Repeat j=1 to NumberofPorts
		If InputPort of j > 0 Then
			Increment packetToOutputport[j]
	Repeat End

	//Packet Scheduling 

	Repeat j=1 to NumberofPorts
		If packetToOutputport[j] has packet to send
			If packetToOutputport[j] == 1 then // If no contention
				store the packet in OutputPort and remove the packet from InputPort 
				decrement packetToOutputport[j] count
				record the Delay for Port j //delay = delay + No of packets Transmitted at InputPort j
			ELSE //If there is a contention
				randomly select a packet, store it in OutputPort j for transmission and remove same the packet from InputPort 
				decrement packetToOutputport[j] count
				record the Delay for Port j //delay = delay + No of packets Transmitted at InputPort j

	Repeat End

	//Transfer the Packet
	Repeat k=1 to NumberofPorts
		IF OutputPort has packets to send
			Increment packetTransmitted count
			Clear OutputPort k
		clear packetToOutputport[k]
	Repeat End
Repeat End	

Calculate the TotalDelay, Average packet Delay, standard deviation packet delay and avg link Utilization and write into a file


'''