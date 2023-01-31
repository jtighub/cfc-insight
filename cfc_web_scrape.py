'''
Script to scrape cfcunderwriting.com for "all externally loaded resources"
e.g. images/scripts/fonts not hosted on cfcunderwriting.com
Output: JSON file containing list of externally loaded resources
'''

###################################
# COMMENT CODE
# REQUIREMENTS .TXT
# a (hyperlink) vs link (link to external) tags 
###################################

#imports
import json
from bs4 import BeautifulSoup as soup
import requests
from collections import Counter
import re


def html_scrape(URL):
    '''Return html content of url'''
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}).content.decode("utf-8")
    html = soup(response, features="html.parser")
    return html


def get_img_tags(html):
    '''Return ALL <img> tags from html, and div tags class=img'''
    # all images seem to be hosted on cfc. challenge specifies externally loaded resources
    # does not include href links to images
    img_list_div = [img['style'].split("'")[1] for img in html.find_all('div', {'class':'img'})]
    img_list_tag = [img['src'] for img in html.find_all('img')]
    #svg_list_tag = html.find_all('svg')
    img_list = img_list_tag + img_list_div
    return img_list


def get_stylesheet(html):
    '''Return ALL <link> tags where rel=stylesheet'''
    # tried to scrape html for <style type="text/css"> as it is there when inspecting on browser but returns none
    style_list = [stylesheet['href'] for stylesheet in html.find_all('link', {'rel':'stylesheet', 'href':True})]
    external_style_list = []
    for style in style_list:
        if "http" in (style):
            external_style_list.append(style)
    return external_style_list


def get_scripts(html):
    '''Return ALL <src> scripts'''
    # print(len(script_list)) = 14 tags + 1 nested = 15 scripts
    script_list = [script for script in html.find_all('script')]
    external_script_list = []
    for script in script_list:
        try: 
            if "http" in (script['src']):
                external_script_list.append(script['src'])
        except:
            pass
    return external_script_list


def get_hyperlinks(html):
    '''Return all <a> tags (hyperlinks) with href=True'''
    # includes some irregular links '#' and 'javascript:;'
    href_list = [href['href'] for href in html.find_all('a', {'href':True})]
    return href_list


def get_privacy_policy_url(hyperlinks):
    '''
    Return URL of privacy policy page by enumurating through hyperlinks for a match
    Parameters: list of hyperlinks from <a> tags in html
    Output: hyperlink of privacy policy page
    '''
    # only returns first occurance of privacy-policy
    for c, v in enumerate(hyperlinks):
        if "privacy-policy" in v:
            print(c, f"https://cfcunderwriting.com{v}")
            return f"https://cfcunderwriting.com{v}"


def get_word_freq(html):
    '''
    Returns term frequency count of a text and saves as JSON file
    Preprocessing text: 
    > convert bs4 object to text str then to lowercase
    > regex to replace all char that are not alphabetical, new line, or apostrophe
    > replaces \n newline with single space, then splits by single space to output list of words
    '''
    # could do with lemmatizing to get root word
    bow = re.sub("[^a-zA-Z '\n]", "", html.text.lower()).replace("\n", " ").split(" ")
    # Counter object to dictionary
    word_frq = [{'term': k , 'count': v} for k, v in Counter(bow).items()]

    with open("term_frequency.json", 'w', encoding='utf-8') as outfile:
        json.dump(word_frq, outfile, indent=4)


def get_external_content(html):
    '''
    Aggregate external content of images, scripts, fonts as JSON file
    '''
    json_out = []

    for img in get_img_tags(html):
        json_out.append({'type':'image', 'src': f"https://www.cfcunderwriting.com{img}"})

    for script in get_scripts(html):
        json_out.append({'type':'script', 'src': script})

    for style in get_stylesheet(html):
        json_out.append({'type':'stylesheet', 'src': style})

    with open("external_content.json", 'w', encoding='utf-8') as outfile:
        json.dump(json_out, outfile, indent=4)


if __name__ == '__main__':
    URL = "https://www.cfcunderwriting.com/en-gb"

    html = html_scrape(URL)
    get_external_content(html)
    get_word_freq(html)