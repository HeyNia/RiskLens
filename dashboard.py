import pandas as pd
import streamlit as st

from app.snowflake_connection import get_connection


st.set_page_config(
    page_title="RiskLens | AML Risk Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF6FF 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1250px;
        }

        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #DCE6F2;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        }

        [data-testid="stMetricLabel"] {
            color: #475569;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: #0F172A;
            font-weight: 700;
        }

        .risklens-card {
            background: #FFFFFF;
            color: #1E293B;
            border: 1px solid #DCE6F2;
            border-left: 5px solid #2563EB;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
            line-height: 1.6;
        }

        .risklens-card strong {
            color: #1D4ED8;
            font-size: 1.05rem;
        }

        .high-risk {
            color: #B91C1C;
            font-size: 1.25rem;
            font-weight: 700;
        }

        .medium-risk {
            color: #B45309;
            font-size: 1.25rem;
            font-weight: 700;
        }

        .prototype-note {
            color: #475569;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .hero-banner {
            background: linear-gradient(90deg, #0F3D78 0%, #2563EB 100%);
            color: white;
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 22px;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.20);
        }

        .hero-banner h1 {
            color: white;
            margin: 0;
            font-size: 2rem;
        }

        .hero-banner p {
            color: #DBEAFE;
            margin: 8px 0 0 0;
            font-size: 1rem;
        }

        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #DCE6F2;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def run_query(query: str) -> pd.DataFrame:
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        columns = [column[0].lower() for column in cursor.description]
        rows = cursor.fetchall()

        return pd.DataFrame(rows, columns=columns)

    finally:
        cursor.close()
        connection.close()


@st.cache_data(ttl=60)
def get_alert_summary() -> pd.DataFrame:
    query = """
        SELECT
            RISK_LEVEL,
            COUNT(*) AS ALERT_COUNT,
            ROUND(AVG(RISK_SCORE), 2) AS AVERAGE_RISK_SCORE
        FROM ALERTS
        GROUP BY RISK_LEVEL
        ORDER BY
            CASE RISK_LEVEL
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                WHEN 'LOW' THEN 3
            END
    """

    return run_query(query)


@st.cache_data(ttl=60)
def get_open_alerts() -> pd.DataFrame:
    query = """
        SELECT
            a.ALERT_ID,
            a.TRANSACTION_ID,
            a.RISK_SCORE,
            a.RISK_LEVEL,
            a.TRIGGERED_RULES,
            a.ALERT_STATUS,
            a.CREATED_AT,
            t.AMOUNT,
            t.LOCATION,
            t.DEVICE_ID,
            t.TRANSACTION_TYPE,
            t.TRANSACTION_TIMESTAMP
        FROM ALERTS a
        JOIN TRANSACTIONS t
            ON a.TRANSACTION_ID = t.TRANSACTION_ID
        WHERE a.ALERT_STATUS = 'OPEN'
        ORDER BY a.RISK_SCORE DESC
    """

    return run_query(query)


def risk_label(risk_level: str) -> str:
    if risk_level == "HIGH":
        return "🔴 HIGH RISK"

    if risk_level == "MEDIUM":
        return "🟡 MEDIUM RISK"

    return "🟢 LOW RISK"


st.sidebar.title("🔎 RiskLens")
st.sidebar.caption("AML Risk Intelligence Prototype")
st.sidebar.divider()

st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Choose a view",
    ["Risk Overview", "Alert Investigation", "About Prototype"],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.markdown(
    """
    <div class="prototype-note">
        <strong>Status:</strong> Under active development<br><br>
        RiskLens currently uses synthetic data and rule-based risk scoring.
        It is not a production AML or compliance system.
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    summary = get_alert_summary()
    alerts = get_open_alerts()

    high_count = len(alerts[alerts["risk_level"] == "HIGH"])
    medium_count = len(alerts[alerts["risk_level"] == "MEDIUM"])
    open_count = len(alerts)

    if page == "Risk Overview":
        st.title("RiskLens Intelligence Dashboard")
        st.caption(
            "Explainable transaction-risk detection and AML alert prioritization"
        )

        st.warning(
            "Prototype under active development. The application uses synthetic "
            "data and rule-based risk scoring for demonstration purposes."
        )

        metric_1, metric_2, metric_3, metric_4 = st.columns(4)

        metric_1.metric("Open Alerts", open_count)
        metric_2.metric("High-Risk Alerts", high_count)
        metric_3.metric("Medium-Risk Alerts", medium_count)
        metric_4.metric(
            "Highest Risk Score",
            int(alerts["risk_score"].max()) if not alerts.empty else 0,
        )

        st.divider()

        left, right = st.columns([1, 2])

        with left:
            st.subheader("Risk Distribution")
            st.dataframe(
                summary,
                width="stretch",
                hide_index=True,
                column_config={
                    "risk_level": st.column_config.TextColumn("Risk Level"),
                    "alert_count": st.column_config.NumberColumn("Alerts"),
                    "average_risk_score": st.column_config.NumberColumn(
                        "Average Score",
                        format="%.2f",
                    ),
                },
            )

        with right:
            st.subheader("Why RiskLens Matters")
            st.markdown(
                """
                <div class="risklens-card">
                    <strong>1. Detect</strong><br>
                    Identify suspicious transactions using explainable rules.
                    <br><br>
                    <strong>2. Prioritize</strong><br>
                    Surface the highest-risk alerts first for analyst review.
                    <br><br>
                    <strong>3. Investigate</strong><br>
                    Show the transaction evidence and all triggered risk signals.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("Prioritized Open Alerts")

        display_alerts = alerts[
            [
                "transaction_id",
                "risk_level",
                "risk_score",
                "amount",
                "location",
                "device_id",
                "transaction_type",
                "alert_status",
            ]
        ]

        st.dataframe(
            display_alerts,
            width="stretch",
            hide_index=True,
            column_config={
                "transaction_id": st.column_config.TextColumn("Transaction ID"),
                "risk_level": st.column_config.TextColumn("Risk Level"),
                "risk_score": st.column_config.NumberColumn(
                    "Risk Score",
                    format="%.0f",
                ),
                "amount": st.column_config.NumberColumn(
                    "Amount",
                    format="₹ %.2f",
                ),
                "location": st.column_config.TextColumn("Location"),
                "device_id": st.column_config.TextColumn("Device"),
                "transaction_type": st.column_config.TextColumn("Type"),
                "alert_status": st.column_config.TextColumn("Status"),
            },
        )

    elif page == "Alert Investigation":
        st.title("Alert Investigation")
        st.caption(
            "Select an open alert to view the evidence behind its risk score."
        )

        if alerts.empty:
            st.info("No open alerts were found.")
        else:
            selected_transaction = st.selectbox(
                "Choose a transaction to investigate",
                alerts["transaction_id"].tolist(),
            )

            selected_alert = alerts[
                alerts["transaction_id"] == selected_transaction
            ].iloc[0]

            if selected_alert["risk_level"] == "HIGH":
                st.markdown(
                    '<p class="high-risk">🔴 HIGH-RISK TRANSACTION</p>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<p class="medium-risk">🟡 MEDIUM-RISK TRANSACTION</p>',
                    unsafe_allow_html=True,
                )

            metric_1, metric_2, metric_3 = st.columns(3)
            metric_1.metric("Risk Score", int(selected_alert["risk_score"]))
            metric_2.metric("Risk Level", risk_label(selected_alert["risk_level"]))
            metric_3.metric("Alert Status", selected_alert["alert_status"])

            st.divider()

            left, right = st.columns(2)

            with left:
                st.subheader("Transaction Details")
                st.write("**Transaction ID:**", selected_alert["transaction_id"])
                st.write("**Amount:**", f"₹ {selected_alert['amount']}")
                st.write(
                    "**Transaction Type:**",
                    selected_alert["transaction_type"],
                )
                st.write(
                    "**Transaction Time:**",
                    selected_alert["transaction_timestamp"],
                )

            with right:
                st.subheader("Risk Context")
                st.write("**Location:**", selected_alert["location"])
                st.write("**Device ID:**", selected_alert["device_id"])
                st.write("**Alert ID:**", selected_alert["alert_id"])
                st.write("**Created At:**", selected_alert["created_at"])

            st.subheader("Triggered Risk Signals")
            st.error(selected_alert["triggered_rules"])

            st.subheader("Analyst Summary")
            st.info(
                f"{selected_alert['transaction_id']} is classified as "
                f"{selected_alert['risk_level']} risk with a score of "
                f"{selected_alert['risk_score']}. The alert should be reviewed "
                "using the transaction evidence and triggered signals above."
            )

    else:
        st.title("About RiskLens")

        st.markdown(
            """
            ## Risk, Fraud and Regulatory Intelligence Copilot

            RiskLens is an under-development prototype that helps risk and
            compliance analysts identify, prioritize, and investigate
            suspicious transactions.

            ### Current Working Capabilities

            - Retrieves transaction and alert data from Snowflake.
            - Calculates explainable rule-based risk scores.
            - Categorizes transactions as low, medium, or high risk.
            - Stores actionable medium- and high-risk alerts.
            - Prevents duplicate alert creation.
            - Provides a dashboard for alert prioritization and investigation.

            ### Target Vision

            The target version will include configurable Snowflake risk rules,
            account-history analysis, CoCo CLI investigation workflows,
            AI-assisted alert summaries, and audit-ready case management.

            ### Prototype Disclaimer

            This prototype uses synthetic data only. It is not a production
            fraud-detection, AML, regulatory-reporting, or compliance system.
            """
        )

except Exception as error:
    st.error("RiskLens could not load Snowflake data.")
    st.exception(error)