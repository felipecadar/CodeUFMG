import sys, os, random

ops = ('Sub', 'Add', 'Max', 'Min', 'Sum')

vecsize    = (int)(sys.argv[1])
operations = (int)(sys.argv[2])

infile  = open('test_v' + str(vecsize) + '_op' + str(operations) + '.in' , 'w');
# outfile = open('test_v' + str(vecsize) + '_op' + str(operations) + '.out', 'w');

vec = []

for x in xrange(vecsize):
    vec.append(random.randint(0,vecsize))

infile.write(str(vecsize) + ' ' + str(operations) + '\n')

for x in xrange(vecsize):
    infile.write(str(vec[x])+' ')
infile.write('\n')

for x in xrange(operations):
    init =  random.randint(1,vecsize)
    final = random.randint(init,vecsize)
    o = random.randint(0,len(ops)-1)

    infile.write(str(ops[o]) + ' ' + str(init) + ' ' + str(final) + '\n' )
    
    # if o == 2:
    #     outfile.write(str(max(vec[init:final+2])) + '\n')
    # if o == 3:
    #     outfile.write(str(min(vec[init:final+2]) )+ '\n')
    # if o == 4:
    #     outfile.write(str(sum(vec[init:final+2])) + '\n')
