import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(page_title="Placement Prediction Dashboard",
                   page_icon="🎓",
                   layout="wide")

st.title("🎓 Placement Prediction Dashboard")

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
df = pd.read_csv("D:\Python\Job_Placement_data\Placement_Prediction_Data.csv")

# Load trained model
#model = joblib.load("placement_model.pkl")

# -------------------------------------------------
# KPI Section
# -------------------------------------------------

total_candidates = len(df)

placement_rate = (df['placed']==1).mean()*100

avg_interview = (
    df['technical_score']+
    df['aptitude_score']+
    df['communication_score']
).mean()/3

avg_skill = df['skills_match_percentage'].mean()

offer_dropout = (df['placed']==0).mean()*100

high_risk = len(df[
    (df['skills_match_percentage']<60) &
    (
        (df['technical_score']+
         df['aptitude_score']+
         df['communication_score'])/3 <60
    )
])/len(df)*100

c1,c2,c3,c4 = st.columns(4)

c1.metric("👨‍🎓 Total Candidates",total_candidates)
c2.metric("🎯 Placement Rate",f"{placement_rate:.2f}%")
c3.metric("🗣 Avg Interview Score",f"{avg_interview:.2f}")
c4.metric("💻 Avg Skills Match",f"{avg_skill:.2f}%")

c5,c6,c7 = st.columns(3)

c5.metric("✅ Job Acceptance",f"{placement_rate:.2f}%")
c6.metric("❌ Offer Dropout",f"{offer_dropout:.2f}%")
c7.metric("⚠ High Risk",f"{high_risk:.2f}%")

st.divider()

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(df.head())

# -------------------------------------------------
# EDA
# -------------------------------------------------

import streamlit as st
import matplotlib.pyplot as plt

st.sidebar.title("📊 Analysis")

chart = st.sidebar.selectbox(
    "Select Analysis",
    (
        "Placement Distribution",
        "Academic Percentage vs Placement",
        "Interview Score Distribution",
        "Company Tier"
    )
)

col1, col2 = st.columns([2,1])

with col1:

    if chart == "Placement Distribution":
        st.subheader("Placement Distribution")

        fig, ax = plt.subplots(figsize=(8,5))
        df['status'].value_counts().plot(kind='bar', ax=ax)
        ax.set_xlabel("Placement Status")
        ax.set_ylabel("Candidates")
        st.pyplot(fig)


    elif chart == "Academic Percentage vs Placement":
        st.subheader("Academic Percentage vs Placement")

        fig, ax = plt.subplots(figsize=(8,5))
        academic = df.groupby('status')[
            ['ssc_percentage','hsc_percentage','degree_percentage']
        ].mean()

        academic.plot(kind='bar', ax=ax)
        st.pyplot(fig)


    elif chart == "Interview Score Distribution":
        st.subheader("Interview Score Distribution")

        fig, ax = plt.subplots(figsize=(8,5))

        interview = (
            df['technical_score']
            + df['aptitude_score']
            + df['communication_score']
        ) / 3

        ax.hist(interview, bins=20)
        ax.set_xlabel("Interview Score")
        ax.set_ylabel("Candidates")

        st.pyplot(fig)


    elif chart == "Company Tier":
        st.subheader("Placed Candidates by Company Tier")
        fig, ax = plt.subplots(figsize=(8,5))
        placed = df[df['status'] == 'Placed']
        placed['company_tier'].value_counts().sort_index().plot(
        kind='bar',
        ax=ax,
        color='green')
        ax.set_xlabel("Company Tier")
        ax.set_ylabel("Placed Candidates")
        ax.set_title("Placed Candidates by Company Tier")
        
        st.pyplot(fig)

with col2:
    st.info("""
    **Dashboard**
    
    Select a chart from the sidebar to visualize different placement analyses.
    """)