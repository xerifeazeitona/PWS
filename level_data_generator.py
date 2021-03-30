"""
level_data_generator.py

Used to generate the database with levels and letters
"""
import re
import shelve
import logging
import requests
import bs4

logging.basicConfig(
    level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
logging.disable(logging.CRITICAL)

def get_url_list():
    """Get the list of urls to parse from the home page"""
    logging.debug('Getting list of urls...')
    url_list = []
    res = requests.get('https://wordscapeshelp.com/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('li a')
    for i, _ in enumerate(elems):
        if elems[i].getText().startswith('Levels '):
            parent_url = f"https://wordscapeshelp.com{elems[i].attrs.get('href', None)}"
            url_list.append(parent_url)
    return url_list

def save_url_list(url_list):
    """Save list contents to disk"""
    logging.debug('Saving list contents to disk...')
    with open('url_list.txt', 'w') as file_obj:
        for url in url_list:
            file_obj.write(f'{url}\n')

def add_levels_letters(levels_url, dic):
    """Add levels and letters from 'levels_url' to 'dic'"""
    logging.debug('Adding from %s...', levels_url)
    regex = re.compile(r'Level (\d*)\s*Letters: (\w*)')
    res = requests.get(levels_url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    elems = soup.select('div > a')

    for i, _ in enumerate(elems):
        if elems[i].getText().strip().startswith('Level'):
            mo = regex.search(elems[i].getText().strip())
            dic[mo.group(1)] = mo.group(2)

def save_level_data(dic):
    """Save 'dic' contents to a shelve file"""
    logging.debug('Saving dictionary contents...')
    shelf_file = shelve.open('level_data')
    for key, value in dic.items():
        shelf_file[key] = value
    shelf_file.close()

logging.debug('Starting...')
# Get list of urls
master_list = get_url_list()

# Add levels and letters to dictionary
logging.debug('Adding levels and letters...')
temp_dic = {}
for link_url in master_list:
    add_levels_letters(link_url, temp_dic)

# Save dictionary contents to a shelve file
save_level_data(temp_dic)
logging.debug('...all done!')
