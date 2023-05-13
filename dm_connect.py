import pymysql
import csv
# Database credentials from env.php
host = '68.66.194.91'
dbname = 'drew_mage10dec'
username = 'drew_mage433'
password = '34Vp))90Sh'

# Establish a connection to the database
conn = pymysql.connect(
    host=host,
    user=username,
    password=password,
    database=dbname
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

def find_entities(cursor=cursor):
    # List of attribute codes
    attribute_codes = ["length", "voltage", "price"]

    # Base SQL query
    sql = """
    SELECT e.entity_id as product_id, e.sku
    """

    # Add attribute codes to the SELECT clause
    for code in attribute_codes:
        sql += f", v_{code}.value as {code}"

    # Add FROM clause
    sql += """
    FROM
        mg6t_catalog_product_entity as e
    """

    # Add attribute codes to the JOIN clause
    for code in attribute_codes:
        sql += f"""
        LEFT JOIN
            mg6t_catalog_product_entity_varchar as v_{code}
            ON e.entity_id = v_{code}.entity_id
            AND v_{code}.attribute_id = (SELECT attribute_id FROM mg6t_eav_attribute WHERE attribute_code = '{code}' AND entity_type_id = 4)
        """
    # Example usage:
    # get_all_products(cursor)


    # Execute the SQL query
    cursor.execute(sql)

    # Fetch the results
    results = cursor.fetchall()

    # Process the results
    for row in results:
        print(row)


    # Close the cursor and connection
    cursor.close()
    conn.close()

def get_all_products(cursor):
    # Get attribute_id for 'name'
    sql = """
    SELECT attribute_id 
    FROM mg6t_eav_attribute 
    WHERE attribute_code = 'name' 
    AND entity_type_id = (SELECT entity_type_id 
                          FROM mg6t_eav_entity_type 
                          WHERE entity_type_code = 'catalog_product')
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    attribute_id = result[0]  # Adjusted to work with tuple

    # Get product names
    sql = f"SELECT value FROM mg6t_catalog_product_entity_varchar WHERE attribute_id = {attribute_id}"
    cursor.execute(sql)
    product_names = cursor.fetchall()

    with open('product_names.csv', 'w', newline='', encoding='utf-8') as f:  # Added encoding='utf-8'
        writer = csv.writer(f)
        writer.writerow(['Product Name'])
        for row in product_names:
            writer.writerow([row[0]])  # Adjusted to work with tuple


get_all_products(cursor)