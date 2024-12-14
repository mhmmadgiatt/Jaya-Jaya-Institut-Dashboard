import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import joblib
import numpy as np
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Jaya Jaya Institut Dashboard", layout="wide", page_icon="🎓")

# Custom CSS for styling
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
    color: #333;
}
.highlight {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
}
.stMetric {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: unset;
    background-color: #f0f2f6;
    color: #333;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/processed_data.csv")
    return df

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

# Prediction function
def predict_student_status(model_data, marital_status, age, admission_grade, 
                           curricular_units_enrolled, gender):
    # Prepare the input data
    input_data = pd.DataFrame({
        'Marital_status': [marital_status],
        'Age_at_enrollment': [age],
        'Admission_grade': [admission_grade],
        'Curricular_units_1st_sem_enrolled': [curricular_units_enrolled],
        'Gender': [gender]
    })

    # Encode categorical variables
    input_data['Marital_status_encoded'] = model_data['label_encoders']['marital_status'].transform(input_data['Marital_status'])
    input_data['Gender_encoded'] = model_data['label_encoders']['gender'].transform(input_data['Gender'])

    # Select and scale features
    X_input = input_data[model_data['feature_names']]
    X_input_scaled = model_data['scaler'].transform(X_input)

    # Make prediction
    prediction_encoded = model_data['model'].predict(X_input_scaled)

    # Decode the prediction
    prediction = model_data['label_encoders']['status'].inverse_transform(prediction_encoded)

    return prediction[0]

# Load data and model
df = load_data()
model_data = load_model()

# Dashboard Title
st.title("🎓 Jaya Jaya Institut - Student Performance Insights")

section = st.sidebar.radio("🔍 Navigation", [
    "Dashboard Overview", 
    "Student Status Deep Dive", 
    "Academic Performance", 
    "Demographic Insights", 
    "Predictive Analytics"
])

# Main Dashboard Content
if section == "Dashboard Overview":
    st.header("Institutional Overview")
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(df), "🧑‍🎓")
    with col2:
        avg_admission_grade = df['Admission_grade'].mean()
        st.metric("Avg. Admission Grade", f"{avg_admission_grade:.2f}", "📊")
    with col3:
        scholarship_holders = df[df['Scholarship_holder'] == 'yes'].shape[0]
        st.metric("Scholarship Students", f"{scholarship_holders} ({scholarship_holders/len(df)*100:.1f}%)", "💡")
    
    # Status Distribution
    st.subheader("Student Status Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_status = px.pie(
            df, 
            names='Status', 
            title='Student Status Breakdown',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        fig_status_gender = px.histogram(
            df, 
            x='Status', 
            color='Gender', 
            barmode='group',
            title='Status by Gender',
            color_discrete_sequence=['#FF6B6B', '#4ECDC4']
        )
        st.plotly_chart(fig_status_gender, use_container_width=True)

elif section == "Student Status Deep Dive":
    st.header("Student Status Analysis")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Status by Tuition", "Status by Scholarship", "Status by Marital Status"])
    
    with tab1:
        st.subheader("Student Status by Tuition Payment")
        fig_status_tuition = px.histogram(
            df, 
            x='Tuition_fees_up_to_date', 
            color='Status', 
            barmode='group',
            title='Student Status by Tuition Payment',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_status_tuition, use_container_width=True)
    
    with tab2:
        st.subheader("Student Status by Scholarship")
        fig_status_scholarship = px.histogram(
            df, 
            x='Scholarship_holder', 
            color='Status', 
            barmode='group',
            title='Student Status by Scholarship',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_status_scholarship, use_container_width=True)
    
    with tab3:
        st.subheader("Student Status by Marital Status")
        fig_status_marital = px.histogram(
            df, 
            x='Marital_status', 
            color='Status', 
            barmode='group',
            title='Student Status by Marital Status',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_status_marital, use_container_width=True)

elif section == "Academic Performance":
    st.header("Academic Performance Insights")
    
    # Tabs for different performance views
    tab1, tab2, tab3 = st.tabs(["Admission Grade", "Curricular Units", "Age vs Performance"])
    
    with tab1:
        st.subheader("Admission Grade Distribution")
        fig_admission = px.box(
            df, 
            x='Status', 
            y='Admission_grade', 
            title='Admission Grade by Student Status',
            color='Status',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_admission, use_container_width=True)
    
    with tab2:
        st.subheader("Curricular Units Performance")
        fig_units = px.scatter(
            df, 
            x='Curricular_units_1st_sem_enrolled', 
            y='Curricular_units_1st_sem_approved', 
            color='Status',
            title='Enrolled vs Approved Curricular Units',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_units, use_container_width=True)
    
    with tab3:
        st.subheader("Age vs Academic Performance")
        fig_age_perf = px.scatter(
            df, 
            x='Age_at_enrollment', 
            y='Admission_grade', 
            color='Status',
            title='Age and Admission Grade Relationship',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_age_perf, use_container_width=True)

elif section == "Demographic Insights":
    st.header("Demographic and Program Analysis")
    
    # Tabs for demographic views
    tab1, tab2, tab3 = st.tabs(["Program Distribution", "Nationality", "Course Insights"])
    
    with tab1:
        st.subheader("Students per Program")
        course_counts = df['Course'].value_counts().reset_index()
        course_counts.columns = ['Course', 'Count']
        
        fig_course = px.bar(
            course_counts, 
            x='Course', 
            y='Count',
            title='Number of Students per Program',
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig_course.update_layout(height=600, xaxis_tickangle=-45)
        st.plotly_chart(fig_course, use_container_width=True)
    
    with tab2:
        st.subheader("Student Nationality Distribution")
        nationality_counts = df['Nacionality'].value_counts()
        
        # Menambahkan pull untuk memisahkan bagian kecil
        pull_values = [0.2 if value < 0.05 * nationality_counts.sum() else 0 for value in nationality_counts.values]
        
        fig_nationality = px.pie(
            values=nationality_counts.values, 
            names=nationality_counts.index, 
            title='Student Nationality Distribution',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        # Memperjelas ukuran dan memberikan informasi persentase
        fig_nationality.update_traces(
            pull=pull_values,
            textinfo='percent+label',  # Tambahkan label dan persentase
            textfont_size=14          # Ukuran font untuk label
        )
        
        # Atur ukuran chart
        fig_nationality.update_layout(
            height=600,  # Tinggi grafik
            width=800,   # Lebar grafik
            margin=dict(t=50, b=50, l=50, r=50)  # Margin grafik
        )
        
        st.plotly_chart(fig_nationality, use_container_width=False)
    
    with tab3:
        st.subheader("Course Performance")
        course_performance = df.groupby('Course')['Status'].value_counts(normalize=True).unstack()
        
        fig_course_perf = px.imshow(
            course_performance, 
            title='Course Performance by Status',
            labels=dict(x="Status", y="Course", color="Percentage"),
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_course_perf, use_container_width=True)

elif section == "Predictive Analytics":
    st.header("Student Status Predictor")
    
    # Prediction Input Form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            marital_status = st.selectbox("Marital Status", df['Marital_status'].unique())
            age = st.number_input("Age at Enrollment", min_value=15, max_value=70, value=20)
            gender = st.selectbox("Gender", df['Gender'].unique())
        
        with col2:
            admission_grade = st.number_input("Admission Grade", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
            curricular_units_enrolled = st.number_input("Curricular Units Enrolled", min_value=1, max_value=20, value=6)
        
        predict_button = st.form_submit_button("Predict Student Status")
    
    if predict_button:
        prediction = predict_student_status(
            model_data, 
            marital_status, 
            age, 
            admission_grade, 
            curricular_units_enrolled, 
            gender
        )
        st.success(f"Predicted Student Status: {prediction}")
        
        # Probability Distribution Visualization
        probabilities = model_data['model'].predict_proba(
            model_data['scaler'].transform([[
                model_data['label_encoders']['marital_status'].transform([marital_status])[0],
                age,
                admission_grade,
                curricular_units_enrolled,
                model_data['label_encoders']['gender'].transform([gender])[0]
            ]])
        )[0]
        
        status_labels = model_data['label_encoders']['status'].classes_
        
        fig_proba = px.bar(
            x=status_labels, 
            y=probabilities, 
            title='Prediction Probability Distribution',
            labels={'x': 'Student Status', 'y': 'Probability'},
            color=probabilities,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_proba, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🎓 Jaya Jaya Institut Dashboard")
st.sidebar.markdown("© 2024 Data Analytics Team")