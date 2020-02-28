from collections import deque
import pandas as pd
import time
from datetime import timedelta, date, datetime
import random as random
import json

def get_time():
    return datetime.fromtimestamp(time.time())

class Buffer():
    """Key = date, value = tuple (successful, missed, total, follow up, coverage)"""
    
    def __init__(self, size=30):        
        self.buffer = deque(maxlen=int(size))       # extends list which can be sampled from 
        self.maxSize = size 
        self.length = 0


    def len(self):
        return self.length 


    def store(self, data):
        if self.length > 0:
            top = self.buffer.pop()
            # print(f"top['date']: {top['date']}, data['date']: {data['date']}")
            if top['date'] == data['date']:    # Replace if same day
                with open("./static/logs.txt", "a") as file:
                    print(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- Updating buffer with today's latest data:\n\t" + json.dumps(top)))
                    file.write(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- Updating buffer with today's latest data...\n\t" + json.dumps(top) + "\n"))

                self.buffer.append(data)
            else:                               # Stack if new day
                self.buffer.append(top)         # TODO this is broken atm
                self.buffer.append(data)
        else: 
            self.buffer.append(data) 

        self.length += 1


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
        df.to_csv("./static/Monthly Report.csv", sep=',')
        
        with open("./static/logs.txt", "a") as file:
            print(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- Saving to the buffer..."))
            file.write(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- Saving to the buffer...\n"))

    def load(self, filename):
        try:
            with open("./static/logs.txt", "a") as file:
                print(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- Loading from the buffer..."))
                file.write(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- Loading from the buffer...\n"))

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
            with open("./static/logs.txt", "a") as file:
                print(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- " + f"{filename} was not found, building a new buffer..."))
                file.write(get_time().strftime("[%Y-%m-%d %H:%M:%S] --- " + f"{filename} was not found, building a new buffer...\n"))
