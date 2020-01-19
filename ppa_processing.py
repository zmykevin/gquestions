"""
Processing the Extracted Questions and Extracted Anaswers from PPA_JSON
file
"""
import json
import re
from pprint import pprint


class PPA_Q_SELECTOR(object):

    def __init__(self, raw_ppa):
        """
        Input:
          raw_ppa is the dictionary of the people als asking scraped data with our script
        Output:
          output is a filtered questions and answers that can be used for Module chitchat
        """
        self.raw_ppa = raw_ppa

    def select_q(self):
        filtered_ppa = {}
        for query in self.raw_ppa:
            filtered_ppa[query] = []
            for query_q in self.raw_ppa[query]:
                if self.good_question(query_q, query):
                    # processing the answer from summarized answer
                    query_q["answer"] = self.processing_answertext(query_q[
                                                                   "answer"])
                    query_q["question"] = self.processing_questiontext(query_q[
                        "question"])
                    filtered_ppa[query].append(query_q)
        return filtered_ppa

    def good_question(self, question, query):
        """
         determine whether question is a good question to keep for chitchat
        Input:
          question is the dictionary that contains question, url and summarized answer from Google PPA/
          query is the keyword that you use to search for questions
        """
        q_text = question["question"]
        q_answer = question["answer"]
        good_question = False
        """
        Check if the keyword is in the question
        """
        if re.search(query, q_text) and q_answer and self.check_answer_quality(q_answer):
            good_question = True

        return good_question

    def check_answer_quality(self, answer_text):
        """
        check if there is profanity in answer_text or if the answer is too long to be read.
        if pass return True
        """
        return True

    def processing_answertext(self, answer_text):
        """
        Remove unnecessary part from the answer_text to make it sounds less weird. 
        """
        # Remove the Time at the end of the answer
        processed_answer = answer_text.lower()
        time_regex_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) (\d*), (\d*)"
        if re.search(time_regex_pattern, processed_answer):
            processed_answer = re.sub(
                time_regex_pattern, "", processed_answer)
        return processed_answer

    def processing_questiontext(self, question_text):
        """
        Preprocessing the question_text to add grounding to the question
        """
        return question_text


class PPA_Q_SELECTOR_FOODCHAT(PPA_Q_SELECTOR):

    def __init__(self, raw_ppa):
        super().__init__(raw_ppa)
        self.foodchat_q_keywords = [r"\bwhy\b", r"\bshould\b",
                                    r"\bfavorite\b", r"\bgood\b", r"\bbad\b", r"\bmost\b", r"\bbest\b", r"\bbetter\b"]

    def good_question(self, question, query):
        q_text = question["question"]
        q_answer = question["answer"]
        good_question = super().good_question(question, query)

        if good_question:
            """
            Define the extended standards to select good questions
            """
            assert len(q_answer) > 0, "the answer should not be empty"
            if any([re.search(x, q_text) for x in self.foodchat_q_keywords]):
                good_question = True
            else:
                good_question = False

        return good_question

    def processing_answertext(self, answer_text):
        """
        Append grounding 
        """
        processed_answer = super().processing_answertext(answer_text)

        # answer_grounding = [
        #     "i hope this gives you something new about {}",
        #     "i wish you learn some interesting content about {} from this answer.",
        #     "hope my sharing teaches you some new stuff on {} that you can take home with."
        # ]
        processed_answer += " {answer_grounding}"
        return processed_answer

    def processing_questiontext(self, question_text):
        processed_question = super().processing_questiontext(question_text)
        processed_question = "{question_grounding} " + processed_question
        return processed_question


if __name__ == "__main__":
    with open("result/ppa_output_full.json", 'r') as fp:
        raw_ppa = json.load(fp)

    assert type(raw_ppa) is dict, "The initialized result should be a dictionary"
    ppa_q_selector = PPA_Q_SELECTOR_FOODCHAT(raw_ppa)
    selected_question = ppa_q_selector.select_q()
    pprint(selected_question["sushi"])

    # write the selected_question to an output file
    with open("result/ppa_selected_full.json", 'w') as fp:
        json.dump(selected_question, fp, sort_keys=False, indent=4)
