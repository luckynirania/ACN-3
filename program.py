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
    # print("py .\program.py -N switchpoercount -B buffersize -p packetgenprob -queue INQ | KONQ | iSLIP -K knockout -out outputfile -T maxtimeslots")
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


# Alogithm selection

if queue == 'INQ':
    print("INQ starts")
    # Here starts INQ
    InputPort = [[] for i in range(N)]
    OutputPort = [[] for i in range(N)]
    packets = []
    generated_count = 0
    transfer_count = 0
    total_delay = 0
    for _ in range(T):
        # Generate the Packet for Ports
        for i in range(N):
            x = random.random()
            if x < p and len(InputPort[i]) < B:
                packet = Packet(i, int(random.random() * N), _ + (random.random()/10))
                InputPort[i].append(packet)
                generated_count += 1

        # Calculate How many Input ports want to send packet to ouput port
        packetToOutputport = [[] for i in range(N)]
        for i in range(N):
            for j in range(len(InputPort[i])):
                packetToOutputport[InputPort[i][j].to].append(InputPort[i][j])
        
        # Packet Scheduling
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

                    OutputPort[i].append(packet)

                    InputPort[packet.frm].remove(packetToOutputport[i][index])
                    del packetToOutputport[i][index]

        # Transfer the packets
        for i in range(N):
            transfer_count += len(OutputPort[i])
            for each in OutputPort[i]:
                packets.append(each.delay)
                total_delay += each.delay
            OutputPort[i] = []

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
    packets = []
    generated_count = 0
    transfer_count = 0
    dropped_count = 0
    total_delay = 0
    OutputPort = [[] for i in range(N)]

    for _ in range(T):
        packetsToSend = [[] for i in range(N)]
        # Generate the Packet for Ports
        for i in range(N):
            x = random.random()
            if x < p:
                packet = Packet(i, int(random.random() * N), _ + (random.random()/10))
                packetsToSend[packet.to].append(packet)
                generated_count += 1
        # for each in packetsToSend:
        #     print([i.disp() for i in each])

        # print([len(each) for each in packetsToSend])
        # Packet Scheduling
        for i in range(N):
            if len(packetsToSend[i]) > 0:
                if len(packetsToSend[i]) == 1:
                    packet = copy.deepcopy(packetsToSend[i][0])
                    OutputPort[i].append(packet)
                elif len(packetsToSend[i]) > 1 and len(packetsToSend[i]) <= K:
                    for each in packetsToSend[i]:
                        packet = copy.deepcopy(each)
                        OutputPort[i].append(packet)
                else:
                    dropped_count += len(packetsToSend[i]) - K
                    random_K = [int(K*random.random()) for i in range(K)]
                    for each in random_K:
                        packet = copy.deepcopy(packetsToSend[i][each])
                        OutputPort[i].append(packet)
                packetsToSend[i] = []
        # print([len(each) for each in OutputPort])
        # Transfer
        for i in range(N):
            for each in OutputPort[i]:
                delay = int(_) - int(each.timestamp)
                total_delay += delay
                transfer_count += 1
                packets.append(delay)
            OutputPort[i] = []

    print('total delay\t', total_delay)
    print('total gener\t', generated_count)
    print('total dropp\t', dropped_count)
    print('total trans\t', transfer_count)
    print('averg delay\t', total_delay/transfer_count)
    print('devia delay\t', statistics.stdev(packets))
    print('link utiliz\t', transfer_count/(N*T))
    # print(len(packets))

    # Here ends KUOQ

if queue == 'iSLIP':
    print("iSLIP starts")
    # Here starts iSLIP
    for _ in range(T):
        # Generate the Packet for Ports
        print('lol')

    # Here ends iSLIP
