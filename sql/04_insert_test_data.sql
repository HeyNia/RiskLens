USE DATABASE RISK_LENS_DB;

USE SCHEMA RISK_LENS_SCHEMA;

USE WAREHOUSE RISK_LENS_WH;

INSERT INTO ACCOUNTS (
    ACCOUNT_ID,
    CUSTOMER_ID,
    ACCOUNT_TYPE,
    CURRENT_BALANCE,
    ACCOUNT_STATUS,
    OPEN_DATE
)
SELECT
    COLUMN1,
    COLUMN2,
    COLUMN3,
    COLUMN4,
    COLUMN5,
    COLUMN6
FROM VALUES
    (
        'ACC001',
        'CUST001',
        'Savings',
        85000.00,
        'Active',
        '2024-03-15'
    ),
    (
        'ACC002',
        'CUST002',
        'Current',
        125000.00,
        'Active',
        '2023-08-21'
    ),
    (
        'ACC003',
        'CUST003',
        'Business',
        450000.00,
        'Active',
        '2022-11-10'
    )
WHERE NOT EXISTS (
    SELECT 1
    FROM ACCOUNTS
);

INSERT INTO MERCHANTS (
    MERCHANT_ID,
    MERCHANT_NAME,
    MERCHANT_CATEGORY,
    MERCHANT_CITY,
    MERCHANT_RISK_LEVEL
)
SELECT
    COLUMN1,
    COLUMN2,
    COLUMN3,
    COLUMN4,
    COLUMN5
FROM VALUES
    (
        'MER001',
        'City Electronics',
        'Electronics',
        'Lucknow',
        'Medium'
    ),
    (
        'MER002',
        'Travel World',
        'Travel',
        'Delhi',
        'Medium'
    ),
    (
        'MER003',
        'Luxury Imports',
        'Luxury Goods',
        'Mumbai',
        'High'
    )
WHERE NOT EXISTS (
    SELECT 1
    FROM MERCHANTS );

INSERT INTO TRANSACTIONS (
    TRANSACTION_ID,
    ACCOUNT_ID,
    TRANSACTION_TIMESTAMP,
    AMOUNT,
    TRANSACTION_TYPE,
    MERCHANT_ID,
    LOCATION,
    DEVICE_ID,
    STATUS
)
SELECT
    COLUMN1,
    COLUMN2,
    COLUMN3,
    COLUMN4,
    COLUMN5,
    COLUMN6,
    COLUMN7,
    COLUMN8,
    COLUMN9
FROM VALUES
    (
        'TXN001',
        'ACC001',
        '2026-09-10 10:00:00',
        2500.00,
        'Purchase',
        'MER001',
        'Lucknow',
        'DEV001',
        'Success'
    ),
    (
        'TXN002',
        'ACC002',
        '2026-09-10 10:05:00',
        75000.00,
        'Purchase',
        'MER003',
        'Mumbai',
        'DEV999',
        'Success'
    ),
    (
        'TXN003',
        'ACC003',
        '2026-09-10 02:15:00',
        150000.00,
        'Transfer',
        'MER002',
        'Delhi',
        'DEV777',
        'Success'
    )
WHERE NOT EXISTS (
    SELECT 1
    FROM TRANSACTIONS);