import mysql.connector
import random
from datetime import datetime, timedelta

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost", 
    user="wxhack", 
    password="qweQWE12!", 
    database="wxhack",
    auth_plugin="mysql_native_password"
)
cursor = conn.cursor()

# 랜덤 데이터 생성 함수
def generate_random_data(num_records=20):
    categories = ["Electronics", "Furniture", "Clothing", "Food"]
    sub_categories = ["Sub_A", "Sub_B", "Sub_C", "Sub_D"]
    regions = ["North", "South", "East", "West"]
    countries = ["USA", "Canada", "Germany", "Japan"]
    order_statuses = ["Completed", "Pending", "Cancelled"]
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Cash"]
    shipping_methods = ["Standard", "Express", "Overnight"]
    customer_segments = ["Retail", "Wholesale", "Online"]

    data = []
    for i in range(1, num_records + 1):
        sales_id = f"S{str(i).zfill(6)}"
        date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        product_id = f"P{str(random.randint(1, 1000)).zfill(4)}"
        product_name = f"Product_{random.randint(1, 100)}"
        category = random.choice(categories)
        sub_category = random.choice(sub_categories)
        region = random.choice(regions)
        country = random.choice(countries)
        sales_rep = f"Rep_{random.randint(1, 50)}"
        customer_id = f"C{str(random.randint(1, 1000)).zfill(5)}"
        customer_name = f"Customer_{random.randint(1, 500)}"
        customer_segment = random.choice(customer_segments)
        quantity = random.randint(1, 50)
        unit_price = round(random.uniform(5.0, 500.0), 2)
        discount = round(random.uniform(0.0, 0.3), 2)
        total_price = round(quantity * unit_price * (1 - discount), 2)
        order_status = random.choice(order_statuses)
        payment_method = random.choice(payment_methods)
        shipping_method = random.choice(shipping_methods)
        feedback_score = random.randint(1, 5)

        data.append((
            sales_id, date, product_id, product_name, category, sub_category,
            region, country, sales_rep, customer_id, customer_name, customer_segment,
            quantity, unit_price, discount, total_price, order_status, payment_method,
            shipping_method, feedback_score
        ))
    return data

# 데이터 삽입
def insert_random_data(num_records=20):
    data = generate_random_data(num_records)
    insert_query = """
        INSERT INTO sales_data (
            Sales_ID, Date, Product_ID, Product_Name, Category, Sub_Category,
            Region, Country, Sales_Rep, Customer_ID, Customer_Name, Customer_Segment,
            Quantity, Unit_Price, Discount, Total_Price, Order_Status, Payment_Method,
            Shipping_Method, Feedback_Score
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, data)
    conn.commit()
    print(f"{num_records} records inserted successfully.")

# 실행
insert_random_data(100)  # 랜덤으로 100개의 데이터 삽입
conn.close()
