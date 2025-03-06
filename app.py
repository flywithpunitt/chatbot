from flask import Flask, request, jsonify
import pymssql

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask API is live! Use /query to send requests."})

# SQL Server Configuration
DB_CONFIG = {
    "server": "127.0.0.1",  # OR "LAPTOP-15006B58"
    "port": "1433",
    "database": "AdventureWorksDW2022",
    "user": "flywithpunit",
    "password": "NewStrongPassword"
}

# Function to establish a new database connection
def get_db_connection():
    try:
        conn = pymssql.connect(
            server=DB_CONFIG["server"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        return conn
    except pymssql.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

@app.route('/query', methods=['POST'])
def query_database():
    data = request.json
    if not data or "query" not in data:
        return jsonify({"error": "Missing query parameter"}), 400
    
    user_input = data.get("query").lower()

    # ✅ SQL Queries Dictionary
    queries = {
        "total users": {
            "sql": "SELECT COUNT(*) FROM DimCustomer",
            "response_type": "count"
        },
        "top customers": {
            "sql": "SELECT TOP 5 FirstName, LastName, YearlyIncome FROM DimCustomer ORDER BY YearlyIncome DESC",
            "response_type": "list"
        },
        "total sales": {
            "sql": "SELECT SUM(SalesAmount) FROM FactInternetSales",
            "response_type": "sum"
        },
        "top products": {
            "sql": """SELECT TOP 5 ProductKey, SUM(SalesAmount) AS TotalSales 
                      FROM FactInternetSales GROUP BY ProductKey 
                      ORDER BY TotalSales DESC""",
            "response_type": "list"
        },
        "total orders this year": {
            "sql": """SELECT COUNT(*) FROM FactInternetSales 
                      WHERE YEAR(OrderDate) = YEAR(GETDATE())""",
            "response_type": "count"
        },
        "revenue by year": {
            "sql": """SELECT YEAR(OrderDate) AS Year, SUM(SalesAmount) AS TotalSales 
                      FROM FactInternetSales GROUP BY YEAR(OrderDate) 
                      ORDER BY Year DESC""",
            "response_type": "list"
        },
        "recent orders": {
            "sql": """SELECT TOP 5 SalesOrderNumber, OrderDate, SalesAmount 
                      FROM FactInternetSales ORDER BY OrderDate DESC""",
            "response_type": "list"
        }
    }

    # ✅ Special Case: Find User by Email
    if "find user" in user_input:
        email = user_input.split()[-1]  # Extract email from input
        sql_query = "SELECT FirstName, LastName FROM DimCustomer WHERE EmailAddress = %s"
        response_type = "list"
        query_params = (email,)
    else:
        # Validate if query exists in dictionary
        query_info = queries.get(user_input)
        if not query_info:
            return jsonify({"error": "Invalid request"}), 400
        sql_query = query_info["sql"]
        response_type = query_info["response_type"]
        query_params = ()

    # ✅ Get Database Connection
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query, query_params)
            results = cursor.fetchall()

        # ✅ Format Response Based on Type
        if response_type == "list":
            response = {"results": [list(row) for row in results]}
        elif response_type == "count":
            response = {"total": results[0][0] if results else 0}
        elif response_type == "sum":
            response = {"total_sales": float(results[0][0]) if results else 0.0}
        else:
            response = {"error": "Unknown response type"}

    except pymssql.Error as e:
        print(f"❌ SQL Execution Error: {e}")
        response = {"error": "SQL execution failed"}
    finally:
        conn.close()

    return jsonify(response)

if __name__ != "__main__":
    gunicorn_app = app
