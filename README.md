# scrapy-scraping-centris.ca-website-using-scrapy-splash
This Project is build in Python Scrapy, where for rendering JS, I used splash as headless browser.

About:
The Project is built in python scrapy, where we sending requests into centris.ca API two end points with request payload, which is generating when you giving query in website search box and on clicking next button for next page. We also going to each listing summary page and extract description from listing main page, through local splash instance.


Some features:
Scraping Api ends points 
Providing Requests payload
Using Splash for rendering Java script
Best Approach to scrape  data



Tools and packages used in this project:
Python
Scrapy framework
Docker Toolbox
scrapinghub/splash Image
Lua source



Setup:
1. Donwload python from official website: https://www.python.org/downloads/
2. Scrapy requires Python 3.6+
3. Make sure pip package-management system is installed
4. Install Docker from official website : https://www.docker.com/
5. Run Docker and OPEN CMD and download splash image by command:
    docker pull scrapinghub/splash (In windows)
    for more refer to https://splash.readthedocs.io/en/1.6/install.html
6. Run scrapinghub/splash Image 

Add following code to settings.py:

```
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

SPLASH_URL = '<Your_Splash_local_host_Url>' #Mine: http://localhost:8050/'

```

Prerequisites:
Open CMD and change working directory into project directory and then give command:
pip install -r requirements.txt
this will install all required dependencies and packges.

Run:
Run for default Excel Urls file :
scrapy crawl file -o data.csv (-o filename.csv will generate data csv file )

Cancel Run Process:
CTRL+C to cancel.

License:
Feel free to use it for your yourself and contribute in project.

Bonus Note:
The splash lua source in Back_code.py is optamized to abort downloading for unnecessary js css and images, and plugins to process the request
faster and avoid 503 Errors. 

All Right.