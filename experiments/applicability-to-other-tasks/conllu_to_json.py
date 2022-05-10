#!/usr/bin/env python3
# coding: utf-8

import json
import argparse
from itertools import permutations


# initial arguments
parser = argparse.ArgumentParser()
parser.add_argument('--conllu_input_file', help='A path to a file from Universal Dependencies.')
parser.add_argument('--json_output_file', help='A path to the resulting json file.')
args = parser.parse_args()


# load the input file
# convert to desired format
output_data = list()
with open(args.conllu_input_file, mode='r', encoding='U8') as input_file:
    sentence = list()
    for line in input_file:
        # skip comments
        if line.startswith('#'):
            continue

        line = line.rstrip('\n').split('\t')
        
        # skip empty lines, process loadded sentence
        if len(line) <= 1:
            edges, nodes = set(), set()
            edges_data, nodes_data = list(), list()
            for token, parent in sentence:
                node = {"data": {"name": token, "id": token}}
                if parent != -1:
                    edge = {"data": {"target": sentence[parent][0], "intoTree": "solid", "source": token}}

                if token not in nodes:
                    nodes_data.append(node)
                    nodes.add(token)

                if (sentence[parent][0], token) not in edges:
                    edges_data.append(edge)
                    edges.add((sentence[parent][0], token))

            output_data.append({"edges": list(edges_data), "nodes": list(nodes_data)})

            sentence = list()
            continue

        # load information from a setence
        token = '_'.join([line[0], line[1], line[2], line[3]])
        parent = int(line[6].replace('_', '0'))
        sentence.append((token, parent-1))


# store to the json file format
with open(args.json_output_file, mode='w') as output_file:
    json.dump(output_data, output_file, ensure_ascii=True)
