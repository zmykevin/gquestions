"""
Update the Template YML with the selected questions from PPA.
"""
import sys
from ruamel.yaml import YAML
import json
from collections import OrderedDict

yaml = YAML()
yaml.allow_duplicate_keys = True
inp_fo = open("food_template.yml").read()

# yaml file with new paramter in object
code = yaml.load(inp_fo)

# Load the selected question from the json
with open("result/ppa_selected_full.json", 'r') as fp:
    selected_ppa = json.load(fp)

# Created an Ordered List Object from PPA Item
query = "sushi"
ppa_list = selected_ppa[query]
ppa_example = ppa_list[0]

new_yaml_object = OrderedDict(
    [('q', []), ('a', ''), ('acknowledge', ''), ('q_id', '')])


mapped_yml_key = 'qa_{}'.format(query)
current_id = len(code['qa_templates'][mapped_yml_key]) + 1
# update the q_id
new_yaml_object['q_id'] = str('{index}_{food}'.format(current_id, query))
# update the question
new_q = ppa_example["question"]
new_yaml_object['q'].append(new_q)
# code['qa_templates']['qa_sushi']

# create a new object for qa_sushi
