# -*- coding: utf-8 -*-
import argparse
import datetime
import os, glob
from dateutil.parser import parse
from unidecode import unidecode
import string


def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False

def removeNonPrint(myStr):
    myStr = unidecode(myStr)
    return ''.join(s for s in myStr if s in string.printable)

def parseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file/dir containing conversation", required=True, default = 'lists.txt')
    parser.add_argument("-o", "--output",help="Output file/dir to save formatted conversation", required=False, default = 'out.csv') 
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parseArg()
    dataset = {}
    raw_lines = []
    count = 0

    if os.path.isfile(args.input):
        filelist = list(args.input)
        outputs = list(args.output)
    else:
        if os.path.isdir(args.input):
            filelist = glob.glob(args.input + "/*.txt")
            if os.path.isdir(args.output):
                outputs = [x.replace(".txt",".csv").replace(args.input, args.output) for x in filelist]
            else:
                outputs = [x.replace(".txt",".csv") for x in filelist]
        else:
            print("Fail to find " + args.input)
            exit()


    print("Inputs: ", end="")
    [print(x, end='; ') for x in filelist]
    print("")

    print("Outputs: ", end="")
    [print(x, end='; ') for x in outputs]
    print("")

    for filename in filelist:
        with open(filename, 'r',  encoding="utf8") as f :
            raw_lines = f.readlines()

        remove_new_lines = []
        names = {}
        user_count = 0

        
        for l in raw_lines:
            date_str = l.split(' ')[0]
            if is_date(date_str) and len(date_str) > 8:
                remove_new_lines.append(l)
            else:
                remove_new_lines[-1].join(l)

        with open(outputs[count], 'w', encoding="utf8") as f:
            f.write("NOME;DATA;HORA;MINUTO;MIDIA;MSG\n")
            for l in remove_new_lines:
                if not l.find(':', l.find('-')) == -1:

                    name = l[l.find('-')+1:l.find(':', l.find('-'))].strip()
                    name = removeNonPrint(name)
                    if not name in names.keys():
                        names[name] = user_count
                        user_count += 1

                    user = "USER_%02d" % names[name]
                    date = l.split(' ')[0]
                    time = l.split(' ')[1]
                    h = time.split(":")[0]
                    m = time.split(":")[1]
                    msg = l[l.find(':', l.find('-'))+2::].replace(';', '')
                    media = 0
                    if "<Arquivo de mídia oculto>" in msg:
                        msg = msg.replace("<Arquivo de mídia oculto>", "")
                        media = 1
                    
                    f.write("{}; {}; {}; {}; {}; {}".format(user,date,h,m,media, msg))
        
        count += 1