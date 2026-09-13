from decimal import Decimal

from app.snowflake_connection import get_connection


def fetch_transactions():
    query = """
        SELECT
            TRANSACTION_ID,
            ACCOUNT_ID,
            TRANSACTION_TIMESTAMP,
            AMOUNT,
            TRANSACTION_TYPE,
            MERCHANT_ID,
            LOCATION,
            DEVICE_ID,
            STATUS
        FROM TRANSACTIONS
        ORDER BY TRANSACTION_TIMESTAMP DESC
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [column[0].lower() for column in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        cursor.close()
        connection.close()


def analyze_transaction(transaction):
    score = 0
    reasons = []

    amount = Decimal(transaction["amount"])

    if amount >= Decimal("100000"):
        score += 50
        reasons.append("Very high transaction amount")
    elif amount >= Decimal("50000"):
        score += 30
        reasons.append("High transaction amount")
    elif amount >= Decimal("10000"):
        score += 15
        reasons.append("Elevated transaction amount")

    if transaction["device_id"] in {"DEV999", "DEV777"}:
        score += 20
        reasons.append("Transaction from a flagged device")

    if transaction["location"] in {"Mumbai", "Delhi"}:
        score += 10
        reasons.append("Transaction from a monitored location")

    if transaction["transaction_type"].lower() == "transfer":
        score += 10
        reasons.append("Funds transfer requires additional review")

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "transaction_id": transaction["transaction_id"],
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons,
    }


def insert_alert(alert):
    alert_id = f"ALERT-{alert['transaction_id']}"

    query = """
        INSERT INTO ALERTS (
            ALERT_ID,
            TRANSACTION_ID,
            RISK_SCORE,
            RISK_LEVEL,
            TRIGGERED_RULES,
            ALERT_STATUS
        )
        SELECT %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1
            FROM ALERTS
            WHERE TRANSACTION_ID = %s
        )
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        triggered_rules = "; ".join(alert["reasons"])

        cursor.execute(
            query,
            (
                alert_id,
                alert["transaction_id"],
                alert["risk_score"],
                alert["risk_level"],
                triggered_rules,
                "OPEN",
                alert["transaction_id"],
            ),
        )

        connection.commit()

        return cursor.rowcount

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    transactions = fetch_transactions()

    print(f"Fetched {len(transactions)} transactions.\n")

    for transaction in transactions:
        result = analyze_transaction(transaction)

        print(f"Transaction: {result['transaction_id']}")
        print(f"Risk score: {result['risk_score']}")
        print(f"Risk level: {result['risk_level']}")

        if result["reasons"]:
            print("Reasons:")
            for reason in result["reasons"]:
                print(f"- {reason}")
        else:
            print("Reasons: None")

        if result["risk_level"] in {"MEDIUM", "HIGH"}:
            inserted = insert_alert(result)

            if inserted:
                print("Alert saved to Snowflake.")
            else:
                print("Alert already exists; skipped duplicate.")
        else:
            print("Low-risk transaction; no alert created.")

        print("-" * 40)