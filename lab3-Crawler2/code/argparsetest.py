import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a")
parser.add_argument("-b")
args = parser.parse_args()

if args.a == 'magic.name':
    print ('You nailed it!')

if(args.b == "hello"):
    print("b suc!")

