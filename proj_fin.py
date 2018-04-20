import praw
import json
import csv
import sqlite3
import pandas
import emoji
import requests
from fin_secrets import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import plotly.plotly as py
import plotly.graph_objs as go


import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

#System_Preparation_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

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

#Classes____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

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

#HELPER_FUNCTIONS_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

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
    cur.execute(stmnt_comment)
    conn.commit()
    conn.close()

#To load a passed list into the csv as a "staging technique"
def csv_loader(lst_instances):
    cs_file = open(CSV_STORAGE, 'w', encoding='utf-8', newline='')
    with cs_file:
        cols_threads = csv.writer(cs_file)
        cols_threads.writerows(lst_instances)
    # print(cols_threads)
    cs_file.close()

def coms_csv_loader(lst_instances):
    coms_file = open(COM_CSV_STORAGE, 'w', encoding='utf-8', newline='')
    with coms_file:
        cols_comments = csv.writer(coms_file)
        cols_comments.writerows(lst_instances)
    # print(cols_comments)
    coms_file.close()


#Simply will print a "help" dialog to allow user to understand the program's features.
def ui_help():
    print("\n\n\n\n\n")
    print("------------------------------------------------------------------------------------")
    print("new (<#_to_pull>)")
    print("      will call to reddit and fill the csv files and the database with current reddit threads")
    print("      the number a user enters will pull that many threads and their affiliated comments")
    print("      user will be pushed into visualization menu to display the loaded data")
    print("      ***Will turn ON the database, so a user can now request for viualizations")
    print("cache")
    print("      pulls up the keys/datasets stored locally in the cache file of the program")
    print("      user will be prompted to select the number of the data set they want and be put into visualization menu")
    print("      ***Will turn ON the database, so a user can now request for viualizations")
    print("help")
    print("      lists available commands (these instructions)")
    print("exit")
    print("      exits the program")
    print("\n\n")

#Simply will print a "help" dialog to allow user to understand the visualization options for the data.
def viz_help():
    print("\n\n\n\n\n")
    print("------------------------------------------------------------------------------------")
    print("1 = Will display the top 5 users who have the most 'hot' threads in the current database. (If tie, alphabetically returned)")
    print("2 = Displays the hour of the day each thread was posted in a histogram (military time)")
    print("3 = Plots the total number of replies for a given thread and the number against the number of upvotes a thread has documented")
    print("4 = Puts top 5 words across all thread titles into a pie chart, shows what proportion of top 5 each word represents\n\n")
    print("'all' = Runs all of the above visualizations")
    print("------------------------------------------------------------------------------------")
    print("'stop' = Returns user to main menu.")
    print("\n\n")

#Will connect the staged/prepared csv with the db and load the db with relevant information.
def db_loader():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #To wipe the db clean and allow for "fresh" new data to be loaded in
    init_db()

    #First load the threads into the csv using the staged csv file
    cr_file = open(CSV_STORAGE, 'r', encoding='utf-8')
    ithreads_csv = csv.reader(cr_file)
    # print(ithreads_csv)
    #emoji_dodger = (title_encoded.decode('unicode-escape'))
    next(ithreads_csv, None)
    for thread in ithreads_csv:
        insertion = (thread[0], thread[1], thread[2], thread[3], thread[4], thread[5], thread[6], thread[7])
        fill_stmt = '''
                INSERT INTO Threads (Author, Title, Num_Upvotes, Thread_Id, Time_Created, Time_Date_Created, Hour_Created, Num_Comments)
                SELECT ?, ?, ?, ?, ?, ?, ?, ?
                '''
        cur.execute(fill_stmt, insertion)
    conn.commit()
    cr_file.close()
    #---------------------------------------------------------------------------
    #Now load the comments into the db using the staged csv file
    com_file = open(COM_CSV_STORAGE, 'r', encoding='utf-8')
    icomments_csv = csv.reader(com_file)
    next(icomments_csv, None)
    for comment in icomments_csv:

        c_insertion = (comment[0], comment[1], comment[2], comment[3], comment[4], comment[5], comment[6])
        c_fill_stmt = '''
                INSERT INTO Comments (Body, Thread_ID, Author, Comp_Identifier, Time_Date_Created, Hour_Created, Num_Replies)
                SELECT ?, ?, ?, ?, ?, ?, ?
                '''
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
        # print(cur_cache)
        keys = cur_cache.keys()
        for key in keys:
            print("Thread number: " + key + "\n" + "Thread_stored (Username/Time_posted): " + cur_cache[key])

        cache_num = ""
        while cache_num != "stop":
            cache_num = input("Please enter the number affiliated with the search you want to load the db with. \nOr enter 'stop' to exit this menu.\n\nNumber to pull: ")
        #Attempt to get a number from the cache
            try:
                if cache_num == "stop":
                    print("\n**************************************************************\nExiting Cache menu.\n**************************************************************\n")
                    return "stop cache"
                else:
                    chosen_thread = cur_cache[cache_num]
                    return chosen_thread
            except:
                print("Sorry that is not a valid selection. Pick a number in the cache list.\n")
        fw.close() # Close the open file
    except:
        # print("Currently No Cache...'refresh' or 'run' a search to establish a Cache.")
        return "Currently No Cache...'refresh' or 'run' a search to establish a Cache."


#MAIN_FUNCTIONS_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

def reddit_caller(num_threads=100):
    #Blanks out the dbs and allows for a fresh write/data to work with.
    init_db()
    #To properly execute this code and pull from reddit a user will need the information below.
    reddit = praw.Reddit(client_id=s_client_id,
                         client_secret=s_client_secret,
                         user_agent=s_user_agent,
                         username=s_username,
                         password=s_password)

    subreddit = reddit.subreddit('StarWarsBattlefront')

    hot_swbf = subreddit.hot(limit=num_threads)
    # print(hot_swbf)

    complete_cache_diction = {}
    complete_cache_lst = []
    #To create unique keys and set up a "Thread" Instance
    my_threads = []
    mstr_threads_lst =[]
    mstr_comments_lst = []

    #To add to the Cache for the program to expedite execution
    cache_storage = []
    mstr_comments_lst.append(['Body', 'Thread_FK', 'Author', 'Comment_id', 'Date and Time created', 'Hour created', 'Num_Replies'])
    # cache_storage.append(['Author', 'Title', 'Upvotes', 'Thread_id', 'Time_created', 'Date and Time created', 'Hour created', 'Num_Comments'])
    mstr_threads_lst.append(['Author', 'Title', 'Upvotes', 'Thread_id', 'Time_created', 'Date and Time created', 'Hour created', 'Num_Comments'])
    thread_fk = 1
    for thread in hot_swbf:
        thread_dict = {}
        try:
            comments_lst = []
            #Try to pull comments from a given thread. If none, continue to collect information from a thread.
            #Attempt to process information for the "Thread" and prepare comments instances.
            try:
                comments = thread.comments
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

                    my_replies = comment.replies
                    reply_ct = 0
                    for reply in my_replies:
                        reply_ct += 1

                    c_cache_lst = [com_body_sub, com_t_fk, com_author_sub, com_id_sub, f_com_date_sub, f_com_hour_only_sub, reply_ct]
                    comments_lst.append(c_cache_lst)
                    mstr_comments_lst.append(c_cache_lst)
                thread_dict['Comments'] = comments_lst
            except:
                pass
                comments_lst.append( ["Unavailable", "Unavailable", "Unavailable", "Unavailable", "Unavailable", "Unavailable"])

            #process information for the "Thread" and prepare a thread instance.
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
            mstr_threads_lst.append(t_cache_list)
            thread_fk += 1
        except:
            pass

    #Establish a unique Identifier for the returned "fresh request" by applying the class string for threads.
    #After getting unique ID throw the json formatted information into a cache.
    u_thread_ident = (my_threads[0].__str__())
    u_thread_ident = (str(num_threads) + " -number of threads\n" + u_thread_ident)
    complete_cache_diction['Threads'] = mstr_threads_lst
    complete_cache_diction['Comments'] = mstr_comments_lst
    #Load the dictionary into the cache so it can be parsed between threads and affiliated comments.

    CACHE_DICTION[u_thread_ident] = complete_cache_diction
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file

    #Continue on and write this information directly to CSV and load the CSV into the sqlite db
    csv_loader(mstr_threads_lst)
    coms_csv_loader(mstr_comments_lst)
    db_loader()


def db_cache_loader(cache_needed):
    # print(cache_needed)
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
    cache_want = CACHE_DICTION[cache_needed]
    threads_specd = cache_want['Threads']
    comments_specd = cache_want['Comments']

    csv_loader(threads_specd)
    coms_csv_loader(comments_specd)
    db_loader()



#VISUALIZATION________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def visual_rep_menu():
    #Be sure to build at least four visualizations
    print("******************************************************************************************************************************************\nWELCOME TO THE VISUALIZATION MENU\n******************************************************************************************************************************************")
    visualization_req = ""
    while visualization_req != "stop":
        viz_help()
        visualization_req = input("\nPlease enter a visualization # for your data to display.\n\nEnter visualization: ")
        if visualization_req == "stop":
            print("Exiting Visualization Menu...\n\n-----------------------------")
            return
        # elif visulization_req == "help":
        #     viz_help()
        elif visualization_req == "1":
            print(visualization_req)
            top_5_thread_users()
        elif visualization_req == "2":
            print(visualization_req)
            hours_post_thread()
        elif visualization_req == "3":
            print(visualization_req)
            tot_replies_v_thrd_upvotes()
        elif visualization_req == "4":
            print(visualization_req)
            most_common_thread_words()
        # elif visualization_req == "5":
        #     print(visualization_req)
        elif visualization_req == "all":
            print(visualization_req)
            top_5_thread_users() #Run viz 1
            hours_post_thread() #Run viz 2
            tot_replies_v_thrd_upvotes() #Run viz 3
            most_common_thread_words() #Run viz 4
        else:
            print("ERROR. Invalid Command, Try again.")


#-Visualization 1-#############################################################
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
        users_1.append(user_thread_ct[0])
        thread_ct_1.append(user_thread_ct[1])
    conn.close()
    #The visualization steps are below which pass the top 5 to plotly to create a bar graph

    users_1_top5 = users_1[:5]
    thread_ct_1_top5 = thread_ct_1[:5]

    trace = [go.Bar(
                x=users_1_top5,
                y=thread_ct_1_top5)]

    data = trace
    layout = go.Layout(
    title='Top 5 Users w Most "hot" Threads',)
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='text-hover-bar')



#-Visualization 2-##############################################################
def hours_post_thread():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #Alphabettically ordred top users to prep for loading into a bar chart in plotly
    hours_2 = []
    num_threads_2 = []
    hours_posted_threads = '''
        SELECT t.Hour_Created
        FROM Threads AS t
        '''
    cur.execute(hours_posted_threads)
    for hour_post_ct in cur:
        hours_2.append(hour_post_ct[0])
    conn.close()

    data = [go.Histogram(x=hours_2, xbins=dict(start=0, size=4, end=23))]

    layout = go.Layout(title='Time posted for threads of interest', xaxis=dict(title='Hour of Day (Military Time)'), yaxis=dict(title='Number of threads posted in time range'), bargap=0.05,)

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic historgram')


#-Visualization 3-##############################################################
def tot_replies_v_thrd_upvotes():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #Alphabettically ordred top users to prep for loading into a bar chart in plotly
    rthrd_upvotes_3 = []
    replies_thread_3 = []
    repz_v_upvotes = '''
        SELECT t.title, t.Num_Upvotes, SUM(c.Num_Replies)
        FROM Threads AS t JOIN Comments AS c
	           ON t.Id=c.Thread_ID
        GROUP BY c.Thread_ID
        '''
    cur.execute(repz_v_upvotes)
    for rep_ups_ct in cur:

        rthrd_upvotes_3.append(rep_ups_ct[1])
        replies_thread_3.append(rep_ups_ct[2])
    conn.close()

#PLOTLY#
    trace = go.Scatter(
        x = rthrd_upvotes_3,
        y = replies_thread_3,
        mode = 'markers')

    layout = go.Layout(title='Thread Upvotes v Thread Total Number of Replies', xaxis=dict(title='Number of Upvotes'), yaxis=dict(title='Threads number of total replies (all comments)'))
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    # Plot and embed in ipython notebook!
    py.plot(fig, filename='upvote-replies-scatter')


#-Visualization 4-##############################################################
def most_common_thread_words():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #Alphabettically ordred top users to prep for loading into a bar chart in plotly
    super_title_4 = ''
    hours_posted_threads = '''
        SELECT t.title, t.Num_Upvotes
        FROM Threads AS t
        '''
    cur.execute(hours_posted_threads)
    for td_title in cur:
        str_title = str(td_title[0])
        super_title_4 += str_title
    my_tokens_4 = nltk.word_tokenize(super_title_4)
    conn.close()

    #User must have proper nltk commands and donwload('stopwords') for this to work.
    #Collect Stop_words defaulted by nltk software. https://pythonspot.com/nltk-stop-words/
    stopWords = set(stopwords.words('english'))
    #Filter out all the stop_words to get a unique word list.
    no_stops_4 = []
    for word in my_tokens_4:
        if word not in stopWords:
            if word.isalpha():
                no_stops_4.append(word)
    nltk_fin_dist_4 = nltk.FreqDist(no_stops_4)
    top_5_4 = nltk_fin_dist_4.most_common(5)

    pie_words_4 = []
    pie_vals_4 = []
    for word_ct_4 in top_5_4:
        pie_words_4.append(str(word_ct_4[0]))
        pie_vals_4.append(int(word_ct_4[1]))

    #Plotly information
    labels = pie_words_4
    values = pie_vals_4
    trace = go.Pie(labels=labels, values=values, textfont=dict(size=20, color="white"), marker=dict(line=dict(color='#000000', width=2)))

    py.plot([trace], filename='thread_words_pie_chart')



#INTERACTION________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def menu_prompt():
    response = ''
    db = False
    while response != 'exit':
        if db == False:
            response = input('Enter a command: ')

            if response == 'exit':
                print("Exiting Program...")
            elif response == 'help':
                ui_help()
            elif response == 'cache':
                now_cache = cache_call()
                if now_cache != "stop cache":
                    db_cache_loader(now_cache)
                    db = True
                else:
                    print("Returning to Main Menu!")
            elif response[:3] == 'new':
                try:
                    my_num = int(response[4:])
                    reddit_caller(my_num)
                    db = True
                except:
                    print("Returning default value of 100 threads")
                    reddit_caller()
                    db = True
            else:
                print("Command Not recognized" + response)
        else:
            visual_rep_menu()
            db = False


#FILE CONTROlS____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    menu_prompt()
    #init_db()
    #interactive_prompt()
    # reddit_caller(2)
    # top_5_thread_users()

#End of File
