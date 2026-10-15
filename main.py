# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT employees.firstName, employees.lastName  
FROM employees 
JOIN offices
ON employees.officeCode = offices.officeCode
WHERE offices.city = 'Boston';
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT offices.officeCode, offices.city
FROM offices
LEFT JOIN employees
ON offices.officeCode = employees.officeCode
WHERE employees.employeeNumber IS NULL;
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT
employees.firstName,
employees.lastName,
offices.city,
offices.state
FROM employees
LEFT JOIN offices
ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName;
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT
customers.contactFirstName,
customers.contactLastName,
customers.phone,
customers.salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName;
""", conn)


# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT
customers.contactFirstName,
customers.contactLastName,
payments.amount,
payments.paymentDate
FROM customers
JOIN payments
ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
SELECT
employees.employeeNumber,
employees.firstName,
employees.lastName,
customer_summary.num_customers
FROM employees
JOIN (
    SELECT
    salesRepEmployeeNumber,
    COUNT(customerNumber) AS num_customers,
    AVG(creditLimit) AS avg_credit_limit
    FROM customers
    GROUP BY salesRepEmployeeNumber
    HAVING AVG(creditLimit) > 90000
) AS customer_summary
ON employees.employeeNumber = customer_summary.salesRepEmployeeNumber
ORDER BY customer_summary.num_customers DESC;
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT
products.productName,
COUNT(orderdetails.orderNumber) AS numorders,
SUM(orderdetails.quantityOrdered) AS totalunits
FROM products
JOIN orderdetails
ON products.productCode = orderdetails.productCode
GROUP BY products.productCode, products.productName
ORDER BY totalunits DESC;
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT
products.productName,
products.productCode,
COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
JOIN orderdetails
ON products.productCode = orderdetails.productCode
JOIN orders
ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode, products.productName
ORDER BY numpurchasers DESC;
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT
offices.officeCode,
offices.city,
COUNT(customers.customerNumber) AS n_customers
FROM offices
JOIN employees
ON offices.officeCode = employees.officeCode
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode, offices.city;
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
SELECT DISTINCT
employees.employeeNumber,
employees.firstName,
employees.lastName,
offices.city,
offices.officeCode
FROM employees
JOIN offices
ON employees.officeCode = offices.officeCode
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders
ON customers.customerNumber = orders.customerNumber
JOIN orderdetails
ON orders.orderNumber = orderdetails.orderNumber
WHERE orderdetails.productCode IN (
SELECT productCode
FROM orderdetails
JOIN orders
ON orderdetails.orderNumber = orders.orderNumber
GROUP BY productCode
HAVING COUNT(DISTINCT orders.customerNumber) < 20
);
""", conn)


conn.close()