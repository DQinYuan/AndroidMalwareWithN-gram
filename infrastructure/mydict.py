# -*- coding: utf-8 -*-

class MyDict:
    
    def __init__(self):
        self.dict = {}
        self.current_len = -1
        
    def newLayer(self):
        self.current_len += 1
        self.meet_list = []
        for key in self.dict.keys():
            self.dict[key].append(0)
            
    def mark(self, word):
        if self.dict.get(word):
            if word not in self.meet_list:
                self.dict.get(word)[-1] = 1
                self.meet_list.append(word)
        else:
            self.dict[word] = ([0] * self.current_len)
            self.dict[word].append(1)
            self.meet_list.append(word)
            
