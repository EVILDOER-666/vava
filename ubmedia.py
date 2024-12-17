from pyrogram import *
from pyrogram.types import *
from apscheduler.schedulers.background import BackgroundScheduler
import os
from os import getenv



#---------------------------------+ heroku
api_id_pyrogram = int(getenv("API_ID","5282591"))
api_hash_pyrogram = getenv("API_HASH", "d416fe4e323d0e2b4616fef68a8ddd63")
string_pyrogram = getenv("SESSION_STRING" , "AQAHT9XjGobRSwnMwExkZpY-4tN0MwkBwPhud1LdKFH0MngDj7dy8pEB2lzIAtiBjeoLJcuquP2lDhJ2E6V4yqfGgReqUYrLf4AVq-KemQzWtz1CH0HBnrw62PvNz_Onm70eykWTRsTRSMOkoKg-xCkkMcQCTWEpy_-tcOtvBiFd2D6ni3FtbUo1ncktU6XfH6yUc5XRa2PjCxz3kOw_hEO_HO0Zb1C1cJ0sisgeUAcZmgVlVk6xbtX3bTPYD1YHXnLu8rloBZvLGipjhrrTTsbJS_oUgOJaW5VCIN-Nkmrxni1X67iTcsjOE8CYV3S5PWUQPSR5lSOpUzvi8zXt_EaaQSNu3gA")
g_time = int(getenv("GROUP_DELETE_TIME", "1"))
c_time = int(getenv("CHANNEL_DELETE_TIME", "15"))
group =int(getenv("NEW_GROUP", "-1002120547379"))
channel =int(getenv("NEW_CHANNEL", "-1002206212517"))

#------------------------------------end
idss = []


app = Client(name="auto-delete",session_string =string_pyrogram, api_id=api_id_pyrogram, api_hash=api_hash_pyrogram, sleep_threshold=60)
def clean_data():
    print('checking media')
    idss = []
    msgs = []
    msgs.extend(
        tuple(
            app.search_messages(
                chat_id=group, filter=enums.MessagesFilter.PHOTO_VIDEO, limit=30
            )
        )
    )
    msgs.extend(
        tuple(
            app.search_messages(
                chat_id=group, filter=enums.MessagesFilter.DOCUMENT, limit=30
            )
        )
    )
    msgs.sort(key=lambda m: m.id, reverse=True)

    for message in msgs:
        msg_id = message.id
        try:
            app.copy_message(chat_id=channel, from_chat_id=group, message_id=msg_id)
            app.delete_messages(chat_id=group, message_ids=msg_id)
            idss.append(msg_id)
        except Exception as e:
            print(f'Failed copy or delete {msg_id}', type(e), e)

    if len(idss) == 0:
        print('no photos deleted')
        return
    else:
        c = len(idss)
        print(f'cleared {c} messages out of {len(msgs)} messages')





def channel_delete():
    deleted_messages = []
    print("Trying to delete channel messages")
    try:
        for x in app.search_messages(chat_id=channel):
            if x:
                try:
                    deleted_messages.append(x.id)
                    x.delete()
                except Exception as e:
                    print(f"Error deleting message {x.id}: {e}")
    except Exception as e:
        print(f"Error searching messages: {e}")

    print(f"Almost {len(deleted_messages)} messages deleted!")
    deleted_messages.clear()



scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(clean_data, 'interval' , minutes=g_time)


scheduler.start()

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.add_job(channel_delete, 'interval' , minutes=c_time)


scheduler.start()





app.run()
