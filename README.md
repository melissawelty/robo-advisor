# Robo Advisor Project

This app issues requests to the [AlphaVantage Stock Market API](https://www.alphavantage.co/) in order to provide stock recommendations based on historical price trends. 

## Prerequisites 
* Anaconda 3.7
* Python 3.7
* Pip


## Installation

Clone or downlaod [this repository](https://github.com/melissawelty/robo-advisor) link onto your computer. Then navigate there from the command line:

```sh
cd robo-advisor
```

Use Anaconda to create and activate a new virtual environment called "stocks-env". 

```
conda create -n stocks-env python =3.7 # (first time only)
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```
pip install -r requirements.txt
```


## Setup

Before using or developing this application, you will need to  [obtain an AlphaVantage API Key](https://www.alphavantage.co/support/#api-key) (e.g. "cba321").

After obtaining an API Key, create a new file in this repository called ".env", and update the contents of the ".env" file to specify your real API Key:

```
ALPHAVANTAGE_API_KEY="cba321"
```

## Usage

Run the recommendation script:
```
python app/robo_advisor.py
```
## Additional Information

A separate window will populate with historical prices illustrated on a graphic. After viewing, close the graph to see up to date stock prices and a recommendation. 




