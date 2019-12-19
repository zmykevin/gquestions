"""
Scape the People Also Ask from a provided list of queries 
"""
import json
import argparse
from gquestions_json_qurl import *


def config_args():
    parser = argparse.ArgumentParser()

    # Include al the options
    parser.add_argument('--depth', type=int, default=0,
                        help="The depth of the layers for people also ask search. The maximum depth is 1.")
    parser.add_argument('--lang', type=str, default='en',
                        help="The language for search engine. This should be kept as English")
    parser.add_argument('--in_dir', type=str, default='search_queries.txt',
                        help="The path for the input file with a list of queries that you want to search for google paa")
    parser.add_argument('--out_dir', type=str, default='result/ppa_output.json',
                        help="The path for the output json file")
    parser.add_argument('--headless', action='store_true',
                        help="The flag to indicate whether you want the browser pop up or not.")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = config_args()

    #queries = ["sushi"]
    with open(args.in_dir, 'r') as fp:
        queries = fp.readlines()
    queries = [x.strip() for x in queries]

    depth = args.depth
    lang = args.lang

    if args.headless:
        browser = initBrowser(True)
    else:
        browser = initBrowser()

    query = queries[0]
    result = {query: None for query in queries}

    for query in queries:
        start_paa, start_paa_url = newSearch_Mingyang(
            browser, query)

        initialSet = {}
        cnt = 0
        for q, url in zip(start_paa, start_paa_url):
            initialSet.update({cnt: {"q": q, "url": url}})
            cnt += 1

        paa_list = []

        crawlQuestions_Mingyang(start_paa, start_paa_url,
                                paa_list, initialSet, query, browser, depth)
        # print(paa_list)
        query_questions = []
        flatten_paa_list(paa_list, query_questions, query)
        result[query] = query_questions.copy()
        # print(result)

    # Save the result to a json file
    with open(args.out_dir, 'w') as fp:
        json.dump(result, fp, sort_keys=False, indent=4)

    browser.close()
