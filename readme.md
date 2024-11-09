Dynamiq: Price Prediction Model:

This app is designed to help you understand and predict product prices over time. It uses a simple interface to help users explore predicted prices, views, and add-to-cart data for different products over several months and years.


Libraries and Tools:

Streamlit: This is what powers the web interface you interact with. It's simple, fast, and looks great for data visualizations.
Pandas: To manage the data and do calculations.
Plotly: To make interactive charts that you can explore.
Numpy: For some number crunching, like creating synthetic data based on a year’s data.
RapidFuzz: This helps with fuzzy matching, so I can match your input (like a product name or category) to the data we have, even if they     aren't exactly the same.
Requests and BeautifulSoup: These are used for scraping product names from URLs you give me. I’m able to pull out the product details from   a website using these.

NOTE: THE DATA FOR THE PRODUCTS ARE PRODUCED THROUGH SYNTHETIC GENERATION,THUS THE RESULTS MAY VARY WITH IDEAL DATA

How the Analysis Works:

When you enter the information and click the "Analyse" button, here's what happens behind the scenes:
Product Matching: I look for the category and product you entered and use fuzzy matching to find the closest match in our data.
Monthly Data Generation: Based on the data for a given year (views, add-to-cart, and base price), I generate synthetic monthly data. I even add a little boost to certain months to reflect sales seasons (like in November).
Price Adjustment: The price is adjusted depending on views and add-to-cart activity. If there's a surge in interest, the price might go up; if there's less interest, the price could go down. For example, in November, I apply a 60% discount to reflect holiday sales.
Best Time to Buy and Sell: I also analyze the monthly prices to tell you which months are the best to buy and sell a product based on predicted pricing trends.

========================================================================================================================================================================

DISCLAIMER ON COMMERCIAL USE AND WEB SCRAPING:

The data provided by this tool is based on web scraping from publicly available websites. While the tool is intended for personal or educational use, commercial use of scraped data may be subject to legal restrictions.

We encourage users to ensure that they comply with the terms of service of any website they scrape from. Additionally, web scraping can be seen as a violation of some sites' terms and conditions, especially for commercial purposes. Please make sure to seek permission from relevant website owners if you intend to use scraped data for commercial applications.

The creator of this tool is not responsible for any legal issues arising from the use of scraped data for commercial purposes.

========================================================================================================================================================================
