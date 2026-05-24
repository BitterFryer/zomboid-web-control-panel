from flask import Flask,render_template,request,redirect, url_for
import time
import sys 

sys.path.insert(0,'static')

from zomboid_send_commands import *
from get_zomboid_player_list import *
from file_work import *
from get_server_state import *
from mod_info_parser import * 


app = Flask(__name__)
allowed_commands= ['setaccesslevel','grantadmin','removeadmin', 'teleport','servermsg']
@app.route('/',methods = ["GET","POST"])

def mainpage(message=''):
    

    if not get_server_state(): 
        message = 'Server is offline(or restarting), you might want to try to restart it'
        players = []
        return render_template('offline_message.html',message = message)

    write_player_state_db()

    players=get_players_from_db()

    
    return render_template('index.html',online_len = len(players['online']), online_players = players['online'],offline_len=len(players['offline']),offline_players=players['offline'],message=message, allowed_commands=allowed_commands, allowed_commands_len=len(allowed_commands))

@app.route('/execute', methods = ['POST'])

def excute_input_commands():
    
    command = request.form['command']
    if not command: return redirect("https://uglyretardedfaggots.com")
    if command.startswith("/"): command=command[1:]
    if command.split()[0] in allowed_commands: zomboid_send_commands(command=command)
    else: 
        return redirect("https://uglyretardedfaggots.com")
    return redirect(url_for('mainpage'))
    

@app.route('/restart', methods = ["POST"])

def restart_zomboid_server():
    
    zomboid_send_commands("zomboid", 'quit')
    time.sleep(10)
    
    zomboid_send_commands("zomboid", './start-server.sh -servername Again')
    
    
    return redirect(url_for('mainpage'))


@app.route('/add_mods', methods=["GET","POST"])

def confirm_mod_addition():

    return render_template('add_mods.html', message='')


@app.route('/add_mod_confirmation', methods = ["GET","POST"])

def add_mod():
    
    url = request.form['mod_url']
    modID = parse_by_link(url)
    
    if not modID: 
        message='bad link' 
    else: message = modID
    return render_template('add_mods.html', message=message,url=url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


while True:
    if not get_server_state(): continue
    
