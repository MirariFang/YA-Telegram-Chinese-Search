#!/usr/bin/env python
# coding: utf-8

import emoji
import re
from nltk.parse.corenlp import CoreNLPParser
import numpy as np
import os
from query.config import LOG_DIR


def read_file(filename, message_dict):
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    m_id = ''
    user_id = ''
    date = ''
    time = ''
    mode = False    # False for META, True for MESSAGE
    message_buffer = ''
    lines_num = len(lines)
    for i, line in enumerate(lines):
        # metadata
        if not mode:
            messages_info = line.split()
            m_id = int(messages_info[1])
            user_id = messages_info[2]
            date = messages_info[3]
            time = messages_info[4]
            mode = True
        else:
            if '[MESSAGE]' in line and len(line.split()) == 1:
                # empty or multimedia message
                message = ''
                mode = False
            else:
                message_list = line.split()[1:]
                message = ' '
                message = message.join(message_list)
                if (i + 1 < lines_num and lines[i+1][:6] == '[META]') or (i + 1 >= lines_num):
                    mode = False
                    message_dict[m_id] = (message, user_id, date, time)


def tokenizer():
    '''
    Initialize parser and tokenize message history log. 
    '''
    # load log files from directory
    for file in os.listdir(LOG_DIR):
        # filename = os.fsencode(file)
        filename = os.path.join(LOG_DIR, file)
        read_file(filename, messageid_message_dict)

    # Start to do the tokenization
    for m_id in messageid_message_dict.keys():
        s = messageid_message_dict[m_id][0]
        # Get the emoji
        s = emoji.demojize(s)
        # Do regular expression to remove the punctuation
        res = re.findall(
            u'([\u4e00-\u9fff0-9a-zA-Z]|(?<=[0-9])[^\u4e00-\u9fff0-9a-zA-Z]+(?=[0-9]))', s)
        s = ""
        s = s.join(res)

        # Do token
        word_list = list(parser.tokenize(s))

        # Make a word count table for each message
        word_count_dict = dict()
        for word in word_list:
            if word not in word_count_dict:
                word_count_dict[word] = 0
            word_count_dict[word] += 1
        message_id_wcount_dict[m_id] = word_count_dict

        # Make an inverted table for each word
        for word in word_list:
            if word not in inverted_index_table:
                inverted_index_table[word] = dict()
            inverted_index_table[word][m_id] = message_id_wcount_dict[m_id][word]

# Do a simple regex search in the docs


def simple_regex_search(query, mid_message_dict):
    result = []
    mid_list = sorted(mid_message_dict.keys(), reverse=True)
    for m_id in mid_list:
        if (re.search(query, mid_message_dict[m_id][0])):
            message = mid_message_dict[m_id][0]
            username = mid_message_dict[m_id][1]
            date = mid_message_dict[m_id][2]
            time = mid_message_dict[m_id][3]
            message_info_dict = {'message': message,
                                 'username': username, 'date': date, 'time': time}
            result.append(message_info_dict)
    return result


# score accumulator maps doc IDs to scores
def term_at_a_time_ranking_score(query_list, mid_message_dict, inverted_table):
    score_dict = dict()
    for word in query_list:
        if word in inverted_table:
            for m_id in inverted_table[word]:
                if m_id not in score_dict:
                    score_dict[m_id] = 0
                score_dict[m_id] += inverted_table[word][m_id]
    score_result = sorted(score_dict.items(),
                          key=lambda item: item[1], reverse=True)
    result = []
    for each_tuple in score_result:
        m_id = each_tuple[0]
        message = mid_message_dict[m_id][0]
        username = mid_message_dict[m_id][1]
        date = mid_message_dict[m_id][2]
        time = mid_message_dict[m_id][3]
        message_info_dict = {'message': message,
                             'username': username, 'date': date, 'time': time}
        result.append(message_info_dict)
    return result


# define the query dict
def get_query_dict(query_tokenized):
    query_dict = {}
    for word in query_tokenized:
        if not word in query_dict:
            query_dict[word] = 0
        query_dict[word] += 1
    return query_dict


def get_average_message_size(mid_message_dict):
    length_sum = 0
    for m_id in mid_message_dict:
        length_sum += len(mid_message_dict[m_id][0])
    return length_sum / len(mid_message_dict)


# define the BM25: assume the word are one unique word in the query, so the input for the score should be the dict
# get the score for the BM25
def get_BM25_score(query_dict, word, mid_message_dict, inverted_table, m_id, b=0.5, k=5):
    # count of word in query
    w_q_count = query_dict[word]
    # count of word in the specific message
    w_m_count = inverted_table[word][m_id]

    total_message_count = len(mid_message_dict)
    ave_message_size = get_average_message_size(mid_message_dict)

    # message length
    message_len = len(mid_message_dict[m_id][0])
    # document frequence (total number of documnets contains word w)
    document_frequency = len(inverted_table[word])

    score_part1 = w_q_count * \
        (k + 1) * w_m_count / (w_m_count + k *
                               (1 - b + b * message_len / ave_message_size))
    score_part2 = np.log((total_message_count + 1) / document_frequency)
    return score_part1 * score_part2


# BM25 score ranking
def BM_score(query_dict, inverted_table, mid_message_dict):
    score_dict = dict()
    for word in query_dict:
        if word in inverted_table:
            for m_id in inverted_table[word]:
                if m_id not in score_dict:
                    score_dict[m_id] = 0
                score_dict[m_id] += get_BM25_score(
                    query_dict, word, mid_message_dict, inverted_table, m_id)
    score_result = sorted(score_dict.items(),
                          key=lambda item: item[1], reverse=True)
    result = []
    for each_tuple in score_result:
        m_id = each_tuple[0]
        message = mid_message_dict[m_id][0]
        username = mid_message_dict[m_id][1]
        date = mid_message_dict[m_id][2]
        time = mid_message_dict[m_id][3]
        message_info_dict = {'message': message,
                             'username': username, 'date': date, 'time': time}
        result.append(message_info_dict)
    return result


def search_query(query, matched_mode='regex'):
    '''
    Search related histories using the query.
    '''
    # Parse the query
    raw_query_list = query.split()
    query_list = []
    for phrase in raw_query_list:
        # Get rid of the emoji
        phrase = emoji.demojize(phrase)
        # Do regular expression to remove the punctuation
        res = re.findall(
            u'([\u4e00-\u9fff0-9a-zA-Z]|(?<=[0-9])[^\u4e00-\u9fff0-9a-zA-Z]+(?=[0-9]))', phrase)
        phrase = ""
        phrase = phrase.join(res)
        # Do token
        query_list.extend(list(parser.tokenize(phrase)))
    query_dict = get_query_dict(query_list)

    # Start to do the search engine
    if matched_mode == 'regex':
        return simple_regex_search(query, messageid_message_dict)
    elif matched_mode == 'term_at_a_time':
        return term_at_a_time_ranking_score(query_list, messageid_message_dict, inverted_index_table)
    elif matched_mode == 'BM25':
        return BM_score(query_dict, inverted_index_table, messageid_message_dict)
    else:
        raise NameError('wrong match mode: ' + matched_mode +
                        '. Please use default mode: regex, or term_at_a_time or BM25')


messageid_message_dict = dict()
# This is for the word count table for each message
message_id_wcount_dict = dict()
# This is for the inverted index for each word: The format is {word: {chatid_messageid: count_of_word_in_this_message}}
inverted_index_table = dict()

# start the nlpparser server
# refer to https://stackoverflow.com/questions/13883277/how-to-use-stanford-parser-in-nltk-using-python/49345866#49345866
parser = CoreNLPParser('http://localhost:9001')

tokenizer()
