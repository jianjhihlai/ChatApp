import pandas as pd
from os import path

class Account:
    # place = models.CharField(max_length=20)
    # subject = models.CharField(max_length=50)
    # cost = models.DecimalField(max_digits=5, decimal_places=0)
    # created = models.DateTimeField(blank=True)
    # modified = models.DateTimeField(null=True, blank=True)
    columns = ['place', 'subject', 'cost', 'created']
    def __init__(self):
        self.objects = AccountCollection(self.columns)

    # @property
    # def objects(self):
    #     return self.objects



class AccountCollection:
    database = './db.csv'
    def __init__(self, columns):
        self.columns = columns
        self.parse_dates = ['created']
        if path.isfile(self.database):
            self.db = pd.read_csv(self.database, index_col=0, parse_dates=self.parse_dates)
        else:
            self.db = pd.DataFrame(columns = self.columns)
    
    def create(self, place, subject, cost, created):
        data = dict(zip(self.columns, [place, subject, cost, created]))
        row = pd.Series(data)
        self.db = self.db.append(row, ignore_index=True)
        self.__save()
        # print(self.db['created'])
        return self.db.iloc[-1,:]

    def order_by(self, field):
        self.db = self.db.sort_values(by=field)
        return self

    def filter(self, place=None, subject=None, cost=None, created__range=None):
        filter_and = self.db['subject'] != None
        if place != None:
            filter_and = filter_and & (self.db['place'] == place)
        if subject != None:
            filter_and = filter_and & (self.db['subject'] == subject)
        if cost != None:
            filter_and = filter_and & (self.db['cost'] == cost)
        if created__range != None:
            filter_and = filter_and & ((self.db['created'] >= pd.Timestamp(created__range[0])) & (self.db['created'] < pd.Timestamp(created__range[1])))
        self.db = self.db[filter_and]
        return self
        

    def first(self):
        return self.db.iloc[0]

    def sum(self, field):
        return {'total': self.db[field].sum()}

    def __save(self):
        self.db.to_csv(self.database, sep=',', encoding='utf-8')
    
        
