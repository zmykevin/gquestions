## People Also Ask Scraper
The code is forked from Alessio Nittoli's github repo to scrape the people also ask box from google search. For details of the scraper, please refer to his [blogs post](https://nitto.li/scraping-people-also-asked/).

### Changes we made
We modify the original scraper, which scraped the questions from the box. We extend the scraper to also extract the url of the website that provides a potential answer to it. The output is also saved in a easy-to-read json file. 

### Install Dependencies
Please have **python 3.6+** installed and run the following command  

```
pip install -r requirements.txt
```

### How to Run the Code
You can create a list of the queries/entities you want to search for the "people also ask" questions in the **search_queries.txt**, in the following format:

```
sushi
sashimi
advengers
automatic mobile
...
```

