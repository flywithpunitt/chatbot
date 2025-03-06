import pymssql

server = "127.0.0.1"  # OR "LAPTOP-15006B58"
database = "AdventureWorksDW2022"
username = "flywithpunit"
password = "NewStrongPassword"

try:
    conn = pymssql.connect(server=server, user=username, password=password, database=database, port="1433")
    print("✅ Connection Successful!")
    conn.close()
except pymssql.Error as e:
    print(f"❌ Connection Failed: {e}")
