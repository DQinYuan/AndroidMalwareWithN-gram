# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:20:32 2018

@author: 燃烧杯
"""
import os
import re
from .smali import Smali

class Ware:
    
    __smali_pat =  re.compile(r"\.smali$")
    
    def __init__(self, path, isMalware):
        self.name = os.path.split(path)[-1]
        smaliPath = os.path.join(path, "smali")
        self.smalis = []
        self.isMalware = isMalware
        for root, dirs, files in os.walk(smaliPath):
            for file in files:
                if Ware.__smali_pat.findall(file):
                    self.smalis.append(Smali(
                            os.path.join(root, file)
                            ))
                    
    def extractFeature(self, datafile):
        feature = ''
        for smali in self.smalis:
            feature += smali.getFeature()
        datafile.append(self.name, feature, self.isMalware)
        
                    
            
            