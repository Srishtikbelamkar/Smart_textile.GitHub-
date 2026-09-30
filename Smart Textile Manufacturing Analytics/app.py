import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime
import hashlib
import sqlite3
import os




# ============================================================
# PROFILE & SETTINGS
# ============================================================

def profile_settings():

    st.markdown(
        '<div class="page-title">👤 Profile & Settings</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Logged in as: **{st.session_state.username}**"
    )

    st.divider()

    st.subheader("Change Password")

    current_password = st.text_input(
        "Current Password",
        type="password"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password"
    )

    if st.button(
        "Change Password",
        type="primary"
    ):

        if not current_password:
            st.error("Please enter your current password.")

        elif not new_password:
            st.error("Please enter your new password.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:

            try:

                connection = connect_database()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT Password
                    FROM Users
                    WHERE Username = %s
                    """,
                    (st.session_state.username,)
                )

                result = cursor.fetchone()

                if result is None:

                    st.error("User not found.")

                elif result[0] != hash_password(current_password):

                    st.error("Current password is incorrect.")

                else:

                    cursor.execute(
                        """
                        UPDATE Users
                        SET Password = %s
                        WHERE Username = %s
                        """,
                        (
                            hash_password(new_password),
                            st.session_state.username
                        )
                    )

                    connection.commit()

                    st.success(
                        "Password changed successfully!"
                    )

                cursor.close()
                connection.close()

            except Exception as e:

                st.error(
                    f"MySQL Error: {e}"
                )
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Textile Manufacturing Analytics",
    page_icon="🧵",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.login-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #17365d;
    margin-bottom: 5px;
}

.login-subtitle {
    text-align: center;
    font-size: 18px;
    color: #666666;
    margin-bottom: 30px;
}

.page-title {
    font-size: 32px;
    font-weight: 800;
    color: #17365d;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #17365d;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 3px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# PASSWORD HASH
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================
# MYSQL CONNECTION
# ============================================================

def connect_server():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345"
    )


def connect_database():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="smart_textile_db"
    )


# ============================================================
# DATABASE FILE
# ============================================================

DB_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "smart_textile.db"
)


# ============================================================
# CREATE DATABASE AND APPLICATION TABLES
# ============================================================

def initialize_database():

    try:

        connection = connect_server()
        cursor = connection.cursor()

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS smart_textile_db"
        )

        cursor.close()
        connection.close()

        connection = connect_database()
        cursor = connection.cursor()

        # USERS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (

            User_ID INT AUTO_INCREMENT PRIMARY KEY,

            Username VARCHAR(100) UNIQUE NOT NULL,

            Email VARCHAR(150) UNIQUE NOT NULL,

            Password VARCHAR(255) NOT NULL,

            Created_At DATETIME
        )
        """)

        # INCIDENT TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Incidents (

            Incident_ID INT AUTO_INCREMENT PRIMARY KEY,

            Incident_Date DATE,

            Machine_ID VARCHAR(50),

            Operator_ID VARCHAR(50),

            Incident_Type VARCHAR(100),

            Severity VARCHAR(50),

            Description TEXT,

            Reported_By VARCHAR(100),

            Created_At DATETIME
        )
        """)

        connection.commit()

        cursor.close()
        connection.close()

        return True, ""

    except Exception as e:

        return False, str(e)


# ============================================================
# LOAD PRODUCTION DATA
# ============================================================

def load_data():

    try:

        connection = connect_database()

        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM Production_Data
        """)

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        df = pd.DataFrame(records)

        if not df.empty:

            df["Production_Date"] = pd.to_datetime(
                df["Production_Date"],
                errors="coerce"
            )

            numeric_columns = [
                "Planned_Qty",
                "Produced_Qty",
                "Good_Qty",
                "Rejected_Qty",
                "Production_Hours",
                "Downtime_Hours",
                "Raw_Material_Used_Kg",
                "Wastage_Kg",
                "Production_Efficiency",
                "Defect_Rate",
                "Machine_Efficiency",
                "Quality_Score"
            ]

            for column in numeric_columns:

                if column in df.columns:

                    df[column] = pd.to_numeric(
                        df[column],
                        errors="coerce"
                    )

        return df, ""

    except Exception as e:

        return pd.DataFrame(), str(e)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.markdown(
        '<div class="login-title">🧵 SMART TEXTILE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">MANUFACTURING ANALYTICS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Smart Textile Manufacturing Analytics System'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "🔐 Login",
                "📝 Sign Up",
                "🔑 Forgot Password"
            ]
        )

        # ====================================================
        # LOGIN
        # ====================================================

        with tab1:

            st.subheader("Welcome Back")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "Login",
                use_container_width=True,
                type="primary"
            ):

                if username.strip() == "":
                    st.error("Please enter username.")

                elif password.strip() == "":
                    st.error("Please enter password.")

                else:

                    # DEMO ADMIN LOGIN
                    if (
                        username == "admin"
                        and password == "admin123"
                    ):

                        st.session_state.logged_in = True
                        st.session_state.username = "admin"
                        st.session_state.page = "Dashboard"

                        st.rerun()

                    else:

                        try:

                            connection = connect_database()
                            cursor = connection.cursor()

                            cursor.execute(
                                """
                                SELECT Password
                                FROM Users
                                WHERE Username = %s
                                """,
                                (username,)
                            )

                            result = cursor.fetchone()

                            cursor.close()
                            connection.close()

                            if result:

                                stored_password = result[0]

                                if stored_password == hash_password(password):

                                    st.session_state.logged_in = True
                                    st.session_state.username = username
                                    st.session_state.page = "Dashboard"

                                    st.rerun()

                                else:

                                    st.error(
                                        "Incorrect password."
                                    )

                            else:

                                st.error(
                                    "User not found. Please Sign Up."
                                )

                        except Exception as e:

                            st.error(
                                f"MySQL Error: {e}"
                            )

        # ====================================================
        # SIGN UP
        # ====================================================

        with tab2:

            st.subheader("Create New Account")

            new_username = st.text_input(
                "Username",
                key="signup_username"
            )

            new_email = st.text_input(
                "Email",
                key="signup_email"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if (
                    new_username.strip() == ""
                    or new_email.strip() == ""
                    or new_password.strip() == ""
                ):

                    st.error(
                        "Please fill all fields."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    try:

                        connection = connect_database()
                        cursor = connection.cursor()

                        cursor.execute(
                            """
                            INSERT INTO Users
                            (
                                Username,
                                Email,
                                Password,
                                Created_At
                            )
                            VALUES (%s,%s,%s,%s)
                            """,
                            (
                                new_username,
                                new_email,
                                hash_password(new_password),
                                datetime.now()
                            )
                        )

                        connection.commit()

                        cursor.close()
                        connection.close()

                        st.success(
                            "Account created successfully!"
                        )

                    except mysql.connector.IntegrityError:

                        st.error(
                            "Username or email already exists."
                        )

                    except Exception as e:

                        st.error(
                            f"MySQL Error: {e}"
                        )

        # ====================================================
        # FORGOT PASSWORD
        # ====================================================

        with tab3:

            st.subheader("Reset Password")

            reset_email = st.text_input(
                "Registered Email",
                key="reset_email"
            )

            reset_password = st.text_input(
                "New Password",
                type="password",
                key="reset_password"
            )

            confirm_reset = st.text_input(
                "Confirm New Password",
                type="password",
                key="confirm_reset"
            )

            if st.button(
                "Reset Password",
                use_container_width=True
            ):

                if reset_email.strip() == "":
                    st.error("Please enter your email.")

                elif reset_password.strip() == "":
                    st.error("Please enter a new password.")

                elif reset_password != confirm_reset:
                    st.error("Passwords do not match.")

                else:

                    try:

                        connection = connect_database()
                        cursor = connection.cursor()

                        cursor.execute(
                            """
                            UPDATE Users
                            SET Password = %s
                            WHERE Email = %s
                            """,
                            (
                                hash_password(reset_password),
                                reset_email
                            )
                        )

                        connection.commit()

                        if cursor.rowcount > 0:

                            st.success(
                                "Password reset successfully!"
                            )

                        else:

                            st.error(
                                "Email not found."
                            )

                        cursor.close()
                        connection.close()

                    except Exception as e:

                        st.error(
                            f"MySQL Error: {e}"
                        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.info(
        "Demo Login → Username: admin | Password: admin123"
    )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    st.sidebar.title("🧵 Smart Textile")

    st.sidebar.write(
        f"Welcome, **{st.session_state.username}**"
    )

    st.sidebar.divider()

    pages = [
        "🏠 Dashboard",
        "📡 Live Production",
        "📊 Production Analytics",
        "🔮 Prediction & Forecasting",
        "⚙️ Production Optimization",
        "⚠️ Incident Reporting",
        "🔔 Alerts & Notifications",
        "📄 History & Reports",
        "👤 Profile & Settings"
    ]

    selected = st.sidebar.radio(
        "Navigation",
        pages
    )

    st.session_state.page = selected

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "Dashboard"

        st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard(df):

    st.markdown(
        '<div class="page-title">🏠 Smart Textile Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Overview of textile manufacturing production."
    )

    if df.empty:

        st.warning(
            "No production data found in MySQL."
        )

        return

    total_planned = df["Planned_Qty"].sum()
    total_produced = df["Produced_Qty"].sum()
    total_good = df["Good_Qty"].sum()
    total_rejected = df["Rejected_Qty"].sum()

    avg_efficiency = df["Production_Efficiency"].mean()
    avg_quality = df["Quality_Score"].mean()

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "Planned Qty",
        f"{total_planned:,.0f}"
    )

    c2.metric(
        "Produced Qty",
        f"{total_produced:,.0f}"
    )

    c3.metric(
        "Good Qty",
        f"{total_good:,.0f}"
    )

    c4.metric(
        "Rejected Qty",
        f"{total_rejected:,.0f}"
    )

    c5.metric(
        "Avg Efficiency",
        f"{avg_efficiency:.2f}%"
    )

    c6.metric(
        "Quality Score",
        f"{avg_quality:.2f}"
    )

    st.divider()

    daily = (
        df.groupby("Production_Date", as_index=False)
        ["Produced_Qty"]
        .sum()
    )

    fig = px.line(
        daily,
        x="Production_Date",
        y="Produced_Qty",
        markers=True,
        title="📈 Production Trend"
    )

    fig.update_layout(
        xaxis_title="Production Date",
        yaxis_title="Produced Quantity",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# LIVE PRODUCTION
# ============================================================

def live_production(df):

    st.markdown(
        '<div class="page-title">📡 Live Production</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.warning("No production data available.")

        return

    latest_date = df["Production_Date"].max()

    latest = df[
        df["Production_Date"] == latest_date
    ]

    st.info(
        f"Latest production date: {latest_date.strftime('%d-%m-%Y')}"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Produced Qty",
        f"{latest['Produced_Qty'].sum():,.0f}"
    )

    c2.metric(
        "Good Qty",
        f"{latest['Good_Qty'].sum():,.0f}"
    )

    c3.metric(
        "Rejected Qty",
        f"{latest['Rejected_Qty'].sum():,.0f}"
    )

    c4.metric(
        "Downtime Hours",
        f"{latest['Downtime_Hours'].sum():.2f}"
    )

    st.subheader("Machine Production")

    machine = (
        latest.groupby("Machine_ID", as_index=False)
        .agg(
            Produced_Qty=("Produced_Qty", "sum"),
            Good_Qty=("Good_Qty", "sum"),
            Rejected_Qty=("Rejected_Qty", "sum"),
            Machine_Efficiency=("Machine_Efficiency", "mean")
        )
    )

    st.dataframe(
        machine,
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        machine,
        x="Machine_ID",
        y="Produced_Qty",
        title="Live Machine Production"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PRODUCTION ANALYTICS
# ============================================================

def production_analytics(df):

    st.markdown(
        '<div class="page-title">📊 Production Analytics</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.warning("No data available.")

        return

    col1, col2 = st.columns(2)

    with col1:

        machine = (
            df.groupby("Machine_ID", as_index=False)
            ["Produced_Qty"]
            .sum()
        )

        fig1 = px.bar(
            machine,
            x="Machine_ID",
            y="Produced_Qty",
            title="Machine-wise Production"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:

        shift = (
            df.groupby("Shift", as_index=False)
            ["Produced_Qty"]
            .sum()
        )

        fig2 = px.bar(
            shift,
            x="Shift",
            y="Produced_Qty",
            title="Shift-wise Production"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    with col3:

        defects = (
            df.groupby("Defect_Type", as_index=False)
            ["Rejected_Qty"]
            .sum()
            .sort_values(
                "Rejected_Qty",
                ascending=False
            )
        )

        fig3 = px.pie(
            defects,
            names="Defect_Type",
            values="Rejected_Qty",
            title="Defect Analysis"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col4:

        quality = (
            df.groupby("Quality_Level", as_index=False)
            .size()
        )

        fig4 = px.pie(
            quality,
            names="Quality_Level",
            values="size",
            title="Quality Distribution"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.subheader("Production Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PREDICTION & FORECASTING
# ============================================================

def prediction_forecasting(df):

    st.markdown(
        '<div class="page-title">🔮 Prediction & Forecasting</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.warning("No data available.")

        return

    daily = (
        df.groupby("Production_Date", as_index=False)
        ["Produced_Qty"]
        .sum()
        .sort_values("Production_Date")
    )

    if len(daily) < 10:

        st.warning(
            "Not enough data for forecasting."
        )

        return

    daily["Day_Number"] = range(
        1,
        len(daily) + 1
    )

    X = daily[
        ["Day_Number"]
    ]

    y = daily[
        "Produced_Qty"
    ]

    model = LinearRegression()

    model.fit(X, y)

    future_days = st.slider(
        "Forecast Days",
        7,
        90,
        30
    )

    last_day = daily["Day_Number"].max()

    future = pd.DataFrame(
        {
            "Day_Number": range(
                last_day + 1,
                last_day + future_days + 1
            )
        }
    )

    future["Predicted_Production"] = model.predict(
        future[
            ["Day_Number"]
        ]
    )

    st.subheader(
        "Production Forecast"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily["Production_Date"],
            y=daily["Produced_Qty"],
            mode="lines",
            name="Actual Production"
        )
    )

    future_dates = pd.date_range(
        start=daily["Production_Date"].max()
        + pd.Timedelta(days=1),
        periods=future_days
    )

    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=future["Predicted_Production"],
            mode="lines",
            name="Predicted Production"
        )
    )

    fig.update_layout(
        title="Actual vs Predicted Production",
        xaxis_title="Date",
        yaxis_title="Produced Quantity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Predicted Production"
    )

    result = future.copy()

    result["Date"] = future_dates

    st.dataframe(
        result[
            [
                "Date",
                "Predicted_Production"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PRODUCTION OPTIMIZATION
# ============================================================

def production_optimization(df):

    st.markdown(
        '<div class="page-title">⚙️ Production Optimization</div>',
        unsafe_allow_html=True
    )

    if df.empty:

        st.warning("No data available.")

        return

    machine = (
        df.groupby("Machine_ID", as_index=False)
        .agg(
            Produced_Qty=("Produced_Qty", "sum"),
            Downtime_Hours=("Downtime_Hours", "sum"),
            Machine_Efficiency=("Machine_Efficiency", "mean"),
            Defect_Rate=("Defect_Rate", "mean"),
            Quality_Score=("Quality_Score", "mean")
        )
    )

    st.subheader(
        "Machine Performance"
    )

    st.dataframe(
        machine,
        use_container_width=True,
        hide_index=True
    )

    best_machine = machine.sort_values(
        [
            "Machine_Efficiency",
            "Quality_Score"
        ],
        ascending=False
    ).iloc[0]

    st.success(
        f"Machine with highest combined efficiency/quality values: "
        f"{best_machine['Machine_ID']}"
    )

    high_downtime = machine[
        machine["Downtime_Hours"]
        >
        machine["Downtime_Hours"].mean()
    ]

    st.subheader(
        "Machines Requiring Attention"
    )

    st.dataframe(
        high_downtime,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# INCIDENT REPORTING
# ============================================================



def incident_reporting():

    st.markdown(
        '<div class="page-title">⚠️ Incident Reporting</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Report machine, production or quality incidents."
    )

    col1, col2 = st.columns(2)

    with col1:

        incident_date = st.date_input(
            "Incident Date"
        )

        machine_id = st.text_input(
            "Machine ID"
        )

        operator_id = st.text_input(
            "Operator ID"
        )

        incident_type = st.selectbox(
            "Incident Type",
            [
                "Machine Failure",
                "Quality Issue",
                "Production Delay",
                "Raw Material Issue",
                "Safety Incident",
                "Other"
            ]
        )

    with col2:

        severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        description = st.text_area(
            "Incident Description"
        )

    if st.button(
        "Submit Incident",
        type="primary"
    ):

        if description.strip() == "":

            st.error(
                "Please enter incident description."
            )

        else:

            try:

                connection = connect_database()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO Incidents
                    (
                        Incident_Date,
                        Machine_ID,
                        Operator_ID,
                        Incident_Type,
                        Severity,
                        Description,
                        Reported_By,
                        Created_At
                    )
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        incident_date,
                        machine_id,
                        operator_id,
                        incident_type,
                        severity,
                        description,
                        st.session_state.username,
                        datetime.now()
                    )
                )

                connection.commit()

                cursor.close()
                connection.close()

                st.success(
                    "Incident reported successfully!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

                # ============================================================
# SMART TEXTILE SQLITE DATABASE
# ============================================================

DB_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "smart_textile.db"
)


def create_incident_database():

    connection = sqlite3.connect(DB_FILE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            incident_date TEXT,
            machine TEXT,
            operator_id TEXT,
            incident_type TEXT,
            severity TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()



    


# ============================================================
# INCIDENT REPORTING
# ============================================================

def incident_reporting():

    create_incident_database()

    st.title("⚠️ Incident Reporting")

    st.write(
        "Report machine, production or quality incidents."
    )

    col1, col2 = st.columns(2)

    with col1:

        incident_date = st.date_input(
            "Incident Date"
        )

        machine = st.text_input(
            "Machine ID"
        )

        operator_id = st.text_input(
            "Operator ID"
        )

        incident_type = st.selectbox(
            "Incident Type",
            [
                "Machine Failure",
                "Quality Issue",
                "Production Delay",
                "Material Issue",
                "Safety Issue",
                "Other"
            ]
        )

    with col2:

        severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        description = st.text_area(
            "Incident Description"
        )

    if st.button(
        "Submit Incident",
        type="primary"
    ):

        if not machine:
            st.error("Please enter Machine ID.")

        elif not operator_id:
            st.error("Please enter Operator ID.")

        elif not description:
            st.error("Please enter Incident Description.")

        else:

            connection = sqlite3.connect(DB_FILE)

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO incidents
                (
                    user,
                    incident_date,
                    machine,
                    operator_id,
                    incident_type,
                    severity,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.get(
                        "username",
                        "admin"
                    ),
                    str(incident_date),
                    machine,
                    operator_id,
                    incident_type,
                    severity,
                    description
                )
            )

            connection.commit()
            connection.close()

            st.success(
                "✅ Incident reported successfully!"
            )


# ============================================================
# VIEW STORED INCIDENTS
# ============================================================

def view_incident_data():

    create_incident_database()

    st.title("📋 Stored Incident Data")

    connection = sqlite3.connect(DB_FILE)

    df_incidents = pd.read_sql_query(
        "SELECT * FROM incidents ORDER BY id DESC",
        connection
    )

    connection.close()

    if df_incidents.empty:

        st.info("No incidents have been reported yet.")

    else:

        st.dataframe(
            df_incidents,
            use_container_width=True
        )




# ============================================================
# ALERTS & NOTIFICATIONS
# ============================================================

def alerts_notifications(df):

    st.title("🔔 Alerts & Notifications")

    # Make sure Defect_Rate is numeric
    df["Defect_Rate"] = pd.to_numeric(
        df["Defect_Rate"],
        errors="coerce"
    )

    # Make sure Downtime_Hours is numeric
    df["Downtime_Hours"] = pd.to_numeric(
        df["Downtime_Hours"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # HIGH DEFECT ALERT - ABOVE 5%
    # --------------------------------------------------------

    high_defects = df[df["Defect_Rate"] > 5]

    if len(high_defects) > 0:

        st.info(
    f"⚠️ High Defect Alert: "
    f"{len(high_defects)} records have defect rate above 5%."
)

    else:

        st.success(
            "✅ No high defect rate alerts."
        )

    # --------------------------------------------------------
    # DOWNTIME ALERT - ABOVE 2 HOURS
    # --------------------------------------------------------

    high_downtime = df[df["Downtime_Hours"] > 2]

    if len(high_downtime) > 0:
        st.info(
    f"🕒 Downtime Alert: "
    f"{len(high_downtime)} records have downtime above 2 hours."
)

    else:

        st.success(
            "✅ No excessive downtime alerts."
        )

    # --------------------------------------------------------
    # ALERT DETAILS
    # --------------------------------------------------------

    st.header("Alert Details")

    if len(high_defects) > 0:

        st.write("### 🔴 High Defect Records")

        st.dataframe(
            high_defects[
                [
                    "Production_ID",
                    "Production_Date",
                    "Product_Name",
                    "Machine_ID",
                    "Defect_Rate",
                    "Quality_Level"
                ]
            ],
            use_container_width=True
        )

    if len(high_downtime) > 0:

        st.write("### 🟠 High Downtime Records")

        st.dataframe(
            high_downtime[
                [
                    "Production_ID",
                    "Production_Date",
                    "Machine_ID",
                    "Downtime_Hours",
                    "Production_Status"
                ]
            ],
            use_container_width=True
        )

# ============================================================
# HISTORY & REPORTS
# ============================================================

# ============================================================
# HISTORY & REPORTS
# ============================================================

def history_reports(df):

    st.title("📄 History & Reports")

    st.write("View production history and download production reports.")

    st.divider()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        if "Production_Date" in df.columns:
            df["Production_Date"] = pd.to_datetime(
                df["Production_Date"],
                errors="coerce"
            )

            min_date = df["Production_Date"].min()
            max_date = df["Production_Date"].max()

            date_range = st.date_input(
                "Select Date Range",
                value=(min_date.date(), max_date.date())
            )

    with col2:
        if "Shift" in df.columns:
            shifts = ["All"] + sorted(
                df["Shift"].dropna().astype(str).unique().tolist()
            )

            selected_shift = st.selectbox(
                "Shift",
                shifts
            )

    with col3:
        if "Production_Status" in df.columns:
            statuses = ["All"] + sorted(
                df["Production_Status"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_status = st.selectbox(
                "Production Status",
                statuses
            )

    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    filtered_df = df.copy()

    # Date filter
    if "Production_Date" in filtered_df.columns:

        if isinstance(date_range, tuple) and len(date_range) == 2:

            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[1])

            filtered_df = filtered_df[
                (filtered_df["Production_Date"] >= start_date)
                &
                (filtered_df["Production_Date"] <= end_date)
            ]

    # Shift filter
    if (
        "Shift" in filtered_df.columns
        and selected_shift != "All"
    ):

        filtered_df = filtered_df[
            filtered_df["Shift"].astype(str) == selected_shift
        ]

    # Status filter
    if (
        "Production_Status" in filtered_df.columns
        and selected_status != "All"
    ):

        filtered_df = filtered_df[
            filtered_df["Production_Status"].astype(str)
            == selected_status
        ]

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.subheader("📊 Production History Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Records",
            len(filtered_df)
        )

    with c2:
        if "Produced_Qty" in filtered_df.columns:
            st.metric(
                "Produced Quantity",
                f"{filtered_df['Produced_Qty'].sum():,.0f}"
            )

    with c3:
        if "Good_Qty" in filtered_df.columns:
            st.metric(
                "Good Quantity",
                f"{filtered_df['Good_Qty'].sum():,.0f}"
            )

    with c4:
        if "Rejected_Qty" in filtered_df.columns:
            st.metric(
                "Rejected Quantity",
                f"{filtered_df['Rejected_Qty'].sum():,.0f}"
            )

    st.divider()

    # --------------------------------------------------------
    # PRODUCTION HISTORY TABLE
    # --------------------------------------------------------

    st.subheader("📋 Production History")

    if filtered_df.empty:

        st.info("No production records found for the selected filters.")

    else:

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=450
        )

    # --------------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------------

    st.subheader("📥 Download Report")

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Production Report",
        data=csv_data,
        file_name="Smart_Textile_Production_Report.csv",
        mime="text/csv"
    )

    # ============================================================
# MAIN APPLICATION
# ============================================================

# ------------------------------------------------------------
# SHOW LOGIN PAGE FIRST
# ------------------------------------------------------------

if not st.session_state.logged_in:

    login_page()

    st.stop()


# ------------------------------------------------------------
# AFTER LOGIN - CONNECT TO MYSQL
# ------------------------------------------------------------

try:

    database_ok, database_error = initialize_database()

    if not database_ok:

        st.error("MySQL connection failed.")
        st.code(database_error)
        st.stop()

except Exception as e:

    st.error("MySQL connection error.")
    st.code(str(e))
    st.stop()


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

sidebar()


# ------------------------------------------------------------
# LOAD PRODUCTION DATA
# ------------------------------------------------------------

try:

    df, data_error = load_data()

    if data_error:

        st.error(
            "Unable to load Production_Data from MySQL."
        )

        st.code(data_error)

        st.stop()

except Exception as e:

    st.error(
        "Error loading production data."
    )

    st.code(str(e))

    st.stop()


# ------------------------------------------------------------
# PAGE ROUTING
# ------------------------------------------------------------

if st.session_state.page == "🏠 Dashboard":

    dashboard(df)


elif st.session_state.page == "📡 Live Production":

    live_production(df)


elif st.session_state.page == "📊 Production Analytics":

    production_analytics(df)


elif st.session_state.page == "🔮 Prediction & Forecasting":

    prediction_forecasting(df)


elif st.session_state.page == "⚙️ Production Optimization":

    production_optimization(df)


elif st.session_state.page == "⚠️ Incident Reporting":

    incident_reporting()


elif st.session_state.page == "🔔 Alerts & Notifications":

    alerts_notifications(df)


elif st.session_state.page == "📄 History & Reports":

    history_reports(df)


elif st.session_state.page == "👤 Profile & Settings":

    profile_settings()