# exploratory-flightaware-data-analysis

## Introduction
I have developed an automated app called “Exploratory FlightAware Data Analysis” to fetch aircraft data from the [FlightAware website.](https://flightaware.com/live/aircrafttype/) The app fetches requested aircraft data and builds some analysis on top of it.

## Pre-requisites
The app is developed using in Python. Most of the libraries used for developing the tool are from the Standard Python libraries. One needs to make sure the virtual environment used for running the tool has the following external modules installed,
*	BeautifulSoup
*	Selenium
*	Pandas
*	Matplotlib
*	Numpy

The app uses BeautifulSoup module to scrape data from the website. It requires some form of browser driver to connect to the URL. For this project, I have used chromedriver.

## Configuration
The app requires a configuration file where the names of the aircrafts are defined, whom we are investigating. The configuration file is simple ‘.json’ file and its contents are explained below.
*	url: This element defines the target URL from where the app should fetch more information.
*	path_to_driver:  This element defines the path for the browser driver that should be used to connect to the URL.
*	data_dir: This directory is the target directory where you want the app to generate the output files after analysis.
*	aircraft_names: This is a list of aircraft names that you want to do the analysis for.

You can find the screenshot of the sample configuration file used for this project,
![Image of sample config file](https://github.com/swarupmishal/exploratory-flightaware-data-analysis/blob/master/images/sample_config_file.png)
 
## Execution
To execute the app, one can call the ‘__main__.py’ file provided in the base directory of the tool. To call the tool use the Python virtual environment where all the required modules are installed. The tool expects the path to the configuration file as a first argument to the call. Just use the command,

`<path to virtual env>\python.exe __main__.py conf\config.json`

I wanted to containerize the application but, due to lack of time I was not able to do it. A sample screenshot of how I call the app is shown below,
![Image of sample python call](https://github.com/swarupmishal/exploratory-flightaware-data-analysis/blob/master/images/sample_python_call.png)
 
The app scrapes data from the URL passed in the config file and generates some reports into the data directory defined in the config file.

## Scope of Improvement
The app can be improved further by,
*	adding error handling mechanism
*	Adding logging mechanism
*	Also answering more BI questions like calculating average distance that the aircrafts usually fly. For this we will have to fetch the distance between airports since we have the ICAO codes.
