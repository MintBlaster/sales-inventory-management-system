from flask import Blueprint, jsonify, request
from . import mysql

api_blueprint = Blueprint('api', __name__)

# Endpoint to get all customers
@api_blueprint.route('/api/stats/customers', methods=['GET'])
def get_customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT customer_id, customer_name, email, phone, city FROM Customers")
    customers = cur.fetchall()
    cur.close()

    return jsonify([{"customer_id": row[0],
                     "customer_name": row[1],
                     "email": row[2],
                     "phone": row[3],
                     "city": row[4]} for row in customers])

# Endpoint to get all products
@api_blueprint.route('/api/stats/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT product_id, product_name, category_id, price, stock_quantity FROM Products")
    products = cur.fetchall()
    cur.close()

    return jsonify([{"product_id": row[0],
                     "product_name": row[1],
                     "category_id": row[2],
                     "price": str(row[3]),  # Ensure price is a string for JSON
                     "stock_quantity": row[4]} for row in products])

# Endpoint to get all sales records
@api_blueprint.route('/api/stats/sales', methods=['GET'])
def get_sales():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT sale_id, product_id, customer_id, sale_date, quantity, total_amount 
        FROM Sales""")
    sales = cur.fetchall()
    cur.close()

    return jsonify([{"sale_id": row[0],
                     "product_id": row[1],
                     "customer_id": row[2],
                     "sale_date": row[3].isoformat(),
                     "quantity": row[4],
                     "total_amount": str(row[5])} for row in sales])  # Ensure total_amount is a string

# Total Customers Endpoint
@api_blueprint.route('/api/stats/total-customers', methods=['GET'])
def total_customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Customers")
    total_customers = cur.fetchone()[0]
    cur.close()

    return jsonify({"total_customers": total_customers})

# Total Sales Endpoint
@api_blueprint.route('/api/stats/total-sales', methods=['GET'])
def total_sales():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Sales")
    total_sales = cur.fetchone()[0]
    cur.close()

    return jsonify({"total_sales": total_sales})

# Total Revenue Endpoint
@api_blueprint.route('/api/stats/total-revenue', methods=['GET'])
def total_revenue():
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(total_amount) FROM Sales")
    total_revenue = cur.fetchone()[0] or 0.0  # Set to 0.0 if None
    cur.close()

    return jsonify({"total_revenue": str(total_revenue)})  # Ensure revenue is a string

# Average Order Value Endpoint
@api_blueprint.route('/api/stats/average-order-value', methods=['GET'])
def average_order_value():
    cur = mysql.connection.cursor()
    cur.execute("SELECT AVG(total_amount) FROM Sales")
    avg_order_value = cur.fetchone()[0]
    cur.close()

    return jsonify({"average_order_value": str(avg_order_value)})  # Ensure value is a string

# Sales by Category Endpoint
@api_blueprint.route('/api/stats/sales-by-category', methods=['GET'])
def sales_by_category():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT c.category_name, SUM(s.quantity) AS total_quantity
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        JOIN Categories c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_quantity DESC
    """)
    sales_by_category = cur.fetchall()
    cur.close()

    return jsonify([{"category": row[0], "total_quantity": str(row[1])} for row in sales_by_category])  # Ensure quantity is a string

# Total Revenue by Customer Endpoint
@api_blueprint.route('/api/stats/revenue-by-customer', methods=['GET'])
def revenue_by_customer():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT C.customer_name, SUM(S.total_amount) AS total_revenue
        FROM Sales S
        JOIN Customers C ON S.customer_id = C.customer_id
        GROUP BY C.customer_name
        ORDER BY total_revenue DESC
    """)
    revenue_by_customer = cur.fetchall()
    cur.close()

    return jsonify([{"customer_name": row[0], "total_revenue": str(row[1])} for row in revenue_by_customer])

# Sales by Product Endpoint
@api_blueprint.route('/api/stats/sales-by-product', methods=['GET'])
def sales_by_product():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT P.product_name, SUM(S.quantity) AS total_quantity_sold, SUM(S.total_amount) AS total_revenue
        FROM Sales S
        JOIN Products P ON S.product_id = P.product_id
        GROUP BY P.product_name
        ORDER BY total_revenue DESC
    """)
    sales_by_product = cur.fetchall()
    cur.close()

    return jsonify([{"product_name": row[0], "total_quantity_sold": str(row[1]), "total_revenue": str(row[2])}
                    for row in sales_by_product])

# Sales Trend by Date Endpoint
@api_blueprint.route('/api/stats/sales-trend', methods=['GET'])
def sales_trend():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT YEAR(sale_date) AS year, MONTH(sale_date) AS month, SUM(total_amount) AS total_sales
        FROM Sales
        GROUP BY YEAR(sale_date), MONTH(sale_date)
        ORDER BY year, month
    """)
    sales_trend = cur.fetchall()
    cur.close()

    return jsonify([{"year": row[0], "month": row[1], "total_sales": str(row[2])} for row in sales_trend])

# Low Stock Products Endpoint
@api_blueprint.route('/api/stats/low-stock-products', methods=['GET'])
def low_stock_products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT P.product_name, P.stock_quantity, SUM(S.quantity) AS total_sold
        FROM Products P
        LEFT JOIN Sales S ON P.product_id = S.product_id
        GROUP BY P.product_name
        HAVING P.stock_quantity <= 10 AND total_sold > 0
        ORDER BY total_sold DESC
    """)
    low_stock_products = cur.fetchall()
    cur.close()

    return jsonify([{"product_name": row[0], "stock_quantity": row[1], "total_sold": str(row[2])}
                    for row in low_stock_products])


# Top 10 Customers by Revenue Endpoint
@api_blueprint.route('/api/stats/top-customers', methods=['GET'])
def top_customers():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT C.customer_name, SUM(S.total_amount) AS total_revenue
        FROM Sales S
        JOIN Customers C ON S.customer_id = C.customer_id
        GROUP BY C.customer_name
        ORDER BY total_revenue DESC
        LIMIT 10
    """)
    top_customers = cur.fetchall()
    cur.close()

    return jsonify([{"customer_name": row[0], "total_revenue": str(row[1])} for row in top_customers])


# Top 10 Products by Sales Endpoint
@api_blueprint.route('/api/stats/top-products', methods=['GET'])
def top_products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT P.product_name, SUM(S.quantity) AS total_quantity_sold, SUM(S.total_amount) AS total_revenue
        FROM Sales S
        JOIN Products P ON S.product_id = P.product_id
        GROUP BY P.product_name
        ORDER BY total_quantity_sold DESC
        LIMIT 10
    """)
    top_products = cur.fetchall()
    cur.close()

    return jsonify([{"product_name": row[0], "total_quantity_sold": str(row[1]), "total_revenue": str(row[2])}
                    for row in top_products])
