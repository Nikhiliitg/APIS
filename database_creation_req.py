import sqlite3

def create_table():
    conn = sqlite3.connect('api_requests.db')
    cursor = conn.cursor()

    # Create the 'requests' table
    cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
                        username TEXT PRIMARY KEY,
                        status TEXT,
                        api_key TEXT)''')

    conn.commit()
    conn.close()

# Call the function to create the table
create_table()

print("Table 'requests' created successfully.")

def insert_sample_request():
    conn = sqlite3.connect('api_requests.db')
    cursor = conn.cursor()

    # Insert a dummy pending request
    cursor.execute("INSERT OR IGNORE INTO requests (username, status) VALUES (?, ?)", ("john_doe", "pending"))
    
    conn.commit()
    conn.close()

insert_sample_request()
