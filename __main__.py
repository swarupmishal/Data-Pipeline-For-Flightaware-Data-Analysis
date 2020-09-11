# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:18:56 2020

@author: misha
"""
from app.automated_flightaware_analysis import AutomatedFlightawareAnalysis
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# For debugging the app in an IDE like Pycharm, one can override system call with a user defined call.
# First argument is the name of the main file to call the app
# second argument is the path of the configuration file. Refer to the user defined call below,
# sys.argv = ['__main__.py', 'D:\\Career-Growth\\Assessments\\magniX\\exploratory_flightaware_data_analysis\\conf\\config.json']

if __name__ == '__main__':
    AutomatedFlightawareAnalysis.run(sys.argv)
