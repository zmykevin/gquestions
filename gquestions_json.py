"""
Fork the gqeustions to this script to scrape the questions for a list of entities.
"""
usage = '''
❓❔👾 Gquestions CLI Usage ❔❓

🔍 Usage:
    gquestions.py query <keyword> (en|es) [depth <depth>] [--csv] [--headless]
    gquestions.py (-h | --help)

💡 Examples:
    ▶️  gquestions.py query "flights" en              Search "flights" in English and export in html
    ▶️  gquestions.py query "flights" en --headless   Search headlessly "flights" in English and export in html
    ▶️  gquestions.py query "vuelos" es --csv         Search "vuelos" in Spanish and export in html and csv
    ▶️  gquestions.py query "vuelos" es depth 1       Search "vuelos" in Spanish with a depth of 1 and export in html
    ▶️  gquestions.py -h                              Print this message

👀 Options:
    -h, --help

'''

import os
import re
import sys
import json
import time
import datetime
import platform
from docopt import docopt
from tqdm import tqdm
from time import sleep
import pandas as pd
from pandas.io.json import json_normalize
import logging
from jinja2 import Environment, FileSystemLoader

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import json
'''
Visualizza una barra di caricamento per mostrare l'attesa
'''


class default_answer(object):

    def __init__(self):
        self.textContent = ""

    def get_attribute(self, attribute):
        return self.textContent


def sleepBar(seconds):
    for i in tqdm(range(seconds)):
        sleep(1)


def prettyOutputName(filetype='html'):
    _query = re.sub('\s|\"|\/|\:|\.', '_', query.rstrip())
    prettyname = _query
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S-%f')
    if filetype != 'html':
        prettyname += "_" + st + "." + filetype
    else:
        prettyname += "_" + st + "." + filetype
    return prettyname


def initBrowser(headless=False):
    if "Windows" in platform.system():
        chrome_path = "driver/chromedriver.exe"
    else:
        chrome_path = "driver/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--disable-features=NetworkService")
    if headless:
        chrome_options.add_argument('headless')
    return webdriver.Chrome(options=chrome_options, executable_path=chrome_path)
"""
Search on Google and returns the list of PAA questions in SERP.
"""


def newSearch(browser, query, lang="en"):
    if lang == "en":
        browser.get("https://www.google.com?hl=en")
        searchbox = browser.find_element_by_xpath(
            "//input[@aria-label='Search']")
    else:
        browser.get("https://www.google.com?hl=es")
        searchbox = browser.find_element_by_xpath(
            "//input[@aria-label='Buscar']")

    searchbox.send_keys(query)
    sleepBar(2)
    tabNTimes()
    if lang == "en":
        searchbtn = browser.find_elements_by_xpath(
            "//input[@aria-label='Google Search']")
    else:
        searchbtn = browser.find_elements_by_xpath(
            "//input[@aria-label='Buscar con Google']")
    try:
        searchbtn[-1].click()
    except:
        searchbtn[0].click()
    sleepBar(2)
    paa = browser.find_elements_by_xpath(
        "//span/following-sibling::div[contains(@class,'match-mod-horizontal-padding')]")
    hideGBar()
    return paa


"""
Search on Google and returns the list of PAA questions and corresponding url in SERP.
"""


def newSearch_Mingyang(browser, query, lang="en"):
    if lang == "en":
        browser.get("https://www.google.com?hl=en")
        searchbox = browser.find_element_by_xpath(
            "//input[@aria-label='Search']")
    else:
        browser.get("https://www.google.com?hl=es")
        searchbox = browser.find_element_by_xpath(
            "//input[@aria-label='Buscar']")

    searchbox.send_keys(query)
    sleepBar(2)
    tabNTimes(browser)
    if lang == "en":
        searchbtn = browser.find_elements_by_xpath(
            "//input[@aria-label='Google Search']")
    else:
        searchbtn = browser.find_elements_by_xpath(
            "//input[@aria-label='Buscar con Google']")
    try:
        searchbtn[-1].click()
    except:
        searchbtn[0].click()
    sleepBar(2)
    paa = browser.find_elements_by_xpath(
        "//span/following-sibling::div[contains(@class,'match-mod-horizontal-padding')]")
    paa_url = browser.find_elements_by_xpath(
        "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='g']/div/div/div[@class='r']/a")
    paa_answer_detected = browser.find_elements_by_xpath(
        "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='mod']/div/span/span[@class='e24Kjd']/../..")
    paa_answer_parent = browser.find_elements_by_xpath(
        "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='mod']/div")

    hideGBar()
    # print(paa_answer[0].get_attribute("textContent"))

    assert len(paa) == len(
        paa_url), "assert the number of questions is not matching number of urls : {}-{}".format(len(paa), len(paa_url))
    assert len(paa_answer_parent) == len(
        paa), "assert the number of question is not matching the number of answer blocks: {}-{}".format(len(paa), len(paa_answer_parent))
    # assert len(paa) == len(
    # paa_answer), "assert the number of questions is not matching number of
    # answers:{} - {}".format(len(paa), len(paa_answer))
    paa_answer = [default_answer()] * len(paa_answer_parent)

    for detected_a in paa_answer_detected:
        detected_a_index = paa_answer_parent.index(detected_a)
        paa_answer[detected_a_index] = detected_a

    return paa, paa_url, paa_answer

"""
Helper function that scroll into view the PAA questions element.
"""


def scrollToFeedback(browser, lang):
    if lang == "en":
        el = browser.find_element_by_xpath(
            "//div[@class='kno-ftr']//div/following-sibling::a[text()='Feedback']")
    else:
        el = browser.find_element_by_xpath(
            "//div[@class='kno-ftr']//div/following-sibling::a[text()='Enviar comentarios']")

    actions = ActionChains(browser)
    actions.move_to_element(el).perform()
    browser.execute_script("arguments[0].scrollIntoView();", el)
    actions.send_keys(Keys.PAGE_UP).perform()
    sleepBar(1)
"""
Accessibility helper: press TAB N times (default 2)
"""


def tabNTimes(browser, N=2):
    actions = ActionChains(browser)
    for _ in range(N):
        actions = actions.send_keys(Keys.TAB)
    actions.perform()

"""
Click on questions N times
"""


def clickNTimes(browser, el, n=1, lang="en"):
    for i in range(n):
        el.click()
        logging.info(f"clicking on ... {el.text}")
        sleepBar(1)
        scrollToFeedback(browser, lang)
        try:
            el.find_element_by_xpath("//*[@aria-expanded='true']").click()
        except:
            pass
        sleepBar(1)

"""
Hide Google Bar to prevent ClickInterceptionError
"""


def hideGBar():
    try:
        browser.execute_script(
            'document.getElementById("searchform").style.display = "none";')
    except:
        pass

"""
Where the magic happens
"""


def crawlQuestions_Mingyang(start_paa, start_paa_url, start_paa_answer, paa_list, initialSet, query, browser, depth=0, lang="en"):
    _tmp = createNode_Mingyang(paa_lst=paa_list, name=query, children=True)
    outer_cnt = 0
    for q, url, a in zip(start_paa, start_paa_url, start_paa_answer):
        scrollToFeedback(browser, lang)
        if "Dictionary" in q.text:
            continue
        test = createNode_Mingyang(paa_lst=paa_list, n=0,
                                   name=q.text,
                                   url=url.get_attribute("href"),
                                   answer=a.get_attribute("textContent"),
                                   parent=paa_list[0]["name"],
                                   children=True)

        clickNTimes(browser, q)
        new_q = showNewQuestionsURL(browser, initialSet)
        for l, value in new_q.items():
            sleepBar(1)
            question_text = value["q"].text
            logging.info(f"{l}, {question_text}")
            test1 = createNode_Mingyang(paa_lst=test[0]["children"][outer_cnt]["children"],
                                        name=value["q"].text,
                                        url=value["url"].get_attribute(
                "href"),
                answer=value['a'].get_attribute("textContent"),
                parent=test[0]["children"][
                outer_cnt]["name"],
                children=True)

        initialSet = getCurrentSERP_Mingyang(browser)
        logging.info(f"Current count: {outer_cnt}")
        outer_cnt += 1
        if depth == 1:
            for i in range(depth):
                currentQuestions = []
                for i in initialSet.values():
                    currentQuestions.append(i["q"].text)

                for i in paa_list[0]["children"]:
                    for j in i["children"]:
                        parent = j['name']
                        logging.info(parent)
                        _tmpset = set()
                        if parent in currentQuestions:
                            try:
                                if "'" in parent:
                                    xpath_compiler = '//div[text()="' + \
                                        parent + '"]'
                                else:
                                    xpath_compiler = "//div[text()='" + \
                                        parent + "']"
                                question = browser.find_element_by_xpath(
                                    xpath_compiler)
                            except NoSuchElementException:
                                continue
                            scrollToFeedback(browser, lang)
                            sleepBar(1)
                            clickNTimes(browser, question)
                            new_q = showNewQuestionsURL(browser, initialSet)
                            for l, value in new_q.items():
                                if value["q"].text == parent:
                                    continue
                                j['children'].append(
                                    {"name": value["q"].text, "parent": parent, "url": value["url"].get_attribute("href"), "answer": value['a'].get_attribute("textContent")})

                            initialSet = getCurrentSERP_Mingyang(browser)


"""
Get the current Result Page with both questions and url.

Returns:
    A list with newest questions.

"""


def getCurrentSERP_Mingyang(browser):
    _tmpset = {}
    new_paa = browser.find_elements_by_xpath(
        "//span/following-sibling::div[contains(@class,'match-mod-horizontal-padding')]")
    new_paa_url = browser.find_elements_by_xpath(
        "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='g']/div/div/div[@class='r']/a")
    # new_paa_answer = browser.find_elements_by_xpath(
    #     "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='mod']/div/span/span[@class='e24Kjd']")
    new_paa_answer_detected = browser.find_elements_by_xpath(
        "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='mod']/div/span/span[@class='e24Kjd']/../..")
    new_paa_answer_parent = browser.find_elements_by_xpath(
        "//div[contains(@class,'gy6Qzb')]/div/div/div[@class='mod']/div")

    hideGBar()
    # print(paa_answer[0].get_attribute("textContent"))

    assert len(new_paa) == len(
        new_paa_url), "assert the number of questions is not matching number of urls : {}-{}".format(len(paa), len(paa_url))
    assert len(new_paa_answer_parent) == len(
        new_paa), "assert the number of question is not matching the number of answer blocks: {}-{}".format(len(paa), len(paa_answer_parent))
    # assert len(paa) == len(
    # paa_answer), "assert the number of questions is not matching number of
    # answers:{} - {}".format(len(paa), len(paa_answer))
    new_paa_answer = [default_answer()] * len(new_paa)

    for detected_a in new_paa_answer_detected:
        detected_a_index = new_paa_answer_parent.index(detected_a)
        new_paa_answer[detected_a_index] = detected_a

    cnt = 0
    for q, url, a in zip(new_paa, new_paa_url, new_paa_answer):
        _tmpset.update({cnt: {"q": q, "url": url, "a": a}})
        cnt += 1
    newInitialSet = _tmpset
    return newInitialSet


"""
Shows new questions and URL.

Args:
    intialSet (dict): The initial set in the PAA box.
Returns:
    list of pairs of questions and url with first 3-4 questions-url pairs deleted (initalSet).
"""


def showNewQuestionsURL(browser, initialSet, initialURLSet=None):
    tmp = getCurrentSERP_Mingyang(browser)
    deletelist = [k for k, v in initialSet.items() if k in tmp and tmp[
        k]["q"] == v["q"]]

    _tst = dict.copy(tmp)

    for i, value in tmp.items():
        if i in deletelist:
            _tst.pop(i)
    return _tst


"""
Create a new node in the list for URL and addiitional Text information.

Args:
    paa_list_elements: list of web elements
    n: index of 'children' list on a main node
    name: node nome
    parent: Indicates if the node has a parent. Default to null only for first level.
    chilren: Indicates if the node has a children list. default false

Returns:
    list of questions with the current new node
"""


def createNode_Mingyang(n=-1, parent='null', children=False, name='', url='null', answer='null', *, paa_lst):
    logging.info(paa_lst)
    if children:
        _d = {
            "name": name,
            "parent": parent,
            "url": url,
            "answer": answer,
            "children": []
        }
    else:
        _d = {
            "name": name,
            "parent": parent
        }
    if n != -1:
        logging.info(paa_lst[n]["children"])
        paa_lst[n]["children"].append(_d)
    else:
        paa_lst.append(_d)

    return paa_lst

"""
This func takes in input JSON data and returns csv file.
"""


def flatten_csv(data, depth, prettyname):
    try:
        if depth == 0:
            _ = json_normalize(data[0]["children"], 'children', [
                'name', 'parent', ['children', ]], record_prefix='inner.')
            _.drop(columns=['children', 'inner.children',
                            'inner.parent'], inplace=True)
            columnTitle = ['parent', 'name', 'inner.name']
            _ = _.reindex(columns=columnTitle)
            _.to_csv(prettyname, sep=";", encoding='utf-8')
        elif depth == 1:
            df = json_normalize(data[0]["children"], meta=[
                'name', 'children', 'parent'], record_path="children", record_prefix='inner.')
            frames = [json_normalize(i) for i in df['inner.children']]
            result = pd.concat(frames)
            result.rename(
                columns={"name": "inner.inner.name", "parent": "inner.name"}, inplace=True)
            merge = pd.merge(df, result, how='left', on="inner.name")
            merge.drop(columns=['name'], inplace=True)
            columnTitle = ['parent', 'inner.parent',
                           'inner.name', 'inner.inner.name']
            merge = merge.reindex(columns=columnTitle)
            merge = merge.drop_duplicates(
                subset='inner.inner.name', keep='first')
            merge.to_csv(prettyname, sep=';', encoding='utf-8')
    except Exception as e:
        logging.warning(f"{e}")


def flatten_paa_list(paa_list, questions, root):
    for node in paa_list:
        if node["name"] != root:
            questions.append({"question": node["name"], "url": node[
                             "url"], "answer": node["answer"]})
        if node["children"]:
            flatten_paa_list(node["children"], questions, root)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)

#     args = {"depth": 0,
#             "lang": "en",
#             "headless": False
#             }

#     queries = ["sushi"]

#     depth = args["depth"]
#     lang = args["lang"]

#     if args["headless"]:
#         browser = initBrowser(True)
#     else:
#         browser = initBrowser()

#     query = queries[0]
#     result = {query: None for query in queries}

#     for query in queries:
#         start_paa, start_paa_url, start_paa_answer = newSearch_Mingyang(
#             browser, query)

#         initialSet = {}
#         cnt = 0
#         for q, url, a in zip(start_paa, start_paa_url, start_paa_answer):
#             initialSet.update({cnt: {"q": q, "url": url, "a": a}})
#             cnt += 1

#         paa_list = []

#         crawlQuestions_Mingyang(start_paa, start_paa_url, start_paa_answer,
#                                 paa_list, initialSet, depth)
#         # print(paa_list)
#         query_questions = []
#         flatten_paa_list(paa_list, query_questions, query)
#         result[query] = query_questions.copy()
#         # print(result)

#     # Save the result to a json file
#     with open("output.json", 'w') as fp:
#         json.dump(result, fp, sort_keys=False, indent=4)

#     browser.close()


#########################################Original High Level Code#############
    # crawlQuestions(start_paa, paa_list, initialSet, depth)
    # print(paa_list)
    # query_questions = []
    # flatten_paa_list(paa_list, query_questions, query)
    # result[query]["questions"] = query_questions.copy()

    # print(result)

    # browser.close()
