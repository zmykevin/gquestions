## People Also Ask Scraper
The code is forked from Alessio Nittoli's github repo to scrape the people also ask box from google search. For details of the scraper, please refer to his [blogs post](https://nitto.li/scraping-people-also-asked/). The original github repo is [here](https://github.com/nittolese/gquestions)

### Changes we made
We modify the original scraper, which scraped the questions from the box. We extend the scraper to also extract the url of the website that provides a potential answer to it. The output is also saved in a easy-to-read json file. 

### Install Dependencies
Please have **python 3.6+** installed and run the following command  

```
pip install -r requirements.txt
```
In order to run the code, you will also need to have a chrome browser and corresponding webdriver. Check the version of your chrome browser and download the corresponding driver from [this page](https://chromedriver.chromium.org/downloads). Unzip the downloded zip file to **driver/** under this repository. 
(If your chrome browser version is 78 and you run the code on ubuntu system, you don't have to do this step as the right webdriver is already in the folder.)

### How to Run the Code
You can create a list of the queries/entities you want to search for the "people also ask" questions in the **search_queries.txt**, in the following format:

```
sushi
sashimi
advengers
automatic mobile
...
```

Then you can run the following command to extract all the questions and the associated url with the following command

```
python ppa_generation.py --headless
```

The output will be saved as **result/paa_output.json** with the format:

```
"sushi": [
        {
            "question": "What is the most popular sushi?",
            "url": "https://www.bustle.com/p/the-most-popular-sushi-orders-on-doordash-include-a-lot-of-avocado-18011470"
        },
        {
            "question": "What day should you not eat sushi?",
            "url": "https://www.foodrepublic.com/2012/07/09/the-12-sushi-commandments/"
        },
        {
            "question": "What is best sushi for beginners?",
            "url": "https://rokaakor.com/new-to-sushi-a-simple-guide-to-eating-sushi-for-beginners/"
        },
        {
            "question": "What is the most popular type of sushi in Japan?",
            "url": "https://www.tsunagujapan.com/20-most-common-types-of-sushi-in-japan/"
        },
```
### ToDo
1. Scrape the answers that is summarized by Google from the url post
2. Classify the questions into different types. 
3. Build simple mechanism to select interesting questions for chitchat. 

