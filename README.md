# Project_Final

SI507-Final "Project_Final"
Created by: Michael Cantley

|QUESTION.1.| Data sources used, including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))

ACCESS DATA REQUIREMENTS:
--My Data source is Reddit (Specifically the subreddit "https://www.reddit.com/r/StarWarsBattlefront/"). I used Reddit's API to get data specifically from the 'hot' threads and their affiliated comments and replies. The necessary information to get this program to work is as follows:
    #client_id=s_client_id,
    #client_secret=s_client_secret,
    #user_agent=s_user_agent,
    #username=s_username,
    #password=s_password

    The above fields can be obtained by having an approved developer giving access to a user by giving the client_id and client_secrets to them. Also, a user must have a valid Reddit account and its affiliated password to access/use this application. Refer to https://www.reddit.com/dev/api/ for questions with reddit api.

TO INCORPORATE:
--After getting all the necessary identification and passwords a user should return to their primary workstation and go to the directory that holds this program. In the directory they need to make a '.gitignore' file at the same level as the main files of this program like 'proj_fin.py'. After creating a .gitignore, the user should write in that file 'secrets.py' to ignore that file and protect a users passwords. Lastly a user should create the 'secrets.py' at the same level in the directory and insert the appropriate passwords and ids.




|QUESTION.2.| Any other information needed to run the program (e.g., pointer to getting started info for plotly)

OTHER PROGRAMS:
--In addition to the base files downloaded from github, the user will need Internet Access and be using plotly for the visualization component of this program. To get started with plotly a user can create an account at "https://plotl.ly". After creating an account a user should be able to execute this program successfully as long as they have a stable Internet Connection. To become more familiar with plotly a user should go to the 'Python' section of the site and become familiar with the basic command especially the 'data' and 'layout' features of a graph. Lastly, a user should will need to install and import plotly on their device. If user wishes to add graphs and features (available on plotly) one should look more into the Python graphing section of plotly. Praw is the wrapper used to help handling of Reddit API data.
Here is what you will need to install in your virtual environment to get this to run:
--
pip install praw
pip install pandas
pip install emoji
pip install nltk
pip install plotly
--

Lastly, users will be using nltk for visualization 4, they may need to update/import nltk and download('stopwords') for this part to function as intended!



|QUESTION.3.| Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.

DESCRIPTION OF STRUCTURE:
--This Code is broken down into 7 sections.
Section 1. Simply gives the prep work and sets up appropriate default file references.
Section 2. Involves the creation of Classes, specifically the "Threads" Class. This Class is used to store information from Reddit and involved in creation of primary keys.
Section 3. Has the helper functions which are used to improve the readability and modularity of the code especailly moving the data around between files. This section also contains the menu help features for the two interfaces.
Section 4. Contains the Main functions for the program that are relevant to getting the data from the Reddit API and also from the local cache file. This section will take the data and load it into a "staging" csv for threads and comments. After staging the data in csvs this section will link those loaded csv files to the database so queries/visualization can be executed.
Section 5. Has the visualization menu and commands. This section serves as sub-menu that is accessible after the user has connected to and loaded the database with data either from a fresh call of the cache. It has several functions for visualization which are designed in this section and the viz menu. Some of the visualization features are 1) printing top 5 thread posters from cache [sorted alphabetically for ties] 2) A histogram for which times the threads returned are posted. 3) Another visualization to see a scatterplot of the total number of replies for a thread vs the number of upvotes a thread has. 4) Most common words found in thread titles.
Section 6. Menu. This is the key user interface which acts as the command center for the user. Has a help function to see all available options/commands. This menu starts the database loading and bridges you to the visualization.
Section 7. Simply to execute the menu command when a user runs this file and avoids forcing a user through the entire menu in other files, like the "test_proj_fin.py" file.

DATA FUNCTIONS: The 2 main data functions in this program are 'reddit_caller()' which pulls fresh data from the StarWarsBattlefront Reddit, specifically hot threads and as many as specified by the user, and the db_cache_loader(). The reddit caller acts as a way to refresh your database and visualizations and gives user opportunity to pull as many threads as are available through the API under the 'hot' section. Next, the db_cache_loader() is meant to serve alongside the interactive menu and cache. Its purpose is to take a specified call that has been stored and load the database up with the cached information from this old call.

CLASS DEFINITIONS:
The class Thread is created in this program. The purpose of this is twofold. First, it serves as a means to contain all the data of a thread into one unique identity. Second, it plays a critical part in the storage of data and, consequently, the interface. The Thread class will make a string that serves as a unique identifier in the cache/storage for each call by taking the first thread from the call and the total number of calls and storing it locally.

LARGE_DATA:
Primarily all contained in the 'new' command 'reddit_caller()' Two large lists are built per call where they are combined into a dictionary which is stored in the cache. The first list contains all the desired information for threads and the second contains all desired information from the Comments of the Threads returned. These will be stored based on the "call" to reddit in the dictionary by storing it as the top/first post in the 'hot' section and using the number of calls and Thread String to serve as the key to access all these specific calls.


|QUESTION.4.| Brief user guide, including how to run the program and how to choose presentation options.

USER GUIDE:
--After starting the program's execution, the user will be prompted by the main menu command. If confused, the user can always enter 'help' and they will receive all commands available to them from the main menu. In short, they first will need to get data either by pulling fresh data by typing in 'new' or if you have local data from one's cache using 'cache'. These commands will load a users database and visualization menu will be executed.
In the visualization menu the user will have the opportunity again to get 'help' or 'stop' to exit viz menu. If they decide to use the visualization there are several options described above. They will be prompted with what the functions/visualizations are. All one would need to do is enter the number of the visualization they would like to see or enter 'all' to execute all visualizations for the current database. Theses visualizations will be executed in plotly using a variety of the graphs available. After user decides to exit the viz menu they will be returned to the main menu where they can load a new data set into the database or they exit the program.
