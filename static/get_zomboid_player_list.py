import subprocess

def get_zomboid_player_list(session_name="zomboid", lines_to_capture=20):
    # 1. Run the raw tmux command
    # -p: pipe to stdout
    # -t: target session
    result = subprocess.run(
        ["tmux", "capture-pane", "-pt", session_name],
        capture_output=True,
        text=True,
        check=True
    )

    # 2. Clean up the output and split into individual lines
    all_lines = result.stdout.strip().split('\n')

    # 3. Reverse the list to read from bottom to top
    bottom_up_lines = all_lines[::-1]

    # 4. Return only the number of lines you actually need
    recent_logs = bottom_up_lines[:lines_to_capture]

    players=[]
    for line in recent_logs:
        # Example: Look for the player list response
        if "Players connected" in line: 
            break
        players.append(line[1::])
    return players
    
    
