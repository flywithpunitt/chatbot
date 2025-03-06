import pymssql

server = '127.0.0.1'
port = '1433'
database = 'AdventureWorksDW2022'
username = 'flywithpunit'
password = 'NewSecurePassword'  # Make sure this matches SSMS

try:
    conn = pymssql.connect(server=server, user=username, password=password, database=database, port=port)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM DimCustomer")
    result = cursor.fetchone()
    print("✅ Connection successful! Total users:", result[0])
except Exception as e:
    print("❌ Error:", e)
