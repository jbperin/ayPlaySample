
from LetItWhip import Out
OUTPUT_FILENAME     = 'src/soundbuf.s'
OUTPUT_MACRO        = 'src/nbsample.h'

START_CHAN_A    = 12 # 9
START_CHAN_B    = 12 # 12
START_CHAN_C    = 12 # 15


from codegen import buffer2asmCode
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_RATE = 4000

FREQUENCE_PROCESSEUR = 1000000

NB_CYCLE_01 = 5
NB_CYCLE_02 = 12
NB_CYCLE_03 = 14

DELAY_01 = NB_CYCLE_02/FREQUENCE_PROCESSEUR 
DELAY_02 = NB_CYCLE_03/FREQUENCE_PROCESSEUR 

NB_VAL = 16

def extractValueSet3(model):
    allval = []
    for li in model:
        for li2 in li:
            allval.extend(li2)
    return allval


tab3 = [[[ (k, j, i) for i in range(j, NB_VAL)] for j in range (k, NB_VAL)] for k in range (NB_VAL)]
S3 = extractValueSet3(tab3)
S3.sort(key=lambda val: val[0]*NB_VAL*NB_VAL+val[1]*NB_VAL+val[2])
#print (S3)
I3 = [NB_VAL*NB_VAL*i+NB_VAL*j+k for (i,j,k) in S3]
#print (I3)

nxtS3 = []
for ii in range(len(S3)):
    nxtS3.append([0]*3*16)
    (a, b, c) = S3[ii]
    for inp in range (NB_VAL):
        ltmp = sorted([inp, b, c])
        ins = NB_VAL*NB_VAL*ltmp[0] + NB_VAL*ltmp[1] + ltmp[2]
        nxtS3[-1][inp] = I3.index(ins)

        ltmp = sorted([a, inp, c])
        ins = NB_VAL*NB_VAL*ltmp[0] + NB_VAL*ltmp[1] + ltmp[2]
        nxtS3[-1][inp+16] = I3.index(ins)

        ltmp = sorted([a, b, inp])
        ins = NB_VAL*NB_VAL*ltmp[0] + NB_VAL*ltmp[1] + ltmp[2]
        nxtS3[-1][inp+32] = I3.index(ins)

vol = [2**((x-15)/2) for x in range (NB_VAL)]
vol [0] = 0

curV3 = []
for i in range(len(S3)):
    curV3.append([0]*3*16)
    for inp in range (NB_VAL):
        curV3[-1][inp]      = sum([vol [v] for v in list(S3[nxtS3[i][inp]])])
        curV3[-1][inp+16]   = sum([vol [v] for v in list(S3[nxtS3[i][inp+16]])])
        curV3[-1][inp+32]   = sum([vol [v] for v in list(S3[nxtS3[i][inp+32]])])


vol = [2**((x-15)/2) for x in range (NB_VAL)]
vol [0] = 0

def model (state):
    res = sum([vol [v] for v in state])
    return res


def main ():

    print (len(Out), " echantillons" )
    # print (Out)

    wrt1 = [(0,START_CHAN_A)]
    wrt2 = [(1,START_CHAN_B)]
    wrt3 = [(2,START_CHAN_C)]

    (idx, val) = Out[0]
    if idx == 0:
        wrt1[0]=(idx, val)
    elif idx == 1:
        wrt2[0]=(idx, val)
    elif idx == 2:
        wrt3[0]=(idx, val)
    else:
        print ("ERROR")

    ii = 0
    for (idx, val) in Out[1:]:
        if (ii==0):
            wrt1.append ((idx, val))
        elif (ii==1):
            wrt2.append ((idx, val))
        elif (ii==2):
            wrt3.append ((idx, val))
        else :
            print ("ERROR")
        ii = (ii + 1)%3

    bwrt1 = [(idx+8)*16+val for (idx, val) in wrt1]
    bwrt2 = [(idx+8)*16+val for (idx, val) in wrt2]
    bwrt3 = [(idx+8)*16+val for (idx, val) in wrt3]

    with open (OUTPUT_MACRO, 'w') as f:
        f.write('#define NB_SAMPLE %d\n'%len(bwrt1))

    with open (OUTPUT_FILENAME, 'w') as f:
        f.write(".text\n")
        f.write("\n.dsb 256-(*&255)\n" + buffer2asmCode("bwrt1", bwrt1) + '\n')
        f.write("\n.dsb 256-(*&255)\n" + buffer2asmCode("bwrt2", bwrt2) + '\n')
        f.write("\n.dsb 256-(*&255)\n" + buffer2asmCode("bwrt3", bwrt3) + '\n')

    # nb_sample = round((len(Out)-1)/3)
    # period = 1.0/SAMPLE_RATE
    # duration = nb_sample*period
    # # new_number_of_samples = round(nb_sample * float(new_rate) / SAMPLE_RATE)

    # origtimes = np.linspace(0, duration, nb_sample, endpoint=True)

    # new_times=[0]
    # for tim in origtimes[1:]:
    #     new_times.append (tim - DELAY_01 - DELAY_02)
    #     new_times.append (tim - DELAY_01)
    #     new_times.append (tim)

    # np_new_times = np.array(new_times)
    # print (len(new_times))
    # V = [0] * len(np_new_times)
    # # for t in range (len(np_new_times)):
    # #    V[t] = curV3[P[t]][I[t]] 

    # S=[9, 12, 15]

    # chanA = []
    # chanB = []
    # chanC = []

    # ii = 0
    # for t in range (len(np_new_times)):
    #     (idx, ValSx) = Out[t]
    #     S[idx] = ValSx
    #     # print (ii, Out[t], new_times[t] , model(S))
    #     V[t] = model(S)
    #     if (ii%3 == 0):
    #         chanA.append(S[0])
    #         chanB.append(S[1])
    #         chanC.append(S[2])
    #     ii +=1
    # print (len(chanA), len(chanB), len(chanC))
    # print (chanA)
    # print (chanB)
    # print (chanC)    


    # realV = [0] * len(np_new_times)
    # ii = 0
    # jj = 0
    # realV[0] = model([chanA[0], chanB[0], chanC[0]])
    # for t in range (1,len(np_new_times)):
    #     # print (ii, Out[t], new_times[t] , model(S))
    #     if (ii==0):
    #         realV[t] = model([chanA[jj+1], chanB[jj], chanC[jj]])
    #     elif (ii==1):
    #         realV[t] = model([chanA[jj+1], chanB[jj+1], chanC[jj]])
    #     elif (ii==2):
    #         realV[t] = model([chanA[jj+1], chanB[jj+1], chanC[jj+1]])
    #     else : 
    #         print ("ERROR")
    #     ii = (ii + 1)%3
    #     if (ii == 0): jj += 1

    # plt.figure(1)
    # plt.title("loop")
    # plt.plot(new_times, V, '-o' )

    # plt.figure(2)
    # plt.plot(new_times, realV, '-o' )
    # print (len(V), len(realV))
    # print (V)
    # print (realV)
    # plt.show()




if __name__ == '__main__':
    main()
