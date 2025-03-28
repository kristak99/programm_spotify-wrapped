import sqlite3
import re

# Create the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS spotify_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datetime TEXT,
        artist TEXT,
        track TEXT,
        duration_min INTEGER,
        duration_sec INTEGER
    )
''')

# Paste your data here
raw_data = """
5/24/2024 16:31,Reneé Rapp,Don't Tell My Mom,3 min 9 sek
5/24/2024 16:34,Aiko,Pedestal - Eurovision version,2 min 57 sek
5/24/2024 16:38,Bambie Thug,Doomsday Blue,3 min 3 sek
5/24/2024 16:40,G Flip,GAY 4 ME (feat. Lauren Sanderson),2 min 54 sek
5/24/2024 16:45,Conan Gray,Family Line,3 min 36 sek
5/24/2024 16:49,Billie Eilish,WILDFLOWER,4 min 21 sek
5/24/2024 16:51,sundial,liar,2 min 14 sek
5/24/2024 17:03,Ashnikko,WEEDKILLER,1 min 38 sek
5/24/2024 17:56,Ashnikko,WEEDKILLER,0 min 27 sek
5/24/2024 17:59,Marina Satti,ZARI,3 min 0 sek
5/24/2024 18:02,Ladaniva,Jako,2 min 25 sek
5/24/2024 18:03,Conan Gray,The Exit,0 min 39 sek
5/24/2024 18:09,Taylor Swift,Midnight Rain,2 min 35 sek
5/24/2024 18:12,girl in red,Rue,3 min 36 sek
5/24/2024 18:15,Ashnikko,Possession of a Weapon,2 min 35 sek
5/24/2024 18:18,Taylor Swift,seven,3 min 28 sek
5/24/2024 18:21,KiNG MALA,she calls me daddy,3 min 3 sek
5/24/2024 18:26,ScHoolboy Q,Collard Greens,4 min 59 sek
5/24/2024 18:30,Jann,Gladiator,3 min 31 sek
5/24/2024 18:34,Taylor Swift,Labyrinth,4 min 7 sek
5/24/2024 18:37,Jann,Met the God,2 min 58 sek
5/24/2024 18:40,Billie Eilish,I Didn't Change My Number,2 min 38 sek
5/24/2024 18:41,Nxdia,She Likes a Boy,1 min 37 sek
"""  # <- You can add the rest here if you'd like

# Parse and insert each line
for line in raw_data.strip().split('\n'):
    parts = line.strip().split(',')
    if len(parts) != 4:
        continue  # skip bad lines

    datetime_str, artist, track, duration_str = parts
    match = re.match(r"(\d+)\smin\s(\d+)\ssek", duration_str)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
    else:
        minutes = 0
        seconds = 0

    cursor.execute('''
        INSERT INTO spotify_history (datetime, artist, track, duration_min, duration_sec)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime_str, artist, track, minutes, seconds))

# Commit and close
conn.commit()
conn.close()

print("✅ Data inserted into database.db successfully.")
