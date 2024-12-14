import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #e0e0e0;
    }
    .stSelectbox > div > div > select {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #e0e0e0;
    }
    .prediction-box {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load the saved model and related objects
@st.cache_resource
def load_model():
    try:
        model_data = joblib.load('model.pkl')
        return model_data
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Prediction function
def predict_student_status(model_data, marital_status, age, admission_grade, 
                            curricular_units_enrolled, gender):
    try:
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
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# Main Streamlit app
def main():
    # Load the model
    model_data = load_model()
    
    # Main content
    st.markdown('<h1 class="main-header">🎓 Student Performance Predictor</h1>', unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📊 Predict Student Academic Status
        Enter the student details below to predict their potential academic performance.
        """)
    
    # Input form
    with st.form(key='student_prediction_form'):
        # Create columns for form inputs
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            # Marital Status
            marital_status = st.selectbox(
                'Marital Status', 
                ['single', 'married', 'divorced', 'widower', 'facto union', 'legally separated'],
                help="Select the student's current marital status"
            )
            
            # Age
            age = st.number_input(
                'Age at Enrollment', 
                min_value=15, 
                max_value=70, 
                value=20,
                help="Enter the student's age when enrolling"
            )
            
            # Gender
            gender = st.selectbox(
                'Gender', 
                ['male', 'female'],
                help="Select the student's gender"
            )
        
        with input_col2:
            # Admission Grade
            admission_grade = st.number_input(
                'Admission Grade', 
                min_value=0.0, 
                max_value=20.0, 
                value=14.5,
                step=0.1,
                help="Enter the student's admission grade (0-20)"
            )
            
            # Curricular Units Enrolled
            curricular_units_enrolled = st.number_input(
                'Curricular Units Enrolled', 
                min_value=1, 
                max_value=15, 
                value=6,
                help="Number of curricular units enrolled in the first semester"
            )
        
        # Submit button
        submit_button = st.form_submit_button(label='Predict Student Status')
    
    # Prediction section
    if submit_button:
        if model_data:
            # Make prediction
            prediction = predict_student_status(
                model_data, 
                marital_status, 
                age, 
                admission_grade, 
                curricular_units_enrolled, 
                gender
            )
            
            if prediction:
                # Display prediction in a styled box
                st.markdown(f"""
                <div class="prediction-box">
                    <h2>Predicted Student Status</h2>
                    <p style="font-size: 24px; color: #2ecc71; font-weight: bold;">
                        {prediction}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional insights based on prediction
                st.markdown("### 🔍 Insights")
                
                # Provide contextual advice based on prediction
                if prediction == 'Graduate':
                    st.success("""
                    Great potential! The student shows promising characteristics for academic success. 
                    Continued support and engagement can help maintain this trajectory.
                    """)
                elif prediction == 'Dropout':
                    st.warning("""
                    There might be challenges ahead. Early intervention and additional support 
                    could help the student stay on track with their academic goals.
                    """)
                else:
                    st.info("""
                    The student's academic path requires careful monitoring. 
                    Personalized guidance might be beneficial.
                    """)
        else:
            st.error("Could not load the prediction model. Please check the model file.")

# Run the app
if __name__ == '__main__':
    main()