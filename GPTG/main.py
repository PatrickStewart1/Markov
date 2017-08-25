from DataHandler import *
from Generator import *

DH = DataHandler("pokemon.csv",oStrings=[" ","forme","Mega"],oStringsCaseSensetive=False,column = 2,skip = 1)
DH.__readFile__()
myGen = Generator(2,DH)
myGen.populate_x0_table()
myGen.populate_xt_table()
myGen.calculate_avg_len()
myGen.build_x0_roll_pool()
print(myGen.generate_name())
outfile = open("newfile.txt",'w')
for i in range(0,1000):
    outfile.write(myGen.generate_name() + "\n")

