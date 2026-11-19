import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="123123",
            database="shoe_shop"
        )
        if connection.is_connected():
            print("1.Соединение с базой данных успешно установлено")
        return connection
    except Error as e:
        print(f"1.Ошибка подключения: {e}")
        return None


def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("3.Соединение с базой данных закрыто")


def get_products():
    connection = create_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                p.name_product,
                i.name_industry,
                c.name_category,
                p.composition,
                p.price,
                p.picture,
                COALESCE(SUM(s.count), 0) AS total_count
            FROM products p
            LEFT JOIN industries i ON p.id_industry = i.id_industry
            LEFT JOIN subcategories sc ON p.id_subcategory = sc.id_subcategory
            LEFT JOIN categories c ON sc.id_category = c.id_category
            LEFT JOIN stock_items s ON p.id_product = s.id_product
            GROUP BY p.id_product, p.name_product, i.name_industry, c.name_category, p.composition, p.price, p.picture
        """
        cursor.execute(query)
        products = cursor.fetchall()
        return products
    except Error as e:
        print(f"2.Ошибка выполнения запроса: {e}")
        return []
    finally:
        close_connection(connection)