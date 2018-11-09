#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
try:
    from itertools import izip
except ImportError:
    izip = zip


api_key_min_entropy_ratio = 0.5
api_key_min_length = 7


def get_keys_from_html(soup, class_table="req"):
    """
    Function to get the table "META" and "settings" as a dictionary
    :param soup: html parser with BeautifulSoup
    :param class_table: name of table of "META" and "settings"
    :return: return dict() example:{{'Settings': {'variable': ['ABSOLUTE_...', ..], 'value': ['data', ..]}},
    {'META': {'variable': ['CONTEXT_...', ..], 'value': ['data', ..]}}}
    """
    name_col_varible = "variable"
    name_col_value = "value"
    name_meta = "META"
    name_settings = "Settings"
    # info_data = {"META": [], "Settings": []}
    # info_data = {name_meta: [], name_settings: []}
    info_data = {name_meta: {name_col_varible: [], name_col_value: []},
                 name_settings: {name_col_varible: [], name_col_value: []}}

    tables_found = soup.find_all("table", {"class": class_table})
    for idx, table in enumerate(tables_found):
        # remove first header
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if idx == 0:
                # info_data[name_meta].append({name_col_varible: cols[0].text, name_col_value: cols[1].text})
                info_data[name_meta][name_col_varible].append(cols[0].text)
                info_data[name_meta][name_col_value].append(cols[1].text)
            elif idx == 1:
                # info_data[name_settings].append({name_col_varible: cols[0].text, name_col_value: cols[1].text})
                info_data[name_settings][name_col_varible].append(cols[0].text)
                info_data[name_settings][name_col_value].append(cols[1].text)
            else:
                pass
    if info_data[name_meta] or info_data[name_settings]:
        print(info_data)
        return info_data
    else:
        raise Exception("No data found!")


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return izip(a, b)


def token_is_api_key(token):
    """
    Returns True if the token is an API key or password. (code is taken from: https://github.com/daylen/api-key-detect)
    :param token: token in txt
    :return: ratio of key
    """
    if len(token) < api_key_min_length:
        return False, ''
    entropy = 0
    for a, b in pairwise(list(token)):
        if not ((str.islower(a) and str.islower(b)) or (str.isupper(a) and
                                                        str.isupper(b)) or (str.isdigit(a) and str.isdigit(b))):
            entropy += 1
    return float(entropy) / len(token) > api_key_min_entropy_ratio, float(entropy) / len(token)


def detect_is_key(dict_keys):
    """
    to do...!!
    detectar if value of table is an API key or password
    :param dict_keys:
    :return:
    """
    if token_is_api_key("J3h6JzJ6TAPEltECN7o0qy6GkHZ7QyVjIOhAM1Gm")[0]:
        return True
    else:
        return False