Crude Oil Price Scraper
Overview
This script is designed to scrape and save crude oil price data from the website OilPrice.com. It fetches the historical prices for various crude oil types by sending POST requests and saves the data into CSV files.

Functionality
Web Scraping:

The script uses the requests library to fetch the webpage and BeautifulSoup to parse the HTML content. It identifies and extracts the different crude oil types available on the website using the select element with the ID view_chart.
Data Extraction:

The extracted crude oil types and their corresponding IDs are stored in lists (crude and IDs). These IDs are used to send POST requests to the action URL 'https://oilprice.com/freewidgets/json_get_oilprices', along with a CSRF token.
Session Handling:

A session is created using requests.Session(), and headers are set to mimic a legitimate browser request. This is important to prevent the request from being blocked or flagged as suspicious by the server.
Data Processing:

The script iterates over each crude oil type, sending a POST request with the appropriate blend_id and a fixed period of 7 days. The server responds with a JSON containing the price data.
The timestamp in the price data is converted from UNIX format to a human-readable date format (YYYY-MM-DD).
The data is then converted into a pandas DataFrame, with the price column converted to numeric format, handling any errors in the process.
File Saving:

The script saves the data into CSV files. The file names are sanitized to remove any illegal characters, ensuring compatibility across different operating systems.
Error Handling:

The script includes checks to ensure the presence of the 'prices' key in the response and handles cases where data retrieval fails by printing appropriate messages.
How to Run
Ensure you have the necessary Python libraries installed:

bash
Copy code
pip install requests beautifulsoup4 pandas
Run the script:

bash
Copy code
python crude_oil_price_scraper.py
The script will create CSV files for each crude oil type in the working directory, named in the format Yearly_Crude_Price_<CrudeName>.csv.

Customization
CSRF Token: The CSRF token in the script (csrf_token) is hardcoded. If this token expires, you will need to update it with a fresh token retrieved from the website's network activity.
Period: The script fetches data for the last 7 days by default. This can be modified by changing the 'period': '7' in the POST data.
Disclaimer
This script is intended for educational purposes only. Ensure compliance with the website's terms of service when scraping data.

