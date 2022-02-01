#!/usr/bin/env python3
# coding: utf-8

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# initial parameters
parser = argparse.ArgumentParser()
parser.add_argument('--input', nargs='+')
parser.add_argument('--output_text_vs_tool')
parser.add_argument('--output_individual_questions')
args = parser.parse_args()


# load data
data_questions = pd.DataFrame()
data_tools = pd.DataFrame()
questions, time, style = list(), list(), list()
total_time, total_style = list(), list()
for path in args.input:
    with open(path, mode='r', encoding='U8') as file:
        annotator_time, annotator_style = list(), ''
        for line in file:
            q, t = line.rstrip('\n').split(' ')

            questions.append(int(q[:-1]))
            time.append(int(t))
            annotator_time.append(int(t))

            if any(item in path for item in ['A2', 'A3', 'A4', 'A5', 'A6', 'A7']):
                style.append('.json')
                annotator_style = '.json'
            else:
                style.append('.tsv')
                annotator_style = '.tsv'
    
    total_style.append(annotator_style)
    total_time.append(sum(annotator_time))

data_questions['question'] = questions
data_questions['times'] = time
data_questions['style'] = style

data_tools['times'] = total_time
data_tools['style'] = total_style


# plot graphs
ax = sns.boxplot(x='style', y='times', data=data_tools, palette='colorblind', width=0.5)
ax.set(xlabel='WAY OF ANNOTATION', ylabel='TIME [s]')
plt.savefig(args.output_text_vs_tool, bbox_inches='tight')
plt.clf()

plt.figure(figsize=(20,8))
ax = sns.boxplot(x='question', y='times', hue='style', data=data_questions, palette='colorblind')#, width=0.5)
ax.set(xlabel='ANNOTATED FAMILY', ylabel='TIME [s]')
ax.legend(title='Way of annotation')
plt.savefig(args.output_individual_questions, bbox_inches='tight')
plt.clf()
