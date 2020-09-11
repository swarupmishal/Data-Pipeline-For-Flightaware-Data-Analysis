# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:32:40 2020

@author: misha
"""
import json
import sys
from utils.web_scraping import WebScraper
from utils.fetch_flightaware_data import FetchFlightAwareData
from utils.preprocess_flight_data import PreprocessFlightData
from utils.plot_graphs import PlotGraphs


class AutomatedFlightawareAnalysis:

    @staticmethod
    def run(args):
        config_file_path = args[1]
        
        with open(config_file_path) as file:
            config_file = json.load(file)
            
        url = config_file['url']
        path_to_driver = config_file['path_to_driver']
        aircraft_names = config_file['aircraft_names']
        data_dir = config_file['data_dir']

        aircraft_info = {}

        driver = WebScraper.get_chrome_driver(path_to_driver=path_to_driver)

        # reading the contents of the main URL
        soup = WebScraper.get_page_content_soup(driver=driver, url=url)
        for aircraft_type in aircraft_names:
            link = FetchFlightAwareData.fetch_aircraft_data(soup=soup, aircraft_type=aircraft_type, lookup='link')
            code = FetchFlightAwareData.fetch_aircraft_data(soup=soup, aircraft_type=aircraft_type, lookup='code')
            aircraft_info[code] = link

        # removing files from the data directory if they exist
        PreprocessFlightData.clean_directory(data_dir=data_dir)

        # scrape each link for given aircrafts and generate raw data
        FetchFlightAwareData.fetch_and_generate_aircraft_flight_details(data_dir=data_dir, driver=driver,
                                                                        aircraft_info=aircraft_info)

        # clean the raw data
        PreprocessFlightData.clean_files(data_dir=data_dir)

        # perform analysis on the data to find insights
        PlotGraphs.plot_average_time_for_each_aircraft(data_dir=data_dir)
        PlotGraphs.plot_most_common_origin(data_dir=data_dir)

        print('Process terminated successfully!')


if __name__ == '__main__':
    AutomatedFlightawareAnalysis.run(sys.argv)
