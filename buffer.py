from collections import deque
import pandas as pd
import time
import random as random

class Buffer():
    """Key = date, value = tuple (successful, missed, total, follow up, coverage)"""
    
    def __init__(self, size=30):        
        self.buffer = deque(maxlen=int(size))       # extends list which can be sampled from 
        self.maxSize = size 
        self.len = 0


    def len(self):
        return self.len 


    def store(self, data):
        if self.len > 0:
            top = self.buffer.pop()
            if top['date'] == data['date']:    # Replace if same day
                self.buffer.append(data)
            else:                               # Stack if new day
                self.buffer.append(top)         # TODO this is broken atm
                self.buffer.append(data)
        else: 
            self.buffer.append(data) 

        self.len += 1


    def save(self):
        dates = []
        t = []
        m = []
        s = [] 
        f = [] 
        c = []
        for entry in self.buffer:
            dates.append(entry['date'])
            t.append(entry['total'])
            m.append(entry['missed'])
            s.append(entry['successful'])
            f.append(entry['follow_up'])
            c.append(entry['coverage'])

        # initialise data of lists. 
        data = {'Total': t, 'Successful': s, 'Missed': m, 'Follow Ups': f, '% Coverage': c} 
    
        # Creates pandas DataFrame. 
        df = pd.DataFrame(data, index=dates) 
        df.to_csv("Monthly Report.csv", sep=',')
        print("Logging to the buffer...")



    def load(self, filename):
        try:
            print("Loading to the buffer...")
            d = pd.read_csv(str(filename))
            for index, row in d.iterrows():
                entry = { "date": "", "total": 0, "successful": 0, "missed": 0, "follow_up": 0, "coverage": -1 }
                entry['date'] = row[0] 
                entry['total'] = row[1] 
                entry['successful'] = row[2] 
                entry['missed'] = row[3] 
                entry['follow_up'] = row[4]
                entry['coverage'] = row[4]
                self.buffer.append(entry)
        except FileNotFoundError:
            print(f"{filename} was not found, building a new buffer...")