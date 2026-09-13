# RiskLens

RiskLens is an AI-powered transaction risk and AML assistant built with Python and Snowflake.

The project analyzes financial transactions, assigns risk scores, explains the reasons behind each score, and stores actionable alerts in Snowflake.

## Features

- Connects Python to Snowflake.
- Fetches transaction data from the `TRANSACTIONS` table.
- Calculates transaction risk scores.
- Classifies transactions as `LOW`, `MEDIUM`, or `HIGH` risk.
- Generates human-readable risk reasons.
- Stores medium- and high-risk alerts in the `ALERTS` table.
- Prevents duplicate alerts for the same transaction.
- Uses environment variables to protect credentials.

## Technology Stack

- Python
- Snowflake
- Snowflake Connector for Python
- Python Dotenv
- SQL
- Pandas
- Git and GitHub

## Project Architecture

```text
Snowflake TRANSACTIONS table
            |
            v
    Python Snowflake connector
            |
            v
       Risk analyzer
            |
            v
 Risk score and risk level
            |
            v
      Snowflake ALERTS table
```

## Project Structure

```text
RiskLens/
|
├── app/
│   ├── config.py
│   ├── main.py
│   ├── snowflake_connection.py
│   └── __init__.py
|
├── data/
├── docs/
├── sql/
├── tests/
|
├── .gitignore
├── README.md
└── requirements.txt
```

## Database Schema

### Transactions

The `TRANSACTIONS` table contains transaction data used by the risk engine.

| Column | Description |
|---|---|
| `TRANSACTION_ID` | Unique transaction identifier |
| `ACCOUNT_ID` | Customer account identifier |
| `TRANSACTION_TIMESTAMP` | Date and time of the transaction |
| `AMOUNT` | Transaction amount |
| `TRANSACTION_TYPE` | Purchase or transfer type |
| `MERCHANT_ID` | Merchant identifier |
| `LOCATION` | Transaction location |
| `DEVICE_ID` | Device used for the transaction |
| `STATUS` | Transaction status |

### Alerts

The `ALERTS` table stores transactions that require review.

| Column | Description |
|---|---|
| `ALERT_ID` | Generated alert identifier |
| `TRANSACTION_ID` | Related transaction |
| `RISK_SCORE` | Numeric risk score |
| `RISK_LEVEL` | Low, medium, or high |
| `TRIGGERED_RULES` | Reasons for the alert |
| `ALERT_STATUS` | Current alert status |
| `CREATED_AT` | Alert creation timestamp |

## Risk Scoring

The current prototype uses the following rules:

| Condition | Score |
|---|---:|
| Amount at least 100,000 | +50 |
| Amount at least 50,000 | +30 |
| Amount at least 10,000 | +15 |
| Flagged device | +20 |
| Monitored location | +10 |
| Transfer transaction | +10 |

Risk levels are assigned using the final score:

| Score | Risk level |
|---:|---|
| 0–39 | LOW |
| 40–69 | MEDIUM |
| 70 or higher | HIGH |

Low-risk transactions are analyzed but do not create alerts. Medium- and high-risk transactions are saved in the `ALERTS` table.

## Setup

### 1. Clone the repository

```bash
git clone [https://github.com/HeyNia/RiskLens.git](https://github.com/HeyNia/RiskLens.git)
cd RiskLens
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

If PowerShell blocks activation for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Snowflake credentials

Create a `.env` file in the project root:

```env
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=RISK_LENS_DB
SNOWFLAKE_SCHEMA=RISK_LENS_SCHEMA
SNOWFLAKE_ROLE=your_role
```

Never commit `.env` to GitHub. It is excluded through `.gitignore`.

### 5. Run the application

```powershell
python -m app.main
```

## Example Output

```text
Transaction: TXN002
Risk score: 60
Risk level: MEDIUM
Reasons:
- High transaction amount
- Transaction from a flagged device
- Transaction from a monitored location
Alert saved to Snowflake.
----------------------------------------
Transaction: TXN001
Risk score: 0
Risk level: LOW
Reasons: None
Low-risk transaction; no alert created.
----------------------------------------
Transaction: TXN003
Risk score: 90
Risk level: HIGH
Reasons:
- Very high transaction amount
- Transaction from a flagged device
- Transaction from a monitored location
- Funds transfer requires additional review
Alert saved to Snowflake.
```

## Current Status

Completed:

- Snowflake database and schema setup.
- Synthetic transaction data creation.
- Python-to-Snowflake connection.
- Transaction retrieval.
- Initial risk-scoring engine.
- Alert generation.
- Duplicate alert prevention.
- GitHub project setup.

Planned improvements:

- Load risk rules dynamically from the `RISK_RULES` table.
- Add automated tests.
- Add a command-line interface.
- Add a dashboard for reviewing alerts.
- Add Snowflake Cortex or another AI layer for alert explanations.
- Add customer and account history analysis.
- Add CI checks with GitHub Actions.

## Security

- Credentials are stored in `.env`.
- `.env` is excluded from Git tracking.
- Synthetic data is used for development.
- Do not commit passwords, tokens, private keys, or production customer data.

## Author

Created by [HeyNia](https://github.com/HeyNia).

## License

This project is currently available for educational and portfolio purposes.