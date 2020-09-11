# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:18:56 2020

@author: misha
"""
import glob
import pandas as pd
import os
from matplotlib import pyplot as plt


class PlotGraphs:

    @staticmethod
    def plot_average_time_for_each_aircraft(**kwargs):
        data_dir = kwargs['data_dir']
        ac = {}

        for file in glob.glob(data_dir + '*'):
            if 'cleaned' in file:
                aircraft_code = os.path.splitext(os.path.basename(file))[0].split('_')[0]
                df = pd.read_csv(file)
                df = df[df['Estimated Time Enroute in Minutes'].notnull()]
                avg = df['Estimated Time Enroute in Minutes'].mean()
                ac[aircraft_code] = avg

        df = pd.DataFrame(list(ac.items()), columns=['Aircraft Code', 'Average Time Flown in Minutes'])
        df.plot(x='Aircraft Code', y='Average Time Flown in Minutes', rot=0, kind='bar', sort_columns=False,
                title='Average Time Flown for Different Aircrafts', ylabel='Average Time in Minutes', legend=True)
        plt.savefig(data_dir + 'Average Time Flown by Aircraft.png')

    @staticmethod
    def plot_most_common_origin(**kwargs):
        data_dir = kwargs['data_dir']
        ac = {}

        for file in glob.glob(data_dir + '*'):
            if 'cleaned' in file:
                aircraft_code = os.path.splitext(os.path.basename(file))[0].split('_')[0]
                df = pd.read_csv(file)
                df = pd.DataFrame({'Number of Departures': df.groupby(['Origin']).size()}).reset_index()
                df = df.sort_values('Number of Departures', ascending=False).head(10)
                ac[aircraft_code] = df

        for aircraft_code, df in ac.items():
            ax = df.plot(x='Origin', y='Number of Departures', rot=0, kind='barh', sort_columns=False,
                         title='Top 10 Airports where the Aircraft ' + aircraft_code + ' Departed From',
                         ylabel='Total Number of Departures', figsize=(20, 15), fontsize=15)
            ax.invert_yaxis()
            plt.savefig(data_dir + 'Most Common Origin for ' + aircraft_code + '.png')
