import numpy as np

class Generator:
    def __init__(self,sLen,dHandler):
        self.series_length = sLen
        self.data_handler = dHandler

    def populate_x0_table(self):
        if self.series_length == 1:
            self.x0_freq_table = np.zeros([256])
        elif self.series_length == 2:
            self.x0_freq_table = np.zeros([256,256])
        elif self.series_length >= 3:
            self.x0_freq_table = np.zeros([256,256,256])
        #Series length > 3 produces too large of an array with 256 possible chars
        #for series length > 3 use something like 128, 52, 36, or 26 chars
        else:
            print("WARNING: invalid series_length " + str(self.series_length))

def contains(str,substrs,caseSensetive):
    if caseSensetive == False:
        for substr in substrs:
            if substr.upper() in str.upper():
                return True
    else:
        for substr in substrs:
            if substr in str:
                return True
    return False

class DataHandler:
    def __init__(self,infileName,oStrings,oStringsCaseSensetive = False,column = -1,skip = 0):
        self.input_filename = infileName
        self.omitted_Substrings = oStrings  # words containing omitted substrings will be ignored
        self.omitted_Substrings_isCaseSensetive = oStringsCaseSensetive
        self.desired_column = column # in the case of a multi-columned dataset,
                                     # the user can input which column they are interested in,
                                     # user must specify delimeter
        self.skip_first_line = skip  #user might want to skip a line containing column labels

    def __readFile__(self):
        self.data = tuple(open(self.input_filename))
        if self.desired_column != -1:
            temp = []
            for n in range (self.skip_first_line,len(self.data)):
                string_ = self.data[n].split(",")[self.desired_column - 1]
                if contains(string_,self.omitted_Substrings,self.omitted_Substrings_isCaseSensetive) == False:
                    temp.append(string_)
        self.data = temp

DH = DataHandler("pokemon.csv",["sAur","SQuIr","Mega"],False,column = 2,skip = 1)
DH.__readFile__()
myGen = Generator(1,DH)
print(myGen.data_handler.data)

