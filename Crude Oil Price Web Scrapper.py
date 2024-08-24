import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

# Fetch the webpage
url = 'https://oilprice.com/oil-price-charts/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract options
select_element = soup.find('select', id='view_chart')
options = select_element.find_all('option')
values = {option.text: option['value'] for option in options}

crude = []
IDs = []
for text, value in values.items():
    crude.append(text)
    IDs.append(value)

# Define action URL and CSRF token
action_url = 'https://oilprice.com/freewidgets/json_get_oilprices'
csrf_token = '859c6d9def9b05552958847d7c3d2135'

# Create a session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://oilprice.com',
    'X-Requested-With': 'XMLHttpRequest'
})

# Iterate over each ID and fetch prices
for i in range(len(IDs)):
    post_data = {
        'blend_id': IDs[i],
        'period': '7',
        'op_csrf_token': csrf_token
    }

    response = session.post(action_url, data=post_data)

    # Check if response is successful
    if response.status_code == 200:
        parsed_data = json.loads(response.text)

        # Check if 'prices' key exists
        if 'prices' in parsed_data:
            prices = parsed_data['prices']

            # Process each price entry
            for price_entry in prices:
                timestamp = price_entry['time']
                price_entry['time'] = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

            # Create DataFrame and save to CSV and Excel
            df = pd.DataFrame(prices)
            df['time'] = pd.to_datetime(df['time'])
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            sanitized_crude = sanitize_filename(crude[i])
            df.to_csv(f"Yearly_Crude_Price_{sanitized_crude}.csv", index=False)
        else:
            print(f"No 'prices' key in response for ID: {IDs[i]}")
    else:
        print(f"Failed to fetch data for ID: {IDs[i]}. Status code: {response.status_code}")


