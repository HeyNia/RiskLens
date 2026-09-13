USE DATABASE RISK_LENS_DB;

USE SCHEMA RISK_LENS_SCHEMA;

USE WAREHOUSE RISK_LENS_WH;

INSERT INTO RISK_RULES (
    RULE_ID,
    RULE_NAME,
    RULE_DESCRIPTION,
    RISK_WEIGHT,
    IS_ACTIVE
)
SELECT
    COLUMN1,
    COLUMN2,
    COLUMN3,
    COLUMN4,
    COLUMN5
FROM VALUES
    (
        'RULE001',
        'High Transaction Amount',
        'Transaction amount is significantly higher than the customer normal amount',
        25,
        TRUE
    ),
    (
        'RULE002',
        'Rapid Repeated Transactions',
        'Several transactions occurred within a short period',
        20,
        TRUE
    ),
    (
        'RULE003',
        'Unusual Location',
        'Transaction occurred in a location not commonly associated with the customer',
        15,
        TRUE
    ),
    (
        'RULE004',
        'New Device',
        'Transaction was completed using a previously unseen device',
        15,
        TRUE
    ),
    (
        'RULE005',
        'Unusual Transaction Time',
        'Transaction occurred during an unusual time window',
        10,
        TRUE
    ),
    (
        'RULE006',
        'Multiple Failed Attempts',
        'Several failed transaction attempts were detected',
        15,
        TRUE
    )
WHERE NOT EXISTS (
    SELECT 1
    FROM RISK_RULES
);

SELECT *
FROM RISK_RULES
ORDER BY RULE_ID;