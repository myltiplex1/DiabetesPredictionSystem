# services/advice_service.py
from langchain_core.prompts import ChatPromptTemplate
from services.llm import get_llm


def get_personalized_advice(
    gender_code: int,
    age: int,
    hypertension: int,
    heart_disease: int,
    smoking_history_code: int,
    bmi: float,
    hba1c: float,
    blood_glucose: float,
    is_diabetic: int
) -> str:
    """
    Generate personalized initial health advice using Gemini via LangChain. Dont make it too long,    """
    # Human readable values
    gender = "Male" if gender_code == 1 else "Female"
    hypertension_str = "Yes" if hypertension == 1 else "No"
    heart_disease_str = "Yes" if heart_disease == 1 else "No"

    smoking_map = {
        0: "No Info",
        1: "Current",
        2: "Ever",
        3: "Former",
        4: "Never",
        5: "Not Current"
    }
    smoking = smoking_map.get(smoking_history_code, "Unknown")

    status = "diabetic" if is_diabetic == 1 else "not diabetic"

    # Structured prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a warm, professional, realistic and concise health advisor.
You speak directly to the patient using "you".
Be empathetic but straightforward. Never give false hope or dangerous advice."""),
        ("human", """Patient profile:
- Gender:          {gender}
- Age:             {age} years
- Hypertension:    {hypertension}
- Heart disease:   {heart_disease}
- Smoking history: {smoking}
- BMI:             {bmi}
- HbA1c:           {hba1c}
- Blood glucose:   {glucose} mg/dL

Current prediction result: The person is **{status}**.

Please provide personalized recommendations in this structure:

1. Warm, personal greeting
2. Dietary advice (foods and fruits to prefer / limit / avoid)
3. Lifestyle & physical activity recommendations
4. Recommendation about seeing a doctor (including suggested urgency)

Use bullet points where appropriate. Keep total response reasonably concise. Don't make it too long tho""")
    ])

    llm = get_llm(temperature=0.65, max_tokens=650)

    chain = prompt | llm

    response = chain.invoke({
        "gender": gender,
        "age": age,
        "hypertension": hypertension_str,
        "heart_disease": heart_disease_str,
        "smoking": smoking,
        "bmi": bmi,
        "hba1c": hba1c,
        "glucose": blood_glucose,
        "status": status
    })

    return response.content.strip()