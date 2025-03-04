from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# SQL Server Connection
server = 'localhost,1433'  # Ensure this matches what worked
database = 'AdventureWorksDW2022'
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      'TrustServerCertificate=yes;'
                      'Trusted_Connection=yes;')

@app.route('/query', methods=['POST'])
def query_database():
    data = request.json
    user_input = data.get("query").lower()  # Convert input to lowercase
    
    # Query 1: Get top 5 customers by income
    if "top customers" in user_input:
        sql_query = "SELECT TOP 5 FirstName, LastName, YearlyIncome FROM DimCustomer ORDER BY YearlyIncome DESC"
        response_type = "list"

    # Query 2: Get total number of users
    elif "how many users" in user_input or "total users" in user_input:
        sql_query = "SELECT COUNT(*) FROM DimCustomer"
        response_type = "count"

    # Query 3: Get total sales amount
    elif "total sales" in user_input:
        sql_query = "SELECT SUM(SalesAmount) FROM FactInternetSales"
        response_type = "sum"

    # Query 4: Get top 5 selling products
    elif "top products" in user_input:
        sql_query = """SELECT TOP 5 ProductKey, SUM(SalesAmount) AS TotalSales 
                       FROM FactInternetSales GROUP BY ProductKey 
                       ORDER BY TotalSales DESC"""
        response_type = "list"

    # Query 5: Find a customer by email
    elif "find user" in user_input:
        email = user_input.split()[-1]  # Extract email from query
        sql_query = f"SELECT FirstName, LastName FROM DimCustomer WHERE EmailAddress = '{email}'"
        response_type = "list"

    # Query 6: Count orders placed this year
    elif "total orders this year" in user_input:
        sql_query = """SELECT COUNT(*) FROM FactInternetSales 
                       WHERE YEAR(OrderDate) = YEAR(GETDATE())"""
        response_type = "count"

    # Query 7: Get revenue by year
    elif "revenue by year" in user_input:
        sql_query = """SELECT YEAR(OrderDate) AS Year, SUM(SalesAmount) AS TotalSales 
                       FROM FactInternetSales GROUP BY YEAR(OrderDate) 
                       ORDER BY Year DESC"""
        response_type = "list"

    # Query 8: List 5 most recent orders
    elif "recent orders" in user_input:
        sql_query = """SELECT TOP 5 SalesOrderNumber, OrderDate, SalesAmount 
                       FROM FactInternetSales ORDER BY OrderDate DESC"""
        response_type = "list"

    else:
        return jsonify({"error": "Invalid request"}), 400
    
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    
    if response_type == "list":
        return jsonify({"results": [list(row) for row in results]})
    
    elif response_type == "count":
        return jsonify({"total": results[0][0]})
    
    elif response_type == "sum":
        return jsonify({"total_sales": float(results[0][0])})

if __name__ == '__main__':
    app.run(debug=True)
