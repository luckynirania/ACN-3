ReadMe

Lokesh Nirania, 170010009
Hritik Kumar,   170010013


=============
How to Run
=============

The program from python
python3 program.py -N switchpoercount -B buffersize -p packetgenprob -queue INQ | KONQ | ISLIP -K knockout -out outputfile -T maxtimeslots

Script to run as default values
./run.sh


=============
OutPut Interpretation
=============

Output will be displayed and written in file provided in command line arguement as follows

N   P       Qtype   AvgPD               Std. Dev of PD      Avg LU
4	0.8	    KOUQ	0.30851063829787234	0.15425531914893617	0.564
8	0.8	    KOUQ	0.6419246549794853	0.22695463827341444	0.67025
16	0.8	    KOUQ	0.7731391010836738	0.19328477527091845	0.703625

Where 

N - Number of Input and Output Port

P - Packet Generation Probability

Qtype - INQ or KOUQ or ISLIP

AvgPD - Average packet delay
	AvgPktDelay=(TotalDelay*1.0)/(PacketTransmitted*1.0)
Std. Dev of PD - Standard Deviation of Packet Delay
	StdDevPacketDelay=AvgPktDelay/sqrt(PacketTransmitted*1.0)

Avg LU - Average Link Utilization
	AvgLinkUtilization=(PacketTransmitted*1.0)/((maxtimeslots*1.0)*(NumberofPorts*1.0))

A technical Report - Refer to Technical Report Requirements.
