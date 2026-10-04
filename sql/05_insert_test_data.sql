USE DATABASE RISK_LENS_DB;
USE SCHEMA RISK_LENS_SCHEMA;

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
SELECT *
FROM VALUES
    ('TXN004', 'ACC001', '2026-09-10 09:30:00'::TIMESTAMP_NTZ, 12000.00, 'Purchase', 'MER001', 'Lucknow', 'DEV001', 'Success'),
    ('TXN005', 'ACC002', '2026-09-10 11:45:00'::TIMESTAMP_NTZ, 5200.00, 'Purchase', 'MER001', 'Lucknow', 'DEV002', 'Success'),
    ('TXN006', 'ACC003', '2026-09-10 13:20:00'::TIMESTAMP_NTZ, 68000.00, 'Purchase', 'MER003', 'Mumbai', 'DEV003', 'Success'),
    ('TXN007', 'ACC001', '2026-09-10 18:10:00'::TIMESTAMP_NTZ, 95000.00, 'Transfer', 'MER002', 'Delhi', 'DEV777', 'Success'),
    ('TXN008', 'ACC002', '2026-09-11 01:20:00'::TIMESTAMP_NTZ, 175000.00, 'Transfer', 'MER002', 'Delhi', 'DEV999', 'Success'),
    ('TXN009', 'ACC003', '2026-09-11 10:15:00'::TIMESTAMP_NTZ, 8500.00, 'Purchase', 'MER001', 'Lucknow', 'DEV004', 'Success'),
    ('TXN010', 'ACC002', '2026-09-11 15:35:00'::TIMESTAMP_NTZ, 42000.00, 'Purchase', 'MER003', 'Mumbai', 'DEV002', 'Success'),
    ('TXN011', 'ACC001', '2026-09-11 23:50:00'::TIMESTAMP_NTZ, 130000.00, 'Transfer', 'MER002', 'Delhi', 'DEV888', 'Success')
    AS new_transactions (
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
WHERE NOT EXISTS (
    SELECT 1
    FROM TRANSACTIONS existing_transactions
    WHERE existing_transactions.TRANSACTION_ID =
          new_transactions.TRANSACTION_ID
);