import praw
import json
import csv
import sqlite3
import pandas
import emoji
import requests
from fin_secrets import *
import plotly.plotly as py
import plotly.graph_objs as go


import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

#System Preparation
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#Set up all appropriate file connections for program's execution.
CSV_STORAGE = 'Threads.csv'
COM_CSV_STORAGE = 'Comments.csv'
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
        return "'{}' is the thread title. \n Posted By: '{}' on '{}' \n With '{}' as the thread id.\n\n".format(self.title, self.author, self.date, self.thread_id)

#HELPER FUNCTIONS
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
#To prepare the database and set it up so it can be written to and queried.
def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #First Delete Tables/Clear if they already exist to provide a "fresh-start"
    del_threads = '''
        DROP TABLE IF EXISTS 'Threads';
        '''
    cur.execute(del_threads)
    conn.commit()

    del_comments = '''
        DROP TABLE IF EXISTS 'Comments';
        '''
    cur.execute(del_comments)
    conn.commit()


    stmnt_thread = '''
        CREATE TABLE IF NOT EXISTS 'Threads'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Author' TEXT,
        'Title' TEXT,
        'Num_Upvotes' INTEGER,
        'Thread_Id' TEXT,
        'Time_created' INTEGER,
        'Time_Date_Created' TEXT,
        'Hour_Created' TEXT,
        'Num_Comments' INTEGER
        )
        '''
    cur.execute(stmnt_thread)
    conn.commit()

    stmnt_comment = '''
        CREATE TABLE IF NOT EXISTS 'Comments'(
        'Comment_Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Body' TEXT,
        'Thread_ID' INTEGER,
        'Author' TEXT,
        'Comp_Identifier' TEXT,
        'Time_Date_Created' TEXT,
        'Hour_Created' TEXT,
        'Num_Replies' INTEGER,
        FOREIGN KEY('Thread_ID') REFERENCES Threads('Id')
        )
        '''
        #['Body', 'Thread_FK', 'Author', 'Comment_id', 'Date and Time created', 'Hour created', 'Num_Replies'])
    cur.execute(stmnt_comment)
    conn.commit()
    conn.close()

#To load a passed list into the csv as a "staging technique"
def csv_loader(lst_instances):
    cs_file = open(CSV_STORAGE, 'w', encoding='utf-8', newline='')
    with cs_file:
        cols_threads = csv.writer(cs_file)
        cols_threads.writerows(lst_instances)
    print(cols_threads)
    cs_file.close()

def coms_csv_loader(lst_instances):
    coms_file = open(COM_CSV_STORAGE, 'w', encoding='utf-8', newline='')
    with coms_file:
        cols_comments = csv.writer(coms_file)
        cols_comments.writerows(lst_instances)
    print(cols_comments)
    coms_file.close()


#Simply will print a "help" dialog to allow user to understand the program's features.
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

#Will connect the staged/prepared csv with the db and load the db with relevant information.
def db_loader():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    #First load the threads into the csv using the staged csv file
    cr_file = open(CSV_STORAGE, 'r', encoding='utf-8')
    ithreads_csv = csv.reader(cr_file)
    print(ithreads_csv)
    next(ithreads_csv, None)
    for thread in ithreads_csv:
        print(thread)
        print(type(thread))
        #emoji_dodger = (title_encoded.decode('unicode-escape'))
        insertion = (thread[0], thread[1], thread[2], thread[3], thread[4], thread[5], thread[6], thread[7])
        fill_stmt = '''
                INSERT INTO Threads (Author, Title, Num_Upvotes, Thread_Id, Time_Created, Time_Date_Created, Hour_Created, Num_Comments)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?
                '''
        print(fill_stmt)
        cur.execute(fill_stmt, insertion)
    conn.commit()
    cr_file.close()
    #---------------------------------------------------------------------------
    #Now load the comments into the db using the staged csv file
    com_file = open(COM_CSV_STORAGE, 'r', encoding='utf-8')
    icomments_csv = csv.reader(com_file)
    print(icomments_csv)
    next(icomments_csv, None)
    for comment in icomments_csv:
        print(comment)
        print(type(comment))
        #['Body', 'Thread_FK', 'Author', 'Comment_id', 'Date and Time created', 'Hour created', 'Num_Replies'])
        # 'Comment_Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        # 'Body' TEXT,
        # 'Thread_ID' INTEGER,
        # 'Author' TEXT,
        # 'Comp_Identifier' TEXT,
        # 'Time_Date_Created' TEXT,
        # 'Hour_Created' TEXT,
        # 'Num_Replies' INTEGER
        # encoded_body = (comment[0].encode('utf-8'))
        # c_emoji_dodger = (comment[0].decode('unicode-escape'))
        c_insertion = (comment[0], comment[1], comment[2], comment[3], comment[4], comment[5], comment[6])
        c_fill_stmt = '''
                INSERT INTO Comments (Body, Thread_ID, Author, Comp_Identifier, Time_Date_Created, Hour_Created, Num_Replies)
                SELECT ?, ?, ?, ?, ?, ?, ?
                '''
        print(c_fill_stmt)
        cur.execute(c_fill_stmt, c_insertion)
    conn.commit()
    com_file.close()

    conn.close()

def dict_maker(lst_to_dict):
	current_dict = {}
	key_counter = 1
	for i in lst_to_dict:
		st_key = str(key_counter)
		current_dict[st_key] = i
		key_counter += 1
	return(current_dict)

def cache_call():
    try:
        fw = open(CACHE_FNAME,"r")
        my_read = fw.read()
        json_read = json.loads(my_read)
        cache_keys = json_read.keys()
        cur_cache = dict_maker(cache_keys)
        print(cur_cache)
        keys = cur_cache.keys()
        for key in keys:
            print("Thread number: " + key + "\n" + "Thread_stored (Username/Time_posted): " + cur_cache[key])

        cache_num = ""
        while cache_num != "stop":
            cache_num = input("Please enter the number affiliated with the search you want to load the db with. \nOr enter 'stop' to exit this menu.\n\nNumber to pull: ")
        #Attempt to get a number from the cache
            try:
                if cache_num == "stop":
                    return("**************************************************************\nExiting Cache menu.**************************************************************\n")
                else:
                    chosen_thread = cur_cache[cache_num]
                    return chosen_thread
            except:
                print("Sorry that is not a valid selection. Pick a number in the cache list.\n")
        fw.close() # Close the open file
    except:
        # print("Currently No Cache...'refresh' or 'run' a search to establish a Cache.")
        return "Currently No Cache...'refresh' or 'run' a search to establish a Cache."


#MAIN FUNCTIONS
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def reddit_caller(num_threads=10):
    #Blanks out the dbs and allows for a fresh write/data to work with.
    init_db()
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

    complete_cache_diction = {}
    complete_cache_lst = []
    #To create unique keys and set up a "Thread" Instance
    my_threads = []
    mstr_comments_lst = []
    #To add to the Cache for the program to expedite execution
    cache_storage = []
    mstr_comments_lst.append(['Body', 'Thread_FK', 'Author', 'Comment_id', 'Date and Time created', 'Hour created', 'Num_Replies'])
    cache_storage.append(['Author', 'Title', 'Upvotes', 'Thread_id', 'Time_created', 'Date and Time created', 'Hour created', 'Num_Comments'])

    thread_fk = 1
    for thread in hot_swbf:
        thread_dict = {}
        try:
            comments_lst = []
            #Try to pull comments from a given thread. If none, continue to collect information from a thread.
            try:
                comments = thread.comments
                # print(vars(comments))
                for comment in comments:
                    com_bodys_sub = (str(comment.body).replace('\n', ' '))
                    com_bodys_sub = com_bodys_sub.encode('utf-8')
                    com_body_subo = com_bodys_sub.decode('unicode-escape')
                    com_body_sub = str(com_body_subo)
                    com_t_fk = int(thread_fk)
                    com_author_sub = str(comment.author)
                    com_id_sub = str(comment)

                    #All to get the date/time comment was created...
                    com_time_made_sub = int(comment.created_utc)
                    com_time_made_str = str(com_time_made_sub)
                    com_date_sub = pandas.to_datetime(com_time_made_str, unit='s')
                    f_com_date_sub = str(com_date_sub)
                    f_com_hour_only_sub = f_com_date_sub[11:13]

                    #print(comment.body) #returns the comment "text"
                    #thread_FK
                    #print(comment.author) #Gives comments author
                    # print(comment) #provides the comment id
                    # print(comment.created_utc) #gives the utc
                    my_replies = comment.replies
                    reply_ct = 0
                    for reply in my_replies:
                        # print(reply) #provides reply id
                        # print(reply.body) #gives the reply content
                        #print(reply.author) #gives author of reply
                        reply_ct += 1
                    print(comment.body)
                    print(reply_ct)
                    #['Body', 'Thread_FK', 'Author', 'Comment_id', 'Date and Time created', 'Hour created', 'Num_Replies'])
                    c_cache_lst = [com_body_sub, com_t_fk, com_author_sub, com_id_sub, f_com_date_sub, f_com_hour_only_sub, reply_ct]
                    comments_lst.append(c_cache_lst)
                    mstr_comments_lst.append(c_cache_lst)
                thread_dict['Comments'] = comments_lst
            except:
                thread_dict['Comments'] = comments_lst


            # print(thread.title)
            print('\n\n\n\n\n\n')

            num_comments_sub = thread.num_comments
            author_sub = str(thread.author)
            title_sub = str(thread.title)
            ups_sub = int(thread.ups)
            id_sub = str(thread)
            time_made_sub = int(thread.created_utc)
            time_made_str = str(time_made_sub)
            date_sub = pandas.to_datetime(time_made_str, unit='s')
            f_date_sub = str(date_sub)
            f_hour_only_sub = f_date_sub[11:13]

            #Build a Thread Instance
            cur_thread = Thread(p_author=author_sub, p_title=title_sub, p_ups=ups_sub, p_tid=id_sub, p_time=time_made_sub, p_date=f_date_sub, p_odate=f_hour_only_sub)
            my_threads.append(cur_thread)

            #Build a list for your cache
            t_cache_list = [author_sub, title_sub, ups_sub, id_sub, time_made_sub, f_date_sub, f_hour_only_sub, num_comments_sub]
            cache_storage.append(t_cache_list)
            thread_dict['Threads'] = cache_storage
            complete_cache_lst.append(thread_dict)
            thread_fk += 1
        except:
            pass

    # for i in my_threads:
    #     print(i)
    # print("\n\n\n\n\n")
    #Establish a unique Identifier for the returned "fresh request" by applying the class string for threads.
    #After getting unique ID throw the json formatted information into a cache.
    u_thread_ident = (my_threads[0].__str__())
    #Load the dictionary into the cache so it can be parsed between threads and affiliated comments.
    # cache_diction['threads'] = cache_storage
    # cache_diction['comments'] = comments_lst
    CACHE_DICTION[u_thread_ident] = complete_cache_lst
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    # CACHE_DICTION[u_thread_ident] = cache_storage
    # dumped_json_cache = json.dumps(CACHE_DICTION)
    # fw = open(CACHE_FNAME,"w")
    # fw.write(dumped_json_cache)
    # fw.close() # Close the open file

    #Continue on and write this information directly to CSV and load the CSV into the sqlite db
    csv_loader(cache_storage)
    coms_csv_loader(mstr_comments_lst)
    db_loader()

def cache_loader(cache_needed):
    print(cache_needed)
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
    cache_want = CACHE_DICTION[cache_needed]
    print('\n\n\n\n\n\n\n')
    print(cache_want)

    for row in cache_want:
        print(row)
        print(type(row))

    pass
    #PULL UP CACHED DATA BASED ON MENU COMMAND MANNNNNN


#VISUALIZATION____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def top_5_thread_users():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #Alphabettically ordred top users to prep for loading into a bar chart in plotly
    users_1 = []
    thread_ct_1 = []
    top_user_threads = '''
        SELECT Author, COUNT(Author)
        FROM Threads
        GROUP BY Author
        ORDER BY COUNT(Author) DESC
        '''
    cur.execute(top_user_threads)
    for user_thread_ct in cur:
        print(user_thread_ct)
        users_1.append(user_thread_ct[0])
        thread_ct_1.append(user_thread_ct[1])
    conn.close()
    #The visualization steps are below which pass the top 5 to plotly to create a bar graph
    print('\n\n\n\n\n\'')
    print(users_1)
    print('\n\n\n\n\n\'')
    print(thread_ct_1)
    users_1_top5 = users_1[:5]
    thread_ct_1_top5 = thread_ct_1[:5]
    #Potentially append here??
    trace = [go.Bar(
                x=users_1_top5,
                y=thread_ct_1_top5
        )]

    data = trace
    layout = go.Layout(
    title='Top 5 Users w Most "hot" Threads',)
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='text-hover-bar')

    # py.plot(data, filename='basic-bar')

    #Be sure to build at least four visualizations
    #1. Thread with highest number of upvotes vs. Length of title
    #2. Number of comments v Number of upvotes
    #3. Comments by the hour?----lAST
    #4. Most common used words in comments for 1 thread.
    #5. Most common used words in threads
    pass

def visual_representations():
    #Be sure to build at least four visualizations
    #1. Thread with highest number of upvotes vs. Length of title
    #2. Number of comments v Number of upvotes
    #3. Comments by the hour?
    #4. Most common used words in comments for 1 thread.
    #5. Most common used words in threads
    pass

#INTERACTION___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def menu_prompt():
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'exit':
            print("Exiting Program...")
        elif response == 'cache':
            now_cache = cache_call()
            print("\n\n")
            print(now_cache)
            cache_loader(now_cache)
        elif response == 'new':
            reddit_caller()


#FILE CONTROlS___________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    # reddit_caller(2)
    # top_5_thread_users()
    menu_prompt()
    #init_db()
    #interactive_prompt()
