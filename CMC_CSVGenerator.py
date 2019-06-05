import requests
import csv
import os
import sys
import json
from datetime import datetime
from optparse import OptionParser
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

def main(args=None):
    parser = getParser()
    opts, args = parser.parse_args(args)
    error, api_key, params, file_name = validateArgs(opts)
    if error != "":
        return error
    data = getAPIData(api_key, params)
    generateCSV(data, file_name)
    
    return 0


def getParser():
    parser = OptionParser("%prog: args")
    parser.add_option("-c", "--convert", help="String of comma separated conversion currencies")
    parser.add_option("-l", "--limit", help="Number of Datapoints to return", type="int")
    parser.add_option("-s", "--start", help="Start returning results from this number", type="int")
    parser.add_option("-o", "--output-file", help="the filename for the generated CSV file")
    parser.add_option("-k", "--api-key", dest="api_key", help="Your CMC API Key that will be used to make the request")
    parser.set_defaults(api_key=False,error=None,help_needed=False)
    
    return parser


def generateCSV(data, file_name):
    if file_name == None:
        file_name = "CMC_MarketDataExport_%s.csv" % datetime.now().strftime("%Y%m%d-%H%M%S")
    quotes = []
    csv_data = []
    count = 0; 
    for c in data:
        row = []
        row.append(c["name"])
        row.append(c["symbol"])
        
        for q in c["quote"]:
            if count == 0:
                quotes.append(q)
            q = c["quote"][q]
            row.append(q["market_cap"])
            row.append(q["price"])
            row.append(q["volume_24h"])
            row.append(q["percent_change_1h"])
            row.append(q["percent_change_24h"])
            row.append(q["percent_change_7d"])

        row.append(c["total_supply"])
        row.append(c["circulating_supply"])
        row.append(c["last_updated"])
        csv_data.append(row)
        count += 1; 
    
    headers = generateCSVHeaders(quotes)
    f = csv.writer(open(file_name, "wb+"))
    f.writerow(headers)
    f.writerows(csv_data)


def generateCSVHeaders(quotes):
    full_headers = []
    data_headers = [
        "Currency Name", 
        "Currency Symbol", 
        "QUOTE_HEADERS",
        "Total Supply", 
        "Circulating Supply", 
        "Last Updated"
    ]
    quote_headers = [
        "Market Cap (%s)", 
        "Price (%s)", 
        "24 Hour Volume (%s)", 
        "Percent Change 1 Hour (%s)", 
        "Percent Change 24 Hours (%s)", 
        "Percent Change 7 Day (%s)"
    ]
    
    for h in data_headers:
        if h != "QUOTE_HEADERS":
            full_headers.append(h)
        else:
            for q in quotes:
                for qh in quote_headers:
                    full_headers.append(qh % q)
    
    return full_headers


def validateArgs(opts):
    error = ""
    params = {}
    api_key = ""
    file_name = None
    convert = None
    
    if opts.start is not None:
        if (opts.start > 5000 or opts.start <= 0):
            error += "Start must be between 1 and 5000 \n"
        else:
            params["start"] = opts.start
    if opts.limit is not None:
        if (opts.limit > 5000 or opts.limit <= 0):
            error += "Limit must be between 1 and 5000 \n"
        else:
            params["limit"] = opts.limit 
    if opts.output_file is not None:
        file_name = opts.output_file
    if opts.convert is not None:
        params["convert"] = opts.convert
    if (opts.api_key == False):
        error += "API Key Required to retrieve data, Please use the --api-key option"
    else:
        api_key = opts.api_key   
    
    return error, api_key, params, file_name


def getAPIData(api_key, params):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': api_key,
    }
    resp_data = None
    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=params)
      data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      sys.exit(e)
      
    if response.status_code == 200:
        resp_data = data.get("data", None)
    if not resp_data:
        resp_error =  "No Data recieved from the API"
        resp_error += "HTTP Status Code: %s \n" % str(response.status_code)
        resp_error += "Credits Used: %s \n" % str(data["status"].get("credit_count", "Unknown"))
        resp_error += "Error Message (if avaiable): %s" % (data["status"].get("error_message", "Unknown"))
        sys.exit(resp_error)

    return resp_data
    
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
