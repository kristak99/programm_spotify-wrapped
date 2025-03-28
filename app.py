from flask import Flask, render_template  # Flask ļauj izveidot tīmekļa serveri un rādīt HTML failus
import sqlite3  # SQLite bibliotēka – vienkāršai datubāzes izmantošanai
import pandas as pd  # Pandas – datu apstrādei tabulu veidā
import os  # OS modulis – var noderēt failu pārvaldībai

# Inicializē Flask aplikāciju
app = Flask(__name__)

# Datubāzes faila nosaukums
DATABASE_FILE = "database.db"

# Funkcija, kas pārbauda, vai datubāze eksistē, un, ja nav – izveido to
def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)  # Savienojums ar datubāzi
    cursor = conn.cursor()
    # Izveido tabulu "songs", ja tā vēl neeksistē
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- unikāls ID katrai rindai
            song TEXT NOT NULL,                    -- dziesmas nosaukums
            artist TEXT NOT NULL,                  -- izpildītājs
            playtime INTEGER NOT NULL              -- atskaņošanas laiks (sekundēs)
        )
    ''')
    conn.commit()
    conn.close()

# Funkcija, kas nolasa visus datus no datubāzes un atgriež kā Pandas DataFrame
def get_data():
    conn = sqlite3.connect(DATABASE_FILE)
    df = pd.read_sql_query("SELECT * FROM songs", conn)  # Izvelk visus ierakstus
    conn.close()
    return df  # Atgriež datus tabulas formā

# Sākumlapa – tikai HTML ar pogu, kas aizved uz /wrapped
@app.route('/')
def index():
    return render_template('index.html')

# Wrapped lapa – parāda top datus no datubāzes
@app.route('/wrapped')
def wrapped():
    df = get_data()  # Ielādē visus datus no datubāzes

    # Top 5 izpildītāji pēc biežuma
    top_artists = df['artist'].value_counts().head(5).index.tolist()

    # Grupē pēc dziesmas un saskaita atskaņošanas laiku
    top_songs_df = df.groupby('song')['playtime'].sum().nlargest(10).reset_index()
    least_played_songs_df = df.groupby('song')['playtime'].sum().nsmallest(10).reset_index()

    # Konvertē uz Python sarakstiem, lai varētu rādīt HTML lapā
    top_songs = top_songs_df.to_dict(orient='records')
    least_played_songs = least_played_songs_df.to_dict(orient='records')

    # Atgriež HTML lapu kopā ar datiem
    return render_template('wrapped.html',
                           top_artists=top_artists,
                           top_songs=top_songs,
                           least_played_songs=least_played_songs)

# Šis kods izpildās tikai tad, ja skripts palaists tieši (nevis importēts)
if __name__ == '__main__':
    initialize_database()  # Pārliecinās, ka datubāze eksistē
    app.run(debug=True)  # Startē Flask serveri (debug režīmā)
