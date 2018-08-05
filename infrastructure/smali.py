# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:50:17 2018

@author: 燃烧杯
"""

import codecs
from .map import bytecode_map as bmap

class Smali:
    
    def __init__(self, path):
        self.path = path
        with codecs.open(path, 'r', 'utf-8') as f:
            self.lines = f.readlines()
        self.linenum = len(self.lines)
            
    def __to_next_method(self, begin):
        while begin < self.linenum:
            if self.lines[begin].startswith(".method"):
                return begin
            begin += 1
        return -1;
                
    def __analyze_line(self, line):
        words = line.split()
        if words:
            cmd = words[0]
            ctype = bmap.get(cmd, 0)
            if ctype != 0:
                self.featurelist.append(ctype)
    
    def getFeature(self):
        self.featurelist = []
        cursor = 0
        while True:
            cursor = self.__to_next_method(cursor)
            if cursor == -1:
                return "".join(self.featurelist)
            while True:
                cursor += 1;
                line = self.lines[cursor].strip()
                
                #一个方法的特征提取结束
                if line.startswith(".end"):
                    self.featurelist.append("|")
                    break
                
                self.__analyze_line(line)
                
                
                
                
                        
            
    
        