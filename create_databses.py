import sqlite3
import hashlib

###=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=###
###             FUNCTIONS             ###
###=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=###

# creates the databases used to identify users
def init_linked_databases():

    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/users.db")
    cursor = conn.cursor()

    # stores encrypted username and password information
    # unique user_id, username, and a hashed password
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_logins (user_id INTEGER PRIMARY KEY, username VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL)""")

    conn.commit()

    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/calendar.db")
    cursor = conn.cursor()

    # links user id and calendar ids
    # unique user_id, and a unique calendar id
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_calendar_link (user_id INTEGER PRIMARY KEY, calendar_id INTEGER NOT NULL UNIQUE)""")

    # collection of all user calenders
    # unique calendar id, calendar name, and timezone
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_calendars (calendar_id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL, timezone VARCHAR(128) NOT NULL)""")

    conn.commit()

    return()

# creates the databases specific to each user
def init_user_databases():

    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/events.db")
    cursor = conn.cursor()

    # indicates which calendar an event belongs to
    # unique calendar id and unique event id
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_event_link (calendar_id INTEGER PRIMARY KEY, event_id INTEGER NOT NULL UNIQUE)""")

    # there will be a difference between quests and events
    # but they will all be stored in the same table
    # quests are tasks with a due date, and distinct work on times
    # events are things that happen from a set time to a set time
    # unique event id, name, description, type, group (defined by user), start date, end/due date, difficulty, all day
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_events (event_id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL, description VARCHAR(1020), type INTEGER NOT NULL, group_name VARCHAR(128) NOT NULL, start_date DATETIME NOT NULL, end_date DATETIME NOT NULL, difficulty INTEGER NOT NULL, all_day BOOLEAN NOT NULL)""")

    # stores work on times for events
    # unique work id, event id, start time, end time
    cursor.execute("""CREATE TABLE IF NOT EXISTS event_progress_time (progress_id INTEGER PRIMARY KEY, event_id INTEGER NOT NULL, description VARCHAR(1020), start_date DATETIME NOT NULL, end_date DATETIME NOT NULL, all_day BOOLEAN NOT NULL)""")

    conn.commit()

    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/notif.db")
    cursor = conn.cursor()

    # creates a link between notifications and events
    # unique event id and unique notification id
    cursor.execute("""CREATE TABLE IF NOT EXISTS events_notifs_link (event_id INTEGER PRIMARY KEY, notif_id INTEGER NOT NULL UNIQUE)""")

    # indicates notifs and when they will be sent out
    # unique notification id, date of occurance, and user id to send to
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_notifs (notif_id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL, date DATETIME NOT NULL, user_id INTEGER NOT NULL)""")

    conn.commit()

    return()

# takes user input and creates databases for user calendar
def first_login():
    # obtain new username and password
    print("Create Account:")
    username = input("Username: ")
    # check if username is already in login table. If it is, reprompt
    password = input("Password: ")
    password = hashlib.sha256(password.encode()).hexdigest()

    # input username and password into registered logins
    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_logins (username, password) VALUES (?, ?)", (username, password))
 
    # obtain user id
    cursor.execute("SELECT user_id FROM user_logins WHERE username = ?", (username,))
    user_id_temp = cursor.fetchone()[0]
    conn.commit()

    # create user databases
    init_user_databases()
    
    # create calendar
    calendar_name = username + "'s calendar"
    timezone = input("Timezone: ") # this needs to be modified in the future to be a drop down menu
    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/calendar.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_calendars (name, timezone) VALUES (?, ?)", (calendar_name, timezone))

    # obtain calendar id
    cursor.execute("SELECT calendar_id FROM user_calendars WHERE name = ?", (calendar_name,)) # note that calendar name is not unique, but at this stage, it should be impossible to obtain the same name since usernames are unique
    calendar_id_temp = cursor.fetchone()[0]
    conn.commit()

    # upload calendar and user ids to link
    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/calendar.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_calendar_link (user_id, calendar_id) VALUES (?, ?)", (user_id_temp, calendar_id_temp))
    conn.commit()

    return()

# delete a specific table
def delete_table():
    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/calendar.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS user_calendars""")
    conn.commit()
    return()

# clear a specific table
def clear_table():
    conn = sqlite3.connect("SD_IA3_DatabaseSecurity/databases/users.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS user_logins""")
    conn.commit()
    init_linked_databases()
    return()

###=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=###
###                MAIN               ###
###=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=###

if __name__ == "__main__":

    init_linked_databases()

    # query user to create login or sign in
    # if sign in, allow access to user database connected to them
    # if create login, init a new user database

    ### create login
    # delete_table()
    # clear_table()
    first_login()
    