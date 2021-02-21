import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import csv
import json

def extract_job_headers(jobs={}, page_no=1):
    URL = f'https://www.seek.com.au/jobs-in-information-communication-technology/in-All-Perth-WA?page={page_no}&salaryrange=80000-999999&salarytype=annual&sortmode=ListedDate'

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    html_jobs_group = soup.select_one('div[data-automation="searchResults"]')

    html_jobs = html_jobs_group.select('article[data-automation="normalJob"]')

    for job in html_jobs:
        id = job['data-job-id']
        title = job.select_one('a[data-automation="jobTitle"]').get_text(' ')
        if job.select_one('a[data-automation="jobCompany"]') is not None: #can be advertised privately
            company = job.select_one('a[data-automation="jobCompany"]').get_text(' ')
        else:
            company = 'Private Advertiser'
        list_time = job.select_one('span[data-automation="jobListingDate"]').get_text(' ')
        url = job.select_one('a[data-automation="jobTitle"]')['href']
        url = f'https://seek.com.au{url}'

        if list_time[2] == 'd' and int(list_time[0:2]) > 14:
            return jobs
        else:
            jobs[id] = {
                'title': title,
                'company': company,
                'list_time': list_time,
                'url': url,
            }
    
    return extract_job_headers(jobs, page_no + 1)

jobs = extract_job_headers()



dictionary = []
with open('english_dictionary_words.txt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        dictionary.append(row[0])

trash_words = []
with open('tempdb/words_trash.txt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        trash_words.append(row[0])

buzz_words = []
with open('tempdb/words_buzz.txt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        buzz_words.append(row[0])

buzz_words_dict = []
with open('tempdb/words_buzz_dict.txt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        buzz_words_dict.append(row[0])

it_words = []
with open('tempdb/words_it.txt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        it_words.append(row[0])

it_words_dict = []
with open('tempdb/words_it_dict.txt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        it_words_dict.append(row[0])



#open each job page
job_words_array = []

cnt = 1

for job_id in jobs:
    #print(jobs[job_id]['url'])

    page = requests.get(jobs[job_id]['url'])

    soup = BeautifulSoup(page.content, 'html.parser')

    #get proper date, as time from search is the only item visible in the listing pages
    html_job_date = soup.select_one('dd[data-automation="job-detail-date"]').get_text()
    jobs[job_id]['date'] = html_job_date

    html_job_description_full = soup.select_one('div[data-automation="jobDescription"]')
    html_job_description = html_job_description_full.select_one('div[class="templatetext"]') #pull only the main info text, ignore title and footers
    if html_job_description is not None:
        html_job_description = html_job_description.get_text(' ')
    else:
        html_job_description = html_job_description_full.select_one('div[data-automation="mobileTemplate"]').get_text(' ') #sometimes only this text area exists

    jobs[job_id]['raw'] = html_job_description

    #term I.T. has to be dealt with first as lowering the case turns it into "it", also has different ways people type it
    html_job_description = html_job_description.replace(' IT ', ' _i.t._ ')
    #html_job_description = html_job_description.replace(' I.T.', ' <{i.t.}>')
    #html_job_description = html_job_description.replace(' I.T ', ' <{i.t.}> ')
    ##html_job_description = html_job_description.replace('\nIT ', ' *i.t.* ')
    ##html_job_description = html_job_description.replace('\nI.T.', ' *i.t.*')
    ##html_job_description = html_job_description.replace('\nI.T ', '*i.t.* ')

    html_job_description = html_job_description.lower()


    multi_word_phrases = []
    with open('tempdb/words_multi.txt') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            multi_word_phrases.append([row[0], row[1]])

    for phrase in multi_word_phrases:
        html_job_description = html_job_description.replace(phrase[0], f' {phrase[1]} ')

    #html_job_description = re.sub('[^A-Za-z0-9@ .`-`+<{}>}]+(?![^<{]*}>)', ' ', html_job_description)
    html_job_description = re.sub('[^A-Za-z0-9@ .`-`+_]+', ' ', html_job_description)

    #ci_it = re.compile(re.escape('I.T'), re.IGNORECASE)
    #html_job_description = ci_it.sub('*i.t.*', html_job_description)

    #search for and remove websites at this point finding https:// and www. and http://

    

    """
    html_job_description = html_job_description.replace('. ', ' ')
    html_job_description = html_job_description.replace('.\xa0', ' ')
    html_job_description = html_job_description.replace('.\n', ' ')
    html_job_description = html_job_description.replace("'s", '')
    html_job_description = html_job_description.replace("s'", '')
    html_job_description = html_job_description.replace('’s', '')
    html_job_description = html_job_description.replace('s’', '')
    html_job_description = html_job_description.replace("' ", ' ')
    html_job_description = html_job_description.replace(" '", ' ')

    
    html_job_description = html_job_description.replace('/', ' ')
    html_job_description = html_job_description.replace(' - ', ' ')
    html_job_description = html_job_description.replace('- ', ' ')
    html_job_description = html_job_description.replace(' -', ' ')
    html_job_description = html_job_description.replace('!', ' ')
    html_job_description = html_job_description.replace('?', ' ')
    html_job_description = html_job_description.replace('"', '')
    html_job_description = html_job_description.replace('“', '')
    html_job_description = html_job_description.replace('”', '')
    html_job_description = html_job_description.replace('‘', '')
    html_job_description = html_job_description.replace('(', '')
    html_job_description = html_job_description.replace(')', '')
    html_job_description = html_job_description.replace('[', '')
    html_job_description = html_job_description.replace(']', '')
    html_job_description = html_job_description.replace('{', '')
    html_job_description = html_job_description.replace('}', '')
    html_job_description = html_job_description.replace('<', '')
    html_job_description = html_job_description.replace('>', '')
    html_job_description = html_job_description.replace(',', ' ')
    html_job_description = html_job_description.replace('·', ' ')
    html_job_description = html_job_description.replace('•', ' ')
    html_job_description = html_job_description.replace('●', ' ')
    html_job_description = html_job_description.replace('®', ' ')
    html_job_description = html_job_description.replace('’', "'")
    html_job_description = html_job_description.replace(':', ' ')
    html_job_description = html_job_description.replace(';', ' ')
    html_job_description = html_job_description.replace('|', ' ')
    html_job_description = html_job_description.replace('\xa0', ' ')
    html_job_description = html_job_description.replace('\n', ' ')
    """

    html_job_description = html_job_description.replace(' - ', ' ')
    html_job_description = html_job_description.replace('- ', ' ')
    html_job_description = html_job_description.replace(' -', ' ')
    html_job_description = html_job_description.replace('. ', ' ')
    html_job_description = html_job_description.replace(' . ', ' ')
    html_job_description = html_job_description.replace(' + ', ' ')
    #html_job_description = html_job_description.replace('+ ', ' ')
    html_job_description = html_job_description.replace(' +', ' ')

    html_job_description = ' '.join(html_job_description.split())

    single_job_words_array = html_job_description.split(' ')

    #TODO find and fix fullstop issue

    single_job_words_count = Counter(single_job_words_array)

    jobs[job_id]['words_it'] = {}
    jobs[job_id]['words_buzz'] = {}
    jobs[job_id]['words_other'] = {}
    jobs[job_id]['words_unknown'] = {}

    for job_word in single_job_words_count:
        if not job_word.isdigit() and '@' not in job_word and '.com' not in job_word and '.org' not in job_word and 'www.' not in job_word:
            if job_word in it_words or job_word in it_words_dict:
                jobs[job_id]['words_it'][job_word] = single_job_words_count[job_word]
            elif job_word in buzz_words or job_word in buzz_words_dict:
                jobs[job_id]['words_buzz'][job_word] = single_job_words_count[job_word]
            elif job_word in dictionary or job_word in trash_words:
                jobs[job_id]['words_other'][job_word] = single_job_words_count[job_word]
            else:
                jobs[job_id]['words_unknown'][job_word] = single_job_words_count[job_word]

    job_words_array.append(single_job_words_array)

    #if cnt == 2:
    #    break
    #else:
    #    cnt += 1


if not job_words_array:
    print("empty")
    exit()

job_words_array_flat = [item for arr in job_words_array for item in arr]

job_words_count = Counter(job_words_array_flat)


non_dict_job_words = {}

for job_word in job_words_count:
    if job_word not in dictionary and job_word not in trash_words and job_word not in buzz_words and not job_word.isdigit() and '@' not in job_word and '.com' not in job_word and '.org' not in job_word and 'www.' not in job_word and job_word not in it_words and job_word not in it_words_dict and job_word not in buzz_words_dict:
    #if job_word in it_words or job_word in it_words_dict:
        non_dict_job_words[job_word] = job_words_count[job_word]

with open('tempdb/json_data.txt', 'w') as json_file:
    json.dump(jobs, json_file)

print({k: v for k, v in sorted(non_dict_job_words.items(), key=lambda item: item[1])})