"""
Scape the People Also Ask from a provided list of queries 
"""
import json
import argparse
import logging
#from gquestions_json_qurl import *
#from gquestions_json import *
from gquestions_json import initBrowser
from pprint import pprint


def config_args():
    parser = argparse.ArgumentParser()

    # Include al the options
    parser.add_argument('--depth', type=int, default=0,
                        help="The depth of the layers for people also ask search. The maximum depth is 1.")
    parser.add_argument('--lang', type=str, default='en',
                        help="The language for search engine. This should be kept as English")
    parser.add_argument('--in_dir', type=str, default='search_queries.txt',
                        help="The path for the input file with a list of queries that you want to search for google paa")
    parser.add_argument('--out_dir', type=str, default='result/ppa_output_full.json',
                        help="The path for the output json file")
    parser.add_argument('--backup_dir', type=str, default='result/ppa_backup.json',
                        help="The path for the backup json file for ppa")
    parser.add_argument('--headless', action='store_true',
                        help="The flag to indicate whether you want the browser pop up or not.")
    parser.add_argument('--extraction_mode', type=str,
                        default="full", help="The mode to extract the information")

    args = parser.parse_args()
    return args

# Define the Template for FOOD_GROUNDING
FOOD_GROUNDING = ["best {}", "favorite {}", "why {}"]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = config_args()

    with open(args.out_dir, 'r') as fp:
        result = json.load(fp)
    assert type(result) is dict, "The initialized result should be a dictionary"
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
    #result = {query: None for query in queries}

    if args.extraction_mode == "qurl":
        from gquestions_json_qurl import newSearch_Mingyang, crawlQuestions_Mingyang, flatten_paa_list
        for query in queries:
            if not result.get(query, None):
                try:
                    result[query] = []

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

                    result[query] += query_questions.copy()

                    # Save the result to a json file, make sure the old ones
                    # are good
                    with open(args.out_dir, 'w') as fp:
                        json.dump(result, fp, sort_keys=False, indent=4)
                except:
                    print(
                        "[FAILED_PPA] Unable to extract the questions for: {}".format(query))

    elif args.extraction_mode == "full":
        from gquestions_json import newSearch_Mingyang, crawlQuestions_Mingyang, flatten_paa_list
        for query in queries:
            if not result.get(query, None):

                result[query] = []

                # Grounding Query with Predefined Phrases
                for grounding in FOOD_GROUNDING:
                    try:
                        searched_query = grounding.format(query)
                        start_paa, start_paa_url, start_paa_answer = newSearch_Mingyang(
                            browser, searched_query)
                        # print(start_paa_answer[0])
                        # print(start_paa_parent)
                        # print(start_paa_parent.index(start_paa_answer[0]))

                        initialSet = {}
                        cnt = 0
                        for q, url, a in zip(start_paa, start_paa_url, start_paa_answer):
                            initialSet.update(
                                {cnt: {"q": q, "url": url, "a": a}})
                            cnt += 1

                        paa_list = []

                        crawlQuestions_Mingyang(start_paa, start_paa_url, start_paa_answer,
                                                paa_list, initialSet, searched_query, browser, depth)
                        # print(paa_list)
                        query_questions = []
                        flatten_paa_list(
                            paa_list, query_questions, searched_query)

                        result[query] += query_questions.copy()

                        # Save the result to a json file, make sure the old ones are
                        # good
                        with open(args.out_dir, 'w') as fp:
                            json.dump(result, fp, sort_keys=False, indent=4)
                    except:
                        print("[FAILED_PPA] Unable to extract the questions for: {}".format(
                            searched_query))

        # print(result)
    browser.close()
