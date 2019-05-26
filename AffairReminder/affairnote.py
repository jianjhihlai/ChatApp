import affairs

class AffairNote:
    def __init__(self):
        self._affairs = []
        self._defaultAffair = affairs.家事()

    def inputaffair(self, note):
        if note.find("完成") > -1:
            note = note.replace("完成", "")
            current = self.completeaffair(note)
        else:
            current = self.addaffair(note)

        return current.response()
    
    def completeaffair(self, key):
        affair_idx = self._getaffair(key)
        if affair_idx > -1:
            affair = self._affairs.pop(affair_idx)
        else:
            affair = self._defaultAffair
        affair.done()
        return affair

    def addaffair(self, key):
        return self._newaffair(key)
    
    def remind(self):
        message = ''
        for i, affair in enumerate(self._affairs):
            message += '({}) {}'.format(i+1, affair.name)
        return message

    def _newaffair(self, key):
        affair_class = getattr(affairs, key, affairs.家事)
        affair = affair_class()
        self._affairs.append(affair)
        return affair

    def _getaffair(self, key):
        index = -1
        for i, affair in enumerate(self._affairs):
            if affair.isAffair(key):
                index = i
                break
        return index
        
