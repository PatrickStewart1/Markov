import numpy as np

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
        self.__scrub_data__()

    def __scrub_data__(self): #current implementation accepts only ascii chars, remove all others
        for word in self.data:
            for i in range(0,len(word)):
                if ord(word[i]) > 255:
                    self.data.remove(word)
