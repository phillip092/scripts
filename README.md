# scripts
Quick and dirty scripts for random purposes. This is not clean code and should not be used in a production environment. 


### CMC_CSVGenerator.py
A Simple Python script to generate a CSV file with results pulled from CoinMarketCap's /cryptocurrency/listings/latest endpoint. Works with python 2.7 or 3

#### Prerequisites

Requires python requests library

```
pip install requests
```

#### Usage

The only required parameter is `api-key`, which should be set to your CMC Pro API key

```
python CMC_CSVGeneration.py --api-key INSERT-YOUR-API-KEY-HERE
```

All accepted parmeters are: 

* api-key - The API key that you would like to use to authenticate with the API __Required__
* start - The result that the API's response should start with [1 - 5000] - Default = 1 
* limit - The number of data points that should be returned [1 - 5000] - Default = 100
* convert - Comma seperated string of FIAT symbols that you would like the results converted to - Default = USD
* output-file - A name for the output CSV that will be generated (if a directory is included, it must already exist) - Default = CMC_MarketDataExport_YYYYMMDD-HHMMSS.csv
