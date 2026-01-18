# main.py
import streamlit as st
import pandas as pd
from config import GOOGLE_API_KEY
from models.diabetes_model import train_model
from services.advice_service import get_personalized_advice

from langchain_core.prompts import ChatPromptTemplate
from services.llm import get_llm


def main():
    st.set_page_config(page_title="Diabetes Risk & Health Guide", layout="wide")

    st.title("Diabetes Risk Assessment & Health Guidance")

    col1, col2 = st.columns([1, 1.3])

    # ── LEFT COLUMN ── Patient Input & Prediction ────────────────────────────
    with col1:
        st.subheader("Your Information")

        # Input fields
        gender = st.selectbox("Gender", ["Male", "Female"], index=0)
        age_str = st.text_input("Age", "")
        hypertension = st.selectbox("Hypertension", ["No", "Yes"])
        heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
        smoking_history = st.selectbox(
            "Smoking History",
            ["Never", "No Info", "Current", "Former", "Ever", "Not Current"]
        )
        bmi_str = st.text_input("BMI", "")
        hba1c_str = st.text_input("HbA1c Level", "")
        glucose_str = st.text_input("Blood Glucose Level (mg/dL)", "")

        # Mapping dictionaries
        gender_map = {"Male": 1, "Female": 0}
        yesno_map = {"Yes": 1, "No": 0}
        smoking_map = {
            "No Info": 0,
            "Current": 1,
            "Ever": 2,
            "Former": 3,
            "Never": 4,
            "Not Current": 5
        }

        # Validation & conversion
        try:
            values = [
                gender_map[gender],
                int(age_str) if age_str.strip().isdigit() else None,
                yesno_map[hypertension],
                yesno_map[heart_disease],
                smoking_map[smoking_history],
                float(bmi_str) if bmi_str.strip() else None,
                float(hba1c_str) if hba1c_str.strip() else None,
                float(glucose_str) if glucose_str.strip() else None,
            ]

            all_filled = all(v is not None for v in values)

        except (ValueError, KeyError):
            all_filled = False
            values = None

        if st.button("Get Prediction & Advice", type="primary", disabled=not all_filled):
            if not all_filled:
                st.error("Please fill all fields with valid numbers.")
                st.stop()

            with st.spinner("Analyzing..."):
                model, feature_names = train_model()

                input_df = pd.DataFrame([values], columns=feature_names)

                prediction = model.predict(input_df)[0]
                result_str = "Positive (Diabetic)" if prediction == 1 else "Negative (Not Diabetic)"

                st.success(f"**Prediction result:** {result_str}")

                # Get personalized advice
                advice = get_personalized_advice(*values, prediction)

                st.markdown("### Personalized Health Recommendations")
                st.markdown(advice)

                # Save context for chat
                st.session_state.prediction_context = {
                    "result": result_str,
                    "advice": advice,
                    "user_info": {
                        "Gender": gender,
                        "Age": values[1],
                        "Hypertension": hypertension,
                        "Heart Disease": heart_disease,
                        "Smoking History": smoking_history,
                        "BMI": values[5],
                        "HbA1c": values[6],
                        "Blood Glucose": values[7],
                    }
                }

    # ── RIGHT COLUMN ── Chat with AI Assistant ───────────────────────────────
    with col2:
        st.subheader("Talk to Health Assistant")

        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Quick questions
        st.write("**Quick questions you might want to ask:**")
        quick_q = [
            "What foods should I eat / avoid?",
            "Can I exercise? What type is best?",
            "How do I monitor my blood sugar at home?",
            "What are the long-term risks if I ignore this?",
            "When should I see a doctor?"
        ]

        cols = st.columns(2)
        for i, q in enumerate(quick_q):
            if cols[i % 2].button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                with st.chat_message("user"):
                    st.markdown(q)
                generate_response(q)

        # Normal chat input
        if prompt := st.chat_input("Ask anything about diabetes, diet, lifestyle..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            generate_response(prompt)


def generate_response(user_message: str):
    """Generate AI response using LangChain + Gemini with context"""
    context = st.session_state.get("prediction_context", {})

    context_block = f"""Current context:
Prediction result: {context.get('result', 'No prediction yet')}
Previous advice: {context.get('advice', 'No previous advice given')}
User profile: {context.get('user_info', 'No detailed information available')}

Answer naturally, be helpful, empathetic and realistic.
Use the context when relevant. Keep answers clear and reasonably concise."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{context}\n\nYou are a knowledgeable, kind diabetes & general health assistant."),
        ("human", "{question}")
    ])

    llm = get_llm(temperature=0.75, max_tokens=950)

    chain = prompt | llm

    try:
        response = chain.invoke({
            "context": context_block,
            "question": user_message
        })

        answer = response.content.strip()

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"Error connecting to AI assistant: {str(e)}")


if __name__ == "__main__":
    if not GOOGLE_API_KEY:
        st.error("GOOGLE_API_KEY not found. Please set it in your .env file.")
    else:
        main()