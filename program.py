import argparse 
import sys
import random
import copy
import statistics

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
        self.delay = 0
    def disp(self):
        return (self.frm, self.timestamp, self.to)


InputPort = [[] for i in range(N)]
OutputPort = [[] for i in range(N)]

# Here starts packet generation part

def gen_packets(_):
    generated_count = 0
    for i in range(N):
        x = random.random()
        if x < p and len(InputPort[i]) < B:
            packet = Packet(i, int(random.random() * N), _ + (random.random()/10))
            InputPort[i].append(packet)
            generated_count += 1
    return generated_count

# Here ends packet generation part

# Alogithm selection

if queue == 'INQ':
    print("INQ starts")
    # Here starts INQ
    packets = []
    generated_count = 0
    transfer_count = 0
    total_delay = 0
    for _ in range(T):
        # Generate the Packet for Ports
        generated_count += gen_packets(_)

        # Calculate How many Input ports want to send packet to ouput port
        packetToOutputport = [[] for i in range(N)]
        for i in range(N):
            for j in range(len(InputPort[i])):
                packetToOutputport[InputPort[i][j].to].append(InputPort[i][j])
        # print(packetToOutputport)

        # for each in InputPort:
        #     print([i.disp() for i in each])
        # print("-------------")

        for i in range(N):
            size = len(packetToOutputport[i])
            if size > 0:
                if size == 1:
                    packet = copy.deepcopy(packetToOutputport[i][0])
                    packet.delay = int(_) - int(packet.timestamp)
                    # print("................", packet.delay, _ , packet.timestamp)
                    OutputPort[i].append(packet)
                    # del packetToOutputport[i][0]
                    InputPort[packet.frm].remove(packetToOutputport[i][0])

                    del packetToOutputport[i][0]
                else:
                    index = int(len(packetToOutputport[i]) * random.random())
                    packet = copy.deepcopy(packetToOutputport[i][index])
                    packet.delay = int(_) - int(packet.timestamp)
                    # print("................", packet.delay, _ , packet.timestamp)
                    OutputPort[i].append(packet)
                    # del packetToOutputport[i][0]
                    InputPort[packet.frm].remove(packetToOutputport[i][index])

                    del packetToOutputport[i][index]
        # print(packetToOutputport)

        for i in range(N):
            transfer_count += len(OutputPort[i])
            for each in OutputPort[i]:
                packets.append(each.delay)
                total_delay += each.delay
            OutputPort[i] = []
            # packetToOutputport

    print('total delay\t', total_delay)
    print('total gener\t', generated_count)
    print('total trans\t', transfer_count)
    print('averg delay\t', total_delay/transfer_count)
    print('devia delay\t', statistics.stdev(packets))
    print('link utiliz\t', transfer_count/(N*T))
    # print('loi', generated_count, transfer_count, total_delay, sum(packets))
    # Here ends INQ

# for each in InputPort:
#     print([i.disp() for i in each])
# print("-------------")
# for each in OutputPort:
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