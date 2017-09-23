"""
Main program for clustering gene expression data
"""

from sys import *
from clustering import *

def output(k, names, means, probabilities):
    outfile = open(("input/"+argv[2]+".out"), "w")
    outfile.write(str(k)+"\n")
    for i in range(k):
        outfile.write(str(means[i])+"\n")
        for j in range(probabilities.shape[0]):
            print probabilities.shape
            print j
            belongs = True
            for m in range(k):
                if probabilities[j][i] < probabilities[j][m]:
                    belongs = False
                    break
            if belongs:
                if len(names) != 0:
                    outfile.write(str(names[j])+"\n")
                else:
                    outfile.write(str(j)+"\n")
    outfile.close()

def parse():
    if len(argv)!= 4:
         print "wrong number of arguments; correct usage: python ..."
         exit(1)
    try:
        k = int(argv[1])
        filename = "input/"+argv[2]+".csv"

        infile = open(filename, "r")
        plist = []

        for entry in infile:

            line = entry.strip()
            line = line.split(",")
            floats = [float(i) for i in line]

            plist.append(floats)
        names = []
        if argv[3] == "1":
            filename = "input/"+argv[2]+".names"
            infile = open(filename, "r")

            for entry in infile:

                line = entry.strip()
                names.append(line)
        elif argv[3] != "0":
            exit(1)
        return k, plist, names

    except:
        print "failed :( :(\ncorrect usage: python gene_cluster k dataset boolean(whether or not to load names of data)"
        exit(1)

def main():
    (k, data, names) = parse()
    normiedata = normalization(data)
    (means, probabilities) = EM(normiedata, k)
    output(k, names, means, probabilities)
    sse = SSE(means, np.array(normiedata))
    aic = AIC(sse, k, np.array(normiedata).shape[1])
    print """
    Fitting Gaussian Mixture Model using EM with k=%d

    SSE:      %f
    AIC:      %f
    """ %(k, sse, aic)
    
main()
