import streamlit as st
import pandas as pd
import pickle
import numpy as np


def occ_func( occupation):
    my_list = []
    occupation_names= ['Occupation_Student','Occupation_Corporate','Occupation_Housewife','Occupation_Others']
    for name in occupation_names:
        if occupation in name:
            my_list.append(1)
        else:
            my_list.append(0)
    return my_list

def Days_Indoors_encode(value):
    if value == '1-14 days':
        return np.random.randint(1, 15)  # Random number between 1 and 14
    elif value == '15-30 days':
        return np.random.randint(15, 31) # Random number between 15 and 30
    elif value == '31-60 days':
        return np.random.randint(31, 61) # Random number between 31 and 60
    elif value == 'Go out Every day':
        return 0  # Assuming 0 means going out every day
    elif value == 'More than 2 months':
        return np.random.randint(61, 181) # Random number greater than 60 (e.g., up to 6 months)
    else:
        print(value, "nnnno")


def predict(social_week,habit, indoors, mental_health, gender,mood_swing,occu, work_inter):
    filename = 'Depression_detection_model.sav'
    classifier = pickle.load(open(filename, 'rb'))

    input_feature = [social_week,habit, indoors, mental_health, gender,mood_swing,occu, work_inter]
    column_names = ['Social_Weakness','Changes_Habits','Days_Indoors','Mental_Health_History','Gender','Mood_Swings',
            'Occupation_Student','Occupation_Corporate','Occupation_Housewife','Occupation_Others', 'Work_Interest',]
    occ_encode = occ_func(input_feature[6])
    input_list = input_feature[:-2] + occ_encode + [input_feature[-1]]
    df = pd.DataFrame([input_list],columns= column_names)
    df['Days_Indoors'] = df['Days_Indoors'].apply(Days_Indoors_encode)
    column_name = ['Gender', 'Changes_Habits', 'Mental_Health_History', 'Mood_Swings', 'Work_Interest', 'Social_Weakness']
    mapping = {'No':0, 'Maybe': 1, 'Yes':2, 'Not sure':1, 'Low':0, 'Medium':1, 'High':2,'None':1,'Female':0, 'Male':1}
    df[column_name] = df[column_name].applymap(lambda x: mapping.get(x, x))
    df[column_name] = df[column_name].applymap(lambda x: mapping.get(x, x))
    out=classifier.predict(df)

    return out

# Apply light blue gradient background
light_blue_gradient_style = """
<style>
    .stApp {
        background: linear-gradient(135deg, #ADD8E6, #4682B4);  /* Light blue to dark blue gradient */
        background-size: 400% 400%;
        animation: blueGradient 15s ease infinite;
        color: black;  /* Change default text color to black */
    }

    @keyframes blueGradient {
        0%{background-position:0% 50%}
        50%{background-position:100% 50%}
        100%{background-position:0% 50%}
    }

    html, body, [class*="css"] {
        color: black;  /* Ensure all text is black */
        font-weight: normal;  /* Optional: Remove bold text if you want */
    }

    .stButton > button {
        background-color: #4682B4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }

    .stSelectbox label {
        color: black !important;  /* Ensure select box labels are black */
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: black !important;  /* Ensure all headers and labels are black */
    }
</style>
"""

# Apply the custom style
st.markdown(light_blue_gradient_style, unsafe_allow_html=True)

# Define choices
yes_maybe_no = ['Choose...', 'Yes', 'No']
days_choices = ['Choose...', '1-14 days', '15-30 days', '31-60 days', 'Go out Every day', 'More than 2 months']
gender_choices = ['Choose...', 'Male', 'Female']
occupation_choices = ['Choose...', 'Student', 'Housewife', 'Corporate', 'Business', 'Others']
moodswing_choices = ['Choose...', 'Low', 'Medium', 'High']

# Create Streamlit form
st.title("Check Whether you are Stressed")


with st.form("ckd_form"):
    # Collect user inputs
    Social_Weakness = st.selectbox("Do you feel socially weak?", yes_maybe_no)
    Changes_Habits = st.selectbox("Have you recently changed any habits?", yes_maybe_no)
    Days_Indoors = st.selectbox("How long have you stayed indoors?", days_choices)
    Mental_Health_History = st.selectbox("Any history of mental health issues?", yes_maybe_no)
    Gender = st.selectbox("Gender", gender_choices)
    Mood_Swings = st.selectbox("Mood swings level", moodswing_choices)
    Occupation = st.selectbox("Occupation", occupation_choices)
    Work_Interest = st.selectbox("Are you interested in your work?", yes_maybe_no)

    # Submit button
    submit = st.form_submit_button("Submit")

    # Validation to check if all fields are filled
    if submit:
        if (Social_Weakness == 'Choose...' or Changes_Habits == 'Choose...' or Days_Indoors == 'Choose...' or
            Mental_Health_History == 'Choose...' or Gender == 'Choose...' or Mood_Swings == 'Choose...' or
            Occupation == 'Choose...' or Work_Interest == 'Choose...'):
            st.error("Please fill out all the fields before submitting.")
        else:
            # Prediction logic
            output = predict(Social_Weakness, Changes_Habits, Days_Indoors, Mental_Health_History, Gender,
                                  Mood_Swings, Occupation, Work_Interest)
            print(output)

            if output == 1:
                st.markdown(
                    "<h3 style='color:#FF4B4B; font-weight: bold;'>😟 Yes, you are stressed.</h3>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<h3 style='color:#28a745; font-weight: bold;'>😊 You are not stressed.</h3>",
                    unsafe_allow_html=True
                )



