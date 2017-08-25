import numpy as np
import random

class Generator:
    def __init__(self,sLen,dHandler):
        self.series_length = sLen
        self.data_handler = dHandler

    def populate_x0_table(self):
        if self.series_length == 1:
            self.x0_freq_table = np.zeros([256])
            for i in range (0,len(self.data_handler.data)):
                self.x0_freq_table[ord(self.data_handler.data[i][0])] += 1
        elif self.series_length == 2:
            self.x0_freq_table = np.zeros([256,256])
            for i in range (0,len(self.data_handler.data)):
                self.x0_freq_table[ord(self.data_handler.data[i][0])][ord(self.data_handler.data[i][1])] += 1
        elif self.series_length >= 3:
            self.x0_freq_table = np.zeros([256,256,256])
        #Series length > 3 produces too large of an array with 256 possible chars
        #for series length > 3 use something like 128, 52, 36, or 26 chars
        else:
            print("WARNING: invalid series_length " + str(self.series_length))

    def populate_xt_table(self):
        if self.series_length == 1:
            self.xt_freq_table = np.zeros([256,256])
            for i in range (0,len(self.data_handler.data)):
                #print(i)
                for j in range (0,len(self.data_handler.data[i])-1):
                    #print(self.data_handler.data[i])
                    #print(j)
                    self.xt_freq_table[ord(self.data_handler.data[i][j])][ord(self.data_handler.data[i][j+1])] += 1
        elif self.series_length == 2:
            self.xt_freq_table = np.zeros([256,256,256])
            for i in range(0,len(self.data_handler.data)):
                for j in range(0,len(self.data_handler.data[i])-2):
                    self.xt_freq_table[ord(self.data_handler.data[i][j])][ord(self.data_handler.data[i][j+1])][ord(self.data_handler.data[i][j+2])] += 1

    def calculate_avg_len(self):
        number_of_data = 0
        total_len = 0
        for i in range(0,len(self.data_handler.data)):
            number_of_data += 1
            total_len += len(self.data_handler.data[i])
        self.avg_len = total_len / number_of_data

    def build_x0_roll_pool(self):
        if self.series_length == 1:
            self.x0_roll_pool = []  # np.zeros([1,len(self.x0_freq_table) * len(self.x0_freq_table[0])])
            # xt_roll_pool = []
            for i in range(0, len(self.x0_freq_table)):
                for j in range(0,int(self.x0_freq_table[i])):
                    self.x0_roll_pool.append(chr(i))
        elif self.series_length == 2:
            self.x0_roll_pool = []
            for i in range(0,len(self.x0_freq_table)):
                for j in range(0,len(self.x0_freq_table[i])):
                    for k in range(0,int(self.x0_freq_table[i][j])):
                        self.x0_roll_pool.append(chr(i)+chr(j))

    def build_xt_roll_pool(self,char):

        if self.series_length == 1:
            row = self.xt_freq_table[ord(char)]
            a = (chr(0),row[0])
            b = (chr(0),row[0])
            c = (chr(2),row[2])
            d = (chr(3),row[3])


            for i in range(0,len(row)): #heh
                if (row[i] > a[1]):
                    a = (chr(i),row[i])
            for i in range(0,len(row)):
                if (row[i] > b[1] and (chr(i),row[i]) != a and row[i]):
                    b = (chr(i),row[i])
            for i in range(0,len(row)):
                if (row[i] > c[1] and (chr(i),row[i]) != b and (chr(i),row[i]) != a and row[i]):
                    c = (chr(i),row[i])
            for i in range(0,len(row)):
                if (row[i] > d[1] and (chr(i),row[i]) != c and (chr(i),row[i]) != b and (chr(i),row[i]) != a):
                    d = (chr(i),row[i])

            self.xt_roll_pool = [a,b,c,d] #note, if any x0 is the only instance of that x0 AND that x0 is the only
                                          #character in its data entry, then this function will return all 0s which
                                          #might lead to an infinite loop
        elif(self.series_length == 2):
            self.xt_roll_pool = []
            row = self.xt_freq_table[ord(char[0])][ord(char[1])]
            a = (chr(0),row[0])
            b = c = a

            for i in range(0,len(row)):
                    if row[i] > a[1]:
                         a = (chr(i),row[i])
            for i in range(0,len(row)):
                    if row[i] > b[1] and (chr(i),row[i]) != a:
                         b = (chr(i),row[i])
            for i in range(0,len(row)):
                    if row[i] > c[1] and (chr(i),row[i]) != a and (chr(i),row[i]) != b:
                         c = (chr(i),row[i])

            self.xt_roll_pool = [a,b,c]


    def choose_length(self):
        rand = np.random.randint(1,10)
        if rand < 2:
            return round(self.avg_len) - 2
        elif rand < 4:
            return round(self.avg_len) - 1
        elif rand < 7:
            return round(self.avg_len)
        elif rand < 9:
            return round(self.avg_len) + 1
        else:
            return round(self.avg_len) + 2



    def generate_name(self):
        length = self.choose_length()
        name = ""
        x0 = self.x0_roll_pool[np.random.randint(0,len(self.x0_roll_pool))]
        name += x0
        if self.series_length == 1:
            for i in range(0,length - 1):
               # print(i)
                self.build_xt_roll_pool(name[-1])
                xt = self.xt_roll_pool[np.random.randint(0,len(self.xt_roll_pool))]
                name += xt[0]
        elif self.series_length == 2:
            for i in range(0,length - 1):
                self.build_xt_roll_pool(name[-2]+name[-1])
                #print (name)
                if self.xt_roll_pool[0][-1] == 0: #if bad xt found, next char determined by using series
                    self.series_length = 1        #length of 1 and examining the last character
                    self.populate_xt_table()
                    self.build_xt_roll_pool(name[-1])
                    self.series_length = 2
                    self.populate_xt_table()
                while 1:
                    rando = np.random.randint(0,len(self.xt_roll_pool))
                    if self.xt_roll_pool[rando][1] > 0:
                      xt = self.xt_roll_pool[rando]
                      break
                name += xt[0]
        return name
