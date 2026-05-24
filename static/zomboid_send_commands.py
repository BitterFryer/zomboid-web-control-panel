import subprocess

def zomboid_send_commands(session="zomboid", command="players"):
    subprocess.run(["tmux", "send-keys", "-t", session, command, "C-m"])
