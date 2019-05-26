
class 家事:
    def __init__(self):
        self._mode = 'todo'
        self._affair = '家事'
    
    def isAffair(self, key):
        return self._affair == key

    @property
    def name(self):
        return self._affair

    def todo(self):
        self._mode = 'todo'
    
    def redo(self):
        self._mode = 'redo'
    
    def done(self):
        self._mode = 'done'
    
    def response(self):
        if self._mode == 'todo':
            return '未定義這件家事'
        elif self._mode == 'redo':
            return '再說一次，未定義這件家事'
        elif self._mode == 'done':
            return '這件家事不需要做'
        else:
            return '不想回應'

class 掃地(家事):
    def __init__(self):
        super().__init__()
        self._affair = '掃地'

    def response(self):
        if self._mode == 'todo':
            return '記得角落也要掃'
        elif self._mode == 'redo':
            return '你還沒掃嗎?'
        elif self._mode == 'done':
            return '掃地完記得拖地'
        else:
            return '不想回應'

class 拖地(家事):
    def __init__(self):
        super().__init__()
        self._affair = '拖地'

    def response(self):
        if self._mode == 'todo':
            return '拖把水記得擰乾'
        elif self._mode == 'redo':
            return '請記得要先掃地'
        elif self._mode == 'done':
            return '辛苦了'
        else:
            return '不想回應'

class 煮飯(家事):
    def __init__(self):
        super().__init__()
        self._affair = '煮飯'

    def response(self):
        if self._mode == 'todo':
            return '有買菜了嗎?'
        elif self._mode == 'redo':
            return '煮太多家人吃不完'
        elif self._mode == 'done':
            return '好香喔~~~'
        else:
            return '不想回應'
