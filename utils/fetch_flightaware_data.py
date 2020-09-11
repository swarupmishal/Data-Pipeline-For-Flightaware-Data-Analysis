# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:37:26 2020

@author: misha
"""
import re
import pandas as pd
from utils.web_scraping import WebScraper


class FetchFlightAwareData:

    @staticmethod
    def fetch_aircraft_data(**kwargs):
        """Fetch the data based on the type of lookup value passed. This function is currently designed to process
        and extract the code or the link to fetch more information on each aircraft. It can be further improved
        to fetch more values"""
        soup = kwargs['soup']
        aircraft_type = kwargs['aircraft_type']
        lookup = kwargs['lookup']
        data_found_flag = 0

        tables = soup.findChildren('table')

        # get the first table on the page
        aircraft_table = tables[0]
        table_rows = aircraft_table.findChildren(['tr'])
        for row in table_rows:
            if data_found_flag == 1:
                break
            table_cells = row.findChildren('td')
            for cell in table_cells:
                if aircraft_type in cell:
                    if lookup == 'code':
                        lookup_value = table_cells[1].get_text()
                        data_found_flag = 1
                        break
                    elif lookup == 'link':
                        lookup_value = table_cells[1].a['href']
                        lookup_value = 'https://flightaware.com' + lookup_value
                        data_found_flag = 1
                        break
        return lookup_value

    @staticmethod
    def fetch_and_generate_aircraft_flight_details(**kwargs):
        """This function can be used to fetch more information for individual aircrafts. It also generates the
        raw data in the data directory."""
        data_dir = kwargs['data_dir']
        driver = kwargs['driver']
        aircraft_info = kwargs['aircraft_info']

        for aircraft_type, link in aircraft_info.items():
            ident = []
            type = []
            origin = []
            destination = []
            departure_time = []
            arrival_time = []
            estimated_time_enroute = []

            first_execution_flag = 0
            soup = WebScraper.get_page_content_soup(driver=driver, url=link)

            # check if there is a link to the next page on the current table, if available fetch data on the next
            # page too
            a = soup.find('a', href=True, text=re.compile("Next"))
            while a or first_execution_flag == 0:
                soup = WebScraper.get_page_content_soup(driver=driver, url=link)
                aircraft_flight_details_table = soup.find("table",{"class":"prettyTable fullWidth"})
                if aircraft_flight_details_table is None:
                    continue
                table_rows = aircraft_flight_details_table.findChildren(['tr'])
                for row in table_rows:
                    if row.find('th'):
                        continue
                    table_cells = row.findChildren('td')
                    ident.append(table_cells[0].get_text())
                    type.append(table_cells[1].get_text())
                    origin.append(table_cells[2].get_text())
                    destination.append(table_cells[3].get_text())
                    departure_time.append(table_cells[4].get_text())
                    arrival_time.append(table_cells[5].get_text())
                    estimated_time_enroute.append(table_cells[6].get_text())
                first_execution_flag = 1

                # check if there is a link to the next page on the current table, if available fetch data on the next
                # page too
                a = soup.find('a', href=True, text=re.compile("Next"))
                if a:
                    link = a["href"]

            # write the fetched data into the csv
            df = pd.DataFrame({'Ident': ident, 'Type': type, 'Origin': origin, 'Destination': destination,
                               'Departure': departure_time, 'Estimated Arrival Time': arrival_time,
                               'Estimated Time Enroute': estimated_time_enroute})
            df.to_csv(data_dir + aircraft_type + '.csv', index=False, encoding='utf-8')
