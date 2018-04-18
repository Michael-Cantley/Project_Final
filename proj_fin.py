import praw
import json
import csv
import sqlite3
import pandas
from fin_secrets import *

import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

#System Preparation
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#Set up all appropriate file connections for program's execution.
CSV_STORAGE = 'Threads.csv'
CACHE_FNAME = 'P_FINAL_cache.json'
DBNAME = 'PROJ_FINAL.db'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

#Classes
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#Establish a Class Instance for a Reddit Thread that can store relevant information.
class Thread:
    def __init__(self, p_author="No Author", p_title="No Title", p_ups=0, p_tid="No ID", p_time=0, p_date="No Date",p_odate="No Only Date"):
        self.author = p_author
        self.title = p_title
        self.upvotes = p_ups
        self.thread_id = p_tid
        self.time = p_time
        self.date = p_date
        self.ondate = p_odate

    def __str__(self):
        return "'{}' is the thread title. \n Posted By: '{}' on '{}' \n With '{}' upvotes.\n\n".format(self.title, self.author, self.date, self.upvotes)

#HELPER FUNCTIONS
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def csv_loader(lst_instances):
    cs_file = open(CSV_STORAGE, 'w', newline='')
    with cs_file:
        cols_threads = csv.writer(cs_file)
        cols_threads.writerows(lst_instances)
    print(cols_threads)
    cs_file.close()

def ui_help():
    print("\n\n\n\n\n")
    print("------------------------------------------------------------------------------------")
    print("list <stateabbr>")
    print("      available anytime")
    print("      lists all National Sites in a state")
    print("      valid inputs: a two-letter state abbreviation")
    print("nearby <result_number>")
    print("      available only if there is an active result set")
    print("      lists all Places nearby a given result")
    print("      valid inputs: an integer 1-len(result_set_size)")
    print("map")
    print("      available only if there is an active result set")
    print("      displays the current results on a map")
    print("exit")
    print("      exits the program")
    print("help")
    print("      lists available commands (these instructions)")
    print("\n\n")



#MAIN FUNCTIONS
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def reddit_caller(num_threads=100):

    #To properly execute this code and pull from reddit a user will need the information below.
    reddit = praw.Reddit(client_id=s_client_id,
                         client_secret=s_client_secret,
                         user_agent=s_user_agent,
                         username=s_username,
                         password=s_password)

    subreddit = reddit.subreddit('StarWarsBattlefront')

    #*******************************************************************************************************************************************************************************************************************************************************************************************************Potentially come back here to CHANGE hot/
    hot_swbf = subreddit.hot(limit=num_threads)
    print(hot_swbf)

    #To create unique keys and set up a "Thread" Instance
    my_threads = []
    #To add to the Cache for the program to expedite execution
    cache_storage = []
    cache_storage.append(['Author', 'Title', 'Upvotes', 'Thread_id', 'Time_created', 'Date and Time created', 'Date created'])

    for thread in hot_swbf:
        try:
            print(thread.title)
            author_sub = str(thread.author)
            title_sub = str(thread.title)
            ups_sub = int(thread.ups)
            id_sub = str(thread)
            time_made_sub = int(thread.created_utc)
            time_made_str = str(time_made_sub)
            date_sub = pandas.to_datetime(time_made_str, unit='s')
            f_date_sub = str(date_sub)
            f_date_only_sub = f_date_sub[:10]

            #Build a Thread Instance
            cur_thread = Thread(p_author=author_sub, p_title=title_sub, p_ups=ups_sub, p_tid=id_sub, p_time=time_made_sub, p_date=f_date_sub, p_odate=f_date_only_sub)
            my_threads.append(cur_thread)

            #Build a list for your cache
            c_list = [author_sub, title_sub, ups_sub, id_sub, time_made_sub, f_date_sub, f_date_only_sub]
            cache_storage.append(c_list)
        except:
            pass

    for i in my_threads:
        print(i)
    print("\n\n\n\n\n")
    #Establish a unique Identifier for the returned "fresh request" by applying the class string for threads.
    #After getting unique ID throw the json formatted information into a cache.
    u_thread_ident = (my_threads[0].__str__())
    CACHE_DICTION[u_thread_ident] = cache_storage
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file

    #Continue on and write this information directly to CSV and load the CSV into the sqlite db
    csv_loader(cache_storage)


#INTERACTION___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def menu_prompt():
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'exit':
            print("Exiting Program...")


#FILE CONTROlS___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    reddit_caller()
    #menu_prompt()
    #init_db()
    #interactive_prompt()
