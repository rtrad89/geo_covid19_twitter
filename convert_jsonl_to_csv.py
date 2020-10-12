# -*- coding: utf-8 -*-
"""
Adapted from https://stackoverflow.com/a/46653313/3429115
"""

import json
import csv
import io
from datetime import datetime

'''
creates a .csv file using a Twitter .json file
the fields have to be set manually
'''

def extract_json(fileobj):
    """
    Iterates over an open JSONL file and yields
    decoded lines.  Closes the file once it has been
    read completely.
    """
    with fileobj:
        for line in fileobj:
            yield json.loads(line)    


data_json = io.open('tweets_20200501-V2.jsonl', mode='r', encoding='utf-8') # Opens in the JSONL file
data_python = extract_json(data_json)

csv_out = io.open('tweets_20200501.csv', mode='w', encoding='utf-8') #opens csv file


fields = u'id,created_at,reweet_id,user_screen_name,user_followers_count,user_friends_count,retweet_count,favourite_count,text' #field names
csv_out.write(fields)
csv_out.write(u'\n')

print(f"{datetime.utcnow()}: Output file created. Starting conversion..")

for i, line in enumerate(data_python):

    #writes a row and gets the fields from the json object
    #screen_name and followers/friends are found on the second level hence two get methods
    row = [line.get('id_str'),
           line.get('created_at'),
           line.get('retweeted_status').get('id_str') if line.get('retweeted_status') is not None else "",
           line.get('user').get('screen_name'),  
           str(line.get('user').get('followers_count')),
           str(line.get('user').get('friends_count')),
           str(line.get('retweet_count')),
           str(line.get('favorite_count')),
           '"' + line.get('full_text').replace('"','""') + '"', #creates double quotes
           ]
    
    if i%100000 == 0 and i > 0:
        print(f"{datetime.utcnow()}: {i} tweets done...")

    row_joined = u','.join(row)
    csv_out.write(row_joined)
    csv_out.write(u'\n')

print("All tweets done. Saving the csv...")
csv_out.close()
print("Done.")