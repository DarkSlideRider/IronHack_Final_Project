# IronHack_Final_Project: Stock Recommender

**Goal** of the project is to build a recommender system to empower investors in making better investment decisions.

![image](https://pythonforfinance.net/wp-content/uploads/2021/07/iz9RqFthsh-1170x656.png)

## Business problem to be solved

**How to save money the smart way?**
Media is full of information about stocks of companies, this is overwhelming. Often times there are too many resources with too much information (prices, fundamental data, analysts opinion) to check.
Stock recommender will help investors looking in the right corners in the investment universe giving a selection of high potential companies to focus analysis on.

## MVP

1. Database via (bonus: web scraping)/ API - Reference database in MySQL with schema via YFinance
2. Prototype user interface (Jupyter-notebook) to enter a company name or ticker symbol or industry to see the high potential companies based on the user input
3. Based on KPIs (Return [EBIT] on capital employed, Return [EBIT] on EV) company will be ranked - sector-industry - size (net sales) - region
4. Stock will be first checked if in a list of companies that are being seen as high quality (can be growth, etc.) companies that are advised by stock analysts. 
5. Stock will be benchmarked against others in the industry/ sector and size. The result will be a list of companies with a ranking based on the price (instead of list tableau dashboard?)

## What are "Nice to haves" after the MVP?

1. Web-Scraping from analyst pages, automated downloading with scheduling running updates of DB
2. Logic to obtain company prices to calculate on the fly the ratios
3. Cluster (K-means, DT, RF) the data to create new clusters outside of industry, consider clusters per sectors e.g. slow growers, fast growers, stalwarts, cyclical, turnarounds, asset plays
4. Selection of a strategy (quality-value, growth) is optional, by default value strategy - the strategy will define the KPI for the ranking
5. Run back test (time series) to check if KPIs lead to significant better results in the past
6. Consider more KPIs for evaluation (P/E, earnings growth, debt/equity, net sales, EBITDA, CF from operations)
7. Data input via web application, data output via dashboard or web application
8. Enlarge number of companies or time of analysis.

## Where do I get my data from?

1. Stock Advisors (motley fool)(https://www.fool.de)
2. Heibel Ticker (https://www.heibel-ticker.de/)
3. Onvista (https://www.onvista.de/)
4. Yahoo (https://de.finance.yahoo.com/)
5. Jitta (www.jitta.com)
6. APIs: Yfinance (start with yfinance), Pandas Datareader, investpy
7. Others: 
Tickers
https://www.factiva.com/CP_Developer/ProductHelp/FDK/FDK33/shared_elements/table_exchange.htm
https://www.gnucash.org/docs/v4/C/gnucash-help/fq-spec-yahoo.html


## Used Modules

Stock  
``pip install -i https://pypi.anaconda.org/ranaroussi/simple yfinance``  
``conda install -c conda-forge lxml``

Get tickers  
``conda install -c minhhg200 yahoo-ticker-downloader``  
``pip install Yahoo-ticker-downloader``  
``conda install -c conda-forge sqlalchemy`` 
``conda install -c conda-forge pymysql`` 

## Obstacles
1. Getting the needed knowledge in time to build an interface and obtain the data
2. The huge amount of options can be a curse (libraries, APIs, web scraping, ready DB?)
3. DQ very different on the sources, currency issues, issues with ticker - one company can have several tickers - one per stock exchange, companies are coming and going
4. Web interface and user interaction - I have no clue as of now :(
5. My curiosity and interest in finance topics can lead me on wrong tracks, spending time on irrelevant topics.

### Links
Trelloboard: https://trello.com/b/i6KaO1lK/stock-recommender
