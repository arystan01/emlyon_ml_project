import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

st.set_page_config(page_title="Bank Loan App", layout="centered")

if "login_step" not in st.session_state:
    st.session_state.login_step = "start"
if "user" not in st.session_state:
    st.session_state.user = ""

#### Login Section ####

st.title("Welcome to your bank account")

if st.session_state.login_step == "start":
    st.header("Click the button below to log in.")
    if st.button("Login",help="Clikk to log in"):
        st.session_state.login_step = "form"
        st.rerun()

elif st.session_state.login_step == "form":
    st.subheader("Please log in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if username.strip() and password.strip():
            st.session_state.user = username
            st.session_state.login_step = "logged"
            st.rerun()
        else:
            st.error("Both fields are required.")

                    ##### Sidebar#####

elif st.session_state.login_step == "logged":
    st.success(f"Welcome back, {st.session_state.user}!")

    def reset_all(excepts=None):
        if excepts is None:
            excepts = []
        for k in [
            "accounts_choice","transfers_choice","loans_choice",
            "advisor_choice","documents_choice","more_choice"
        ]:
            if k not in excepts:
                st.session_state[k] = None

    def on_accounts_change():  reset_all(["accounts_choice"])
    def on_transfers_change(): reset_all(["transfers_choice"])
    def on_loans_change():     reset_all(["loans_choice"])
    def on_advisor_change():   reset_all(["advisor_choice"])
    def on_documents_change(): reset_all(["documents_choice"])
    def on_more_change():      reset_all(["more_choice"])

    with st.sidebar:
        st.header("Menu")

        if st.button("Home"):
            reset_all([])
            st.rerun()

        with st.expander("Accounts", expanded=False):
            accounts_choice = st.radio(
                 "",
                ["Cards","Expenses","Income","Balance"],
                index=None,
                key="accounts_choice",
                on_change=on_accounts_change
            )

        with st.expander("Transfers", expanded=False):
            transfers_choice = st.radio(
                 "",
                ["Make a transfer","Transfer history","Beneficiaries"],
                index=None,
                key="transfers_choice",
                on_change=on_transfers_change
            )

        with st.expander("Loans", expanded=False):
            loans_choice = st.radio(
                 "",
                ["Apply for a loan","Current loans"],
                index=None,
                key="loans_choice",
                on_change=on_loans_change
            )


        with st.expander("Advisor", expanded=False):
            advisor_choice = st.radio(
                    "",
                ["My advisor","Contact advisor","Book an appointment"],
                index=None,
                key="advisor_choice",
                on_change=on_advisor_change
            )

        with st.expander("Documents", expanded=False):
            documents_choice = st.radio(
                    "",
                ["IBAN","Account statement","Supporting documents","Insurance certificates","Other certificates"],
                index=None,
                key="documents_choice",
                on_change=on_documents_change
            )

        more_choice = st.radio(
            "More",
            ["Settings","Logout"],
            index=None,
            key="more_choice",
            on_change=on_more_change
        )

    ##### Main Section #####
    ##### Loans Section #####

    if loans_choice is not None:
        st.title("Loans – " + loans_choice)

        if loans_choice == "Apply for a loan":
            @st.cache_resource
            def load_model():
                return joblib.load(Path("models/best_lgbm.pkl"))

            model = load_model()
            OPTIMAL_THRESHOLD = 0.18944723618090453
            
            col1, col2 = st.columns(2)

##### Personal Information #####

            with col1:
                st.subheader("Personal Information")
                
                gender = st.selectbox("Gender", ["Male", "Female"])
                CODE_GENDER = 1 if gender == "Male" else 0
                
                AGE = st.slider("Age", 18, 70, 30)
                
                family_status = st.selectbox("Marital Status", 
                    ["Single / not married", "Married", "Civil marriage", "Separated", "Widow"])
                family_map = {"Civil marriage": 0, "Married": 1, "Separated": 2, 
                            "Single / not married": 3, "Widow": 4}
                NAME_FAMILY_STATUS = family_map[family_status]
                
                CNT_CHILDREN = st.number_input("Children", 0, 10, 0)
                CNT_FAM_MEMBERS = st.number_input("Family Members", 1, 15, 1)
                
                FLAG_OWN_CAR = 1 if st.selectbox("Owns Car?", ["Yes", "No"]) == "Yes" else 0
                FLAG_OWN_REALTY = 1 if st.selectbox("Owns Property?", ["Yes", "No"]) == "Yes" else 0

##### Employment & Income #####

            with col2:
                st.subheader("Employment & Income")
                
                income = st.number_input("Annual Income ($)", 0, 1000000, 50000, step=5000)
                LOG_INCOME = np.log1p(income)
                
                EXPERIENCE = st.slider("Work Experience (years)", 0, 50, 5)
                
                income_type = st.selectbox("Income Type", 
                    ["Working", "Commercial associate", "Pensioner", "State servant", "Student"])
                income_map = {"Commercial associate": 0, "Pensioner": 1, "State servant": 2, 
                            "Student": 3, "Working": 4}
                NAME_INCOME_TYPE = income_map[income_type]
                
                education = st.selectbox("Education",
                    ["Secondary / secondary special", "Higher education", "Incomplete higher", 
                    "Lower secondary", "Academic degree"])
                edu_map = {"Academic degree": 0, "Higher education": 1, "Incomplete higher": 2,
                        "Lower secondary": 3, "Secondary / secondary special": 4}
                NAME_EDUCATION_TYPE = edu_map[education]
                
                housing = st.selectbox("Housing",
                    ["House / apartment", "With parents", "Municipal apartment", 
                    "Rented apartment", "Office apartment", "Co-op apartment"])
                housing_map = {"Co-op apartment": 0, "House / apartment": 1, "Municipal apartment": 2,
                            "Office apartment": 3, "Rented apartment": 4, "With parents": 5}
                NAME_HOUSING_TYPE = housing_map[housing]

##### Contact Information #####

            st.subheader("Contact Information")
            col3, col4, col5, col6 = st.columns(4)
            FLAG_MOBIL = 1 if col3.checkbox("Mobile Phone", value=True) else 0
            FLAG_WORK_PHONE = 1 if col4.checkbox("Work Phone") else 0
            FLAG_PHONE = 1 if col5.checkbox("Home Phone") else 0
            FLAG_EMAIL = 1 if col6.checkbox("Email", value=True) else 0

##### Prediction Button #####

            st.markdown("---")
            if st.button("Assess Credit Risk"):

                INCOME_PER_PERSON = LOG_INCOME / CNT_FAM_MEMBERS
                AGE_YEARS = AGE / 365
                EXPERIENCE_YEARS = EXPERIENCE / 365
                EMPLOYMENT_RATIO = EXPERIENCE_YEARS / (AGE_YEARS + 0.001)
                IS_UNEMPLOYED = 1 if EXPERIENCE == 0 else 0

##### Input DataFrame #####

                input_data = pd.DataFrame({
                    'CODE_GENDER': [CODE_GENDER],
                    'FLAG_OWN_CAR': [FLAG_OWN_CAR],
                    'FLAG_OWN_REALTY': [FLAG_OWN_REALTY],
                    'CNT_CHILDREN': [CNT_CHILDREN],
                    'NAME_INCOME_TYPE': [NAME_INCOME_TYPE],
                    'NAME_EDUCATION_TYPE': [NAME_EDUCATION_TYPE],
                    'NAME_FAMILY_STATUS': [NAME_FAMILY_STATUS],
                    'NAME_HOUSING_TYPE': [NAME_HOUSING_TYPE],
                    'FLAG_MOBIL': [FLAG_MOBIL],
                    'FLAG_WORK_PHONE': [FLAG_WORK_PHONE],
                    'FLAG_PHONE': [FLAG_PHONE],
                    'FLAG_EMAIL': [FLAG_EMAIL],
                    'CNT_FAM_MEMBERS': [CNT_FAM_MEMBERS],
                    'AGE': [AGE],
                    'EXPERIENCE': [EXPERIENCE],
                    'LOG_INCOME': [LOG_INCOME]
                })

                probability = model.predict_proba(input_data)[0]
               

                prediction = 1 if probability[1] >= OPTIMAL_THRESHOLD else 0

##### Output #####

                if prediction == 0:
                    st.success(f"GOOD CLIENT — Confidence: {probability[0]*100:.1f}%")
                else:
                    st.error(f"RISKY CLIENT — Risk: {probability[1]*100:.1f}%")
            st.stop()

##### Current Loans #####

        elif loans_choice == "Current loans":
            st.info("There are no existing loans linked to your account. To request a new loan or check your eligibility, please visit the ‘Apply for a loan’ tab.")
            st.stop()

##### Transfers Section #####

    elif transfers_choice is not None:
        st.title("Transfers – " + transfers_choice)
        if transfers_choice == "Make a transfer":
            st.info("Transfer functionality is currently unavailable.")
        elif transfers_choice == "Transfer history":
            st.info("You have no transfer history.")
        elif transfers_choice == "Beneficiaries":
            st.info("You have no beneficiaries added.")
        st.stop()

##### Accounts Section #####

    elif accounts_choice is not None:
        st.title("Accounts – " + accounts_choice)
        if accounts_choice == "Cards":
            st.info("Visa International — **** 4821")
            st.info("Mastercard Gold — **** 9934")
        elif accounts_choice == "Expenses":
            st.info("Your total expenses for this month are 634.69€")
        elif accounts_choice == "Income":
            st.info("Your total income for this month is 1,200.00€")
        elif accounts_choice == "Balance":
            st.info("Your current balance is 565.31€")
        st.stop()

##### Advisor Section #####

    elif advisor_choice is not None:
        st.title("Advisor – " + advisor_choice)

        if advisor_choice == "My advisor":

            st.write("Name: Sarah Johnson")
            st.write("Phone: +1 555 238 990")
            st.write("Email: sarah.johnson@bank.com")

        elif advisor_choice == "Contact advisor":
            st.subheader("Contact Your Advisor")

            name = st.text_input("Your name")
            topic = st.selectbox("Subject",
                                ["Loan question", "Account issue", "Technical request", "Other"])
            message = st.text_area("Message")

            if st.button("Send message"):
                if name.strip() == "" or message.strip() == "":
                    st.error("Please fill in all fields before sending your message.")
                else:
                    st.success("Your message has been successfully sent.")

        elif advisor_choice == "Book an appointment":

            date = st.date_input("Choose a date")
            time = st.time_input("Choose a time")

            notes = st.text_area("Notes (optional)")

            if st.button("Confirm appointment"):
                st.success(f"Your appointment has been scheduled for {date} at {time}.")

        st.stop()

##### Documents Section #####

    elif documents_choice is not None:
        st.title("Documents – " + documents_choice)
        st.info("No documents available.")
        st.stop()

##### More Section #####
##### Settings #####

    elif more_choice == "Settings":
        st.title("Settings")

        st.subheader("Notifications")
        news = st.checkbox("Receive news and updates")
        loan_updates = st.checkbox("Receive notifications about loan eligibility")
        balance_alerts = st.checkbox("Alert me when my balance is below €50")

        st.markdown("---")

        st.subheader("Communication Preferences")

        st.write("If you want to receive updates by email, you can enter your address below.")
        contact_email = st.text_input("Email")

        if st.button("Save preferences"):
            st.success("Your preferences have been saved.")

        st.markdown("---")
        st.stop()

#####logout #####

    elif more_choice == "Logout":
        st.session_state.login_step = "start"
        st.session_state.user = ""
        st.rerun()

##### Home Section #####

    st.title("Welcome to your bank account")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Balance")
        st.metric("", "800.40€")
    with col2:
        st.subheader("Last Month Expenses")
        st.metric("", "634.69€")
    st.subheader("Your Cards")
    st.write("- Visa International — **** 4821")
    st.write("- Mastercard Gold — **** 9934")
    st.subheader("Recent Transactions")
    st.write("- Columbus : 4.20€")
    st.write("- Uber : 12.50€")
    st.write("- Netflix : 17.99€")
    st.write("- Rent : 600.00€")
