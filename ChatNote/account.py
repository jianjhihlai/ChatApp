from models import Account
import datetime
import aiml
import glob
import os
import re
import json

class CostDefault:

    def __init__(self, text):
        self.text = text
        self.target = self.process()

    def process(self):
        return self.text

    def response(self):
        return self.text

class CostNote(CostDefault):

    def __init__(self, text):
        super().__init__(text)

    def process(self):
        try:
            pre = Account().objects.order_by('-created').filter(subject=self.text[1]).first()
        except:
            self.pre = None
        else:
            self.pre = pre

        ac = Account().objects.create(place=self.text[0], subject=self.text[1], cost=self.text[2], created=datetime.datetime.now())
        return ac

    def response(self):
        if self.pre is None:
            return '您在{0}買{1}花了{2}元'.format(self.target.place,self.target.subject, self.target.cost)
        else:
            return '您上次在{0}買{1}花了{2}元，這次花了{3}元'.format(self.pre.place,self.pre.subject, self.pre.cost, self.target.cost)

class TimeCost(CostDefault):

    def __init__(self, text):
        self.months = {
            '一月': 1, '二月': 2, '三月': 3, '四月': 4, '五月': 5, '六月': 6,
            '七月': 7, '八月': 8, '九月': 9, '十月': 10, '十一月': 11, '十二月': 12
        }
        super().__init__(text)

    def process(self):
        # try:
            period = self.timePeriod(self.text)
            ac = Account().objects.filter(created__range=period).sum(field='cost')
        # except:
        #     return None
        # else:
            return ac

    def response(self):
        if self.target is None:
            return '您在{0}並沒有消費'.format(self.text)
        else:
            return '您在{0}總計花了{1}元'.format(self.text, self.target['total'])

    def timePeriod(self, time_text):
        if time_text == '這個月':
            month = self.getThisMonth()
        elif time_text == '上個月':
            month = self.getLastMonth()
        else:
            month = self.months[time_text]
        return self.getDateRange(month)


    def getThisMonth(self):
        today = datetime.datetime.today()
        return today.month

    def getLastMonth(self):
        today = datetime.datetime.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        return lastMonth.month

    def getDateRange(self, month):
        today = datetime.datetime.today()
        firstM = datetime.date(today.year, month, 1)
        nextM = datetime.date(today.year, month+1, 1)
        return [firstM, nextM]

class ItemCost(CostDefault):

    def __init__(self, text):
        super().__init__(text)

    def process(self):
        try:
            ac = Account().objects.order_by('created').filter(subject=self.text).first()
        except:
            return None
        else:
            return ac

    def response(self):
        if self.target is None:
            return '您並沒有買過{0}'.format(self.text)
        else:
            return '您上次在{2}買{0}花了{1}元'.format(self.text, self.target.cost, self.target.place)

class ItemWhere(CostDefault):

    def __init__(self, text):
        super().__init__(text)

    def process(self):
        try:
            ac = Account().objects.order_by('created').filter(subject=self.text).first()
        except Exception as e:
            return None
        else:
            return ac

    def response(self):
        if self.target is None:
            return '您並沒有買過{0}'.format(self.text)
        else:
            return '您可以去{2}買{0}，上次花了{1}元'.format(self.text, self.target.cost, self.target.place)

class AimlNote(CostDefault):
    def __init__(self, text, userid):
        self.userid = userid
        super().__init__(text)

    def process(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        mybot_path = 'aimldata'
        #切換到語料庫所在工作目錄
        os.chdir(os.path.join(current_path, mybot_path))
        mybot = aiml.Kernel()
        learning = self.learn(self.text)
        if learning or ~os.path.isfile("mybot_brain.brn"):
            files = glob.glob('*.aiml')
            for learn_file in files:
                mybot.learn(learn_file)
            mybot.saveBrain("mybot_brain.brn")
        else:
            mybot.bootstrap(brainFile="mybot_brain.brn") 
        if learning:
            return None
        else:
            self.loadSession(mybot)
            return mybot
    
    def response(self):
        if self.target is None:
            return '已學習您給的知識'
        else:
            message = self.target.respond(self.text, self.userid)
            self.saveSession(self.target)
            return message

    def loadSession(self, mybot):
        sessionFile = self.userid+'.json'
        if os.path.isfile(sessionFile):
            session = dict()
            with open(sessionFile, 'r') as f:
                json_str = f.read()
                session = json.loads(json_str)
            # print(session)
            for key, value in session.items():
                mybot.setPredicate(key, value, self.userid)
        return mybot

    def saveSession(self, mybot):
        sessionData = mybot.getSessionData(self.userid)
        session = dict()
        for key, value in sessionData.items():
            if key == '_inputHistory' or key == '_outputHistory' or key == '_inputStack':
                continue
            session[key] = value
        if any(session):
            with open(self.userid+'.json', 'w') as f:
                f.write(json.dumps(session))
        # print(json.dumps(session))


    def learn(self, text):
        pattern = '^<aiml.+<\/aiml>$'
        findaiml = re.search(pattern, text, flags=re.S | re.M | re.I)
        if findaiml is not None:
            found = findaiml.group()
            with open(self.userid + datetime.now().strftime('%Y%m%d%H%M%S') + '.aiml', 'w') as f:
                f.write(found)
            return True
        else:
            return False



