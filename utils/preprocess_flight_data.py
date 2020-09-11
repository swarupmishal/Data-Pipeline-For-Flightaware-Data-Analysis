# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:32:40 2020

@author: misha
"""
import pandas as pd
import glob
import os
import numpy as np


class PreprocessFlightData:

    @staticmethod
    def clean_files(**kwargs):
        """This function is used for pre-processing the raw data."""
        data_dir = kwargs['data_dir']

        # remove any old pre-processed file before creating new ones
        PreprocessFlightData.remove_unwanted_files(data_dir=data_dir)

        for file in glob.glob(data_dir + '*'):
            filename_without_ext = os.path.splitext(file)[0]
            df = pd.read_csv(file)

            # create a new column to store if the Flight Plan information is available for the current flight
            # based on if the destination is provided
            df.loc[df['Destination'].notnull(), 'Flight Plan'] = 'Available'
            df.loc[df['Destination'].isnull(), 'Flight Plan'] = 'Not Available'

            # remove Latin characters generated in a faulty way
            df.Departure.replace({r'[^\x00-\x7F]+': ' '}, regex=True, inplace=True)
            df['Estimated Arrival Time'].replace({r'[^\x00-\x7F]+': ' '}, regex=True, inplace=True)

            # calculating the time in minutes for the Estimated Time Enroute column and storing it in a new column
            orig_col = df['Estimated Time Enroute']
            df.loc[df['Estimated Time Enroute'].isnull(), 'Estimated Time Enroute'] = 'NULL'
            for index, row in df.iterrows():
                hh_mm = row['Estimated Time Enroute']
                min = PreprocessFlightData.convert_to_minutes(hh_mm=hh_mm)
                df.at[index, 'Estimated Time Enroute in Minutes'] = min
            df['Estimated Time Enroute'] = orig_col

            # dropping any duplicates rows created due to dynamic nature (live) of the flightaware website
            df = df.drop_duplicates()

            # generating cleaned data
            df.to_csv(filename_without_ext + '_cleaned.csv', index=False, encoding='utf-8')

    @staticmethod
    def remove_unwanted_files(**kwargs):
        data_dir = kwargs['data_dir']

        for file in glob.glob(data_dir + '*'):
            if 'cleaned' in file:
                os.remove(file)

    @staticmethod
    def clean_directory(**kwargs):
        """Removing any pre-existing files from the directory"""
        data_dir = kwargs['data_dir']

        for file in glob.glob(data_dir + '*'):
            os.remove(file)

    @staticmethod
    def convert_to_minutes(**kwarg):
        hh_mm = kwarg['hh_mm']
        if hh_mm != 'NULL':
            hours, minutes = map(int, hh_mm.split(':'))
            min = int(hours) * 60 + int(minutes)
        else:
            min = np.NAN
        return min
