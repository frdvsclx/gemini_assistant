import sqlite3
import os

#veritabani dosyasi yolu data/assistand.db
DB_PATH = os.path.join("data","assistant.db") #env icine yazilmasi daha dogru

#database initializer
def initialize_db():
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendar(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            event_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_note(content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    
    conn.commit()
    conn.close()

def add_event(event, event_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO calendar (event, event_date) VALUES (?, ?)", (event, event_date))
   
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT content, created_at FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()
    
    conn.close()
    return notes

def get_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT event, event_date FROM calendar ORDER BY event_date DESC")
    
    events = cursor.fetchall()
    
    conn.close()
    return events
    
    
if __name__ == "__main__":
    initialize_db() #extensions-> SQLite Viewer
    add_note("su iç oh")
    add_event("toplanti var", "20.00da")
    
    print(f"NOtes: {get_notes()}")
    print(f"Events:{get_events()}")
    
    
