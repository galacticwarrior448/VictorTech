import requests

def get_ticker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()
    try:
        company_code = data['quotes'][0]['symbol']
    except:
        return None
    return company_code

def get_line_graph(company_name):
    API_KEY = "NK2X9KDCRS2PG6PV"

    url = 'https://www.alphavantage.co/query'

    symbol = get_ticker(company_name)
    if symbol == None: return [None, None]

    # Define parameters for the API call
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'compact',  # Can be '1min', '5min', '15min', etc.
        'apikey': API_KEY
    }

    # Make a request to the API
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the most recent stock price
    try:
        time_series = data['Time Series (Daily)']

        # Extract the dates and prices
        prices = []
        dates = []
        counter = 0
        for date, price_data in time_series.items():
            prices.append(price_data['1. open'])
            dates.append(date)

        # Return the list of historical prices
        return [dates, prices]

    except KeyError:
        return "Error: Unable to fetch data. Check the symbol or API usage."

def find_stores(store_name, country):
    import requests

    api_key = '3221277a2b724ff58314bb5f9395616a'
    store_name1 = store_name.replace(' ','+')
    url = f'https://api.geoapify.com/v1/geocode/search?text={store_name1},+India&apiKey={api_key}'

    response = requests.get(url)
    data = response.json()
    lat = data['features'][0]['properties']['lat']
    lng = data['features'][0]['properties']['lon']
    label = data['features'][0]['properties']['county']
    a = [{"lat":lat, "lng":lng, "label":label}]
    return a

def age_gender_traffic_distribution(company_name):
    api_key = '60b33ee52d477bcb5be736102d0ac56eacf364a2107ff746edafc6850393b82f'
    # Prepare the SerpAPI URL for Google search query
    url = "https://serpapi.com/search.json"

    url1 = "https://similar-web-data.p.rapidapi.com/"

    headers = {
        "x-rapidapi-key": "2212859f8bmsh08340b3125ee6e6p12abe2jsn24537f55d9ea",
        "x-rapidapi-host": "similar-web-data.p.rapidapi.com"
    }

    # Set the parameters for the API call
    params = {
        "q": company_name,
        "api_key": api_key,
        "engine": "google",
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()

        # Parse through the results and find the first website link
        if 'organic_results' in data and len(data['organic_results']) > 0:
            for result in data['organic_results']:
                if 'link' in result:
                    querystring = {"domain": result['link'].lstrip("htps:/").split("/")[0]}
                    response = requests.get(url1, headers=headers, params=querystring)
                    text = response.json()

                    demo = text["demographics"]
                    output = {}
                    output["age"] = [[], []]
                    for i in range(len(demo["ageDistribution"])):
                        output["age"][0].append(str(demo["ageDistribution"][i]["minAge"]) + " - " + str(demo["ageDistribution"][i]["maxAge"]))
                        output["age"][1].append(demo["ageDistribution"][i]["value"])
                    output["gender"] = [[], []]
                    for i in demo["genderDistribution"]:
                        output["gender"][0].append(i)
                        output["gender"][1].append(demo["genderDistribution"][i])

                    traffic = text["trafficSources"]
                    output["trafficSources"] = [[], []]

                    for i in range(7):
                        output["trafficSources"][0].append(list(traffic.keys())[i])
                        output["trafficSources"][1].append(list(traffic.values())[i])

                    return output
        return "No website found in search results."
    else:
        return None
