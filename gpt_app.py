# app.py
import streamlit as st
from openai import OpenAI
import pandas as pd
from config import OPENAI_API_KEY
from models.diabetes_model import train_model
from services.openai_service import get_advice


def main():
    st.title("Diabetes Prediction and Health Advice App")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            """
        ## Enter the Following Information
        """
        )

        # Input fields
        gender = st.selectbox("Gender:", ["Male", "Female"])
        age = st.text_input("Age:")
        hypertension = st.selectbox("Hypertension:", ["Yes", "No"])
        heart_disease = st.selectbox("Heart Disease:", ["Yes", "No"])
        smoking_history = st.selectbox(
            "Smoking History:",
            ["Never", "No Info", "Current", "Former", "Ever", "Not Current"],
        )
        bmi = st.text_input("BMI:")
        hba1c_level = st.text_input("HBA1C Level:")
        blood_glucose_level = st.text_input("Blood Glucose Level:")

        # Convert inputs to numerical values
        gender_map = {"Male": 1, "Female": 0}
        hypertension_map = {"Yes": 1, "No": 0}
        heart_disease_map = {"Yes": 1, "No": 0}
        smoking_history_map = {
            "Never": 4,
            "No Info": 0,
            "Current": 1,
            "Former": 3,
            "Ever": 2,
            "Not Current": 5,
        }

        val1 = gender_map[gender]
        val2 = int(age) if age else 0
        val3 = hypertension_map[hypertension]
        val4 = heart_disease_map[heart_disease]
        val5 = smoking_history_map[smoking_history]
        val6 = float(bmi) if bmi else 0.0
        val7 = float(hba1c_level) if hba1c_level else 0.0
        val8 = float(blood_glucose_level) if blood_glucose_level else 0.0

        if st.button("Predict"):
            model, feature_names = train_model()

            input_data = pd.DataFrame(
                [[val1, val2, val3, val4, val5, val6, val7, val8]],
                columns=feature_names,
            )

            prediction = model.predict(input_data)
            result = prediction[0]
            result_str = "Diabetic" if result == 1 else "Not Diabetic"
            st.write(f"Result: {result_str}")

            advice = get_advice(val1, val2, val3, val4, val5, val6, val7, val8, result)
            st.write(f"Advice: {advice}")

            st.session_state.prediction_context = {
                "result": result_str,
                "advice": advice,
                "user_info": {
                    "Gender": gender,
                    "Age": val2,
                    "Hypertension": hypertension,
                    "Heart Disease": heart_disease,
                    "Smoking History": smoking_history,
                    "BMI": val6,
                    "HBA1C Level": val7,
                    "Blood Glucose Level": val8,
                },
            }

    with col2:
        st.write("## Chat with the Bot")
        client = OpenAI(api_key=OPENAI_API_KEY)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        st.write("### Pre-defined Questions")
        predefined_questions = [
            "What should I eat if I have diabetes?",
            "Can I still exercise with diabetes?",
            "How can I manage my blood sugar levels?",
            "What are the risks of not treating diabetes?",
            "Should I see a doctor about my diabetes?",
        ]

        for question in predefined_questions:
            if st.button(question):
                prompt = question
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                context = st.session_state.get("prediction_context", {})
                context_prompt = (
                    f"Prediction Result: {context.get('result', 'No prediction made')}\n"
                    f"Advice: {context.get('advice', 'No advice given')}\n"
                    f"User Information: {context.get('user_info', 'No user information available')}\n"
                    "Now, continue the conversation based on the user's input and the context provided."
                )

                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": context_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    stream=True,
                )

                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

        if prompt := st.chat_input("What would you like to ask?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            context = st.session_state.get("prediction_context", {})
            context_prompt = (
                f"Prediction Result: {context.get('result', 'No prediction made')}\n"
                f"Advice: {context.get('advice', 'No advice given')}\n"
                f"User Information: {context.get('user_info', 'No user information available')}\n"
                "Now, continue the conversation based on the user's input and the context provided."
            )

            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": context_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
