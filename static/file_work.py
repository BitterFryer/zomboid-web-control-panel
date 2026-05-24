import sqlite3
import time 
from get_zomboid_player_list import *
from zomboid_send_commands import *

ignored_names = ["admin" , "*"]

def return_player_list_fromdb():
    dbfile="/path/to/your/server/whitelist.db"
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    table_list_names = [a[2] for a in cur.execute("SELECT * FROM whitelist")]
    con.close()
    return table_list_names



def write_player_state_db():


    con = sqlite3.connect('db/player.db')
    cursor = con.cursor()

    create_entry_query = "INSERT OR REPLACE INTO player (Name, OnlineStatus) VALUES (?, ?)"
    update_entry_query = "UPDATE player set OnlineStatus = ?  WHERE Name = ?"

    zomboid_send_commands(command="players")
    
    time.sleep(1.5)
    

    players_in_server_db=return_player_list_fromdb() #gets server/whitlelist db for player list
    online_player_list=get_zomboid_player_list() #runs /player and returns result
    players_in_local_db=get_players_from_db()

    

    for player in players_in_server_db:
        
        #checks if it's actually a player and not a placeholder name, needs cleanup
        if player in ignored_names: continue 
        if player in players_in_local_db['online'] or player in players_in_local_db['offline'] : 
            if player in online_player_list: 
                cursor.execute(update_entry_query, (True, player))
                 
            else: 
               # print(player,46)
                cursor.execute(update_entry_query, (False, player))

            con.commit()
                       
            continue
        if player in online_player_list: cursor.execute(create_entry_query, (player, True))
        else: cursor.execute(create_entry_query, (player, False))
        con.commit()

      #  print(player)
    con.close()

def get_players_from_db():

    con = sqlite3.connect('db/player.db')
    
    
    online_players=[]
    offline_players=[]

    players = con.execute('SELECT Name, OnlineStatus FROM player').fetchall()

    for player in players:
        if player[1]: 
          #  print(player[0])      
            online_players.append(player[0])
        else: 
            offline_players.append(player[0])
    
    con.close()
    
    return {'online':online_players, 'offline': offline_players}


def clear_all_entries():
    
    con = sqlite3.connect('db/player.db')
    cursor = con.cursor()

    clear_all_query = "DELETE from player"
    cursor.execute(clear_all_query)

    con.commit()
    con.close()

    
def copy_file(orignal_file, destination_file): pass



