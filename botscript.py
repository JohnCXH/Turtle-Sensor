import configparser
import os
from telethon import TelegramClient, events 
from datetime import datetime
import MySQLdb 

# initializes configuration for the bot using config.ini
print("Initializing configuration...")
config = configparser.ConfigParser()
config.read('./config.ini')
config.sections()

# sets session name and uses config.ini values from telethon
API_ID = config.get('default','api_id') 
API_HASH = config.get('default','api_hash')
BOT_TOKEN = config.get('default','bot_token')
session_name = "sessions/Bot"

# database information
HOSTNAME = config.get('default','hostname')
USERNAME = config.get('default','username')
PASSWORD = config.get('default','password')
DATABASE = config.get('default','database')
 
# starts the telethon client
client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)


# start command for the bot
@client.on(events.NewMessage(pattern="(?i)/start"))
async def start(event):
    # Get sender
    sender = await event.get_sender()
    SENDER = sender.id
    
    # set text and send message
    text = "🤖Hello would you like an update on the current turtle conditions? Use /display🤖"
    await client.send_message(SENDER, text)


# function for selecting information in the database
def create_message_select_query(ans):
    text = ""
    for i in ans:
        bounding_box_id = i[0]
        colour_change = i[1]
        time_changed = i[2]
        text += "<b>"+ str(bounding_box_id) +"</b> | " + "<b>"+ str(colour_change) +"</b> | " + "<b>"+ str(time_changed) +"</b>\n"
    message = "<b>🤖Retreived </b> All information about current turtles🐢! Thanks for using our bot!\nBot is now disconnected🤖\n\n"+text
    return message

# select command
@client.on(events.NewMessage(pattern="(?i)/display"))
async def select(event):
    conn_mysql = MySQLdb.connect( host=HOSTNAME, user=USERNAME, passwd=PASSWORD,database=DATABASE)
    crsr_mysql = conn_mysql.cursor()
    
    try:
        sender = await event.get_sender()
        SENDER = sender.id
        # selects all data from turtles
        crsr_mysql.execute("SELECT * FROM colour_changes")
        fetched = crsr_mysql.fetchall() # fetches all info about turtles
        #if there is data,print fetched text, else return default text 
        if(fetched):
            text = create_message_select_query(fetched) 
            await client.send_message(SENDER, text, parse_mode='html')
            crsr_mysql.close()
            conn_mysql.close()
            
            
        else:
            text = "🤖No information on current turtles were found! Thanks for using our bot!\nBot is now disconnected🤖"
            await client.send_message(SENDER, text, parse_mode='html')
            crsr_mysql.close()
            conn_mysql.close()

    except Exception as e: 
        print(e)
        await client.send_message(SENDER, "🤖Error Occured!🤖", parse_mode='html')
        return



# creates database
def create_database(query):
    try:
        crsr_mysql.execute(query)
        print("🤖Database created successfully🤖")
    except Exception as e:
        print(f"WARNING: '{e}'")

##### MAIN
if __name__ == '__main__':
    try:
        print("🤖Initializing Database...🤖")
        conn_mysql = MySQLdb.connect( host=HOSTNAME, user=USERNAME, passwd=PASSWORD,database=DATABASE)
        crsr_mysql = conn_mysql.cursor()
    
        
        print("🤖Bot Started🤖")
        client.run_until_disconnected()

    except Exception as error:
        print('Cause: {}'.format(error))