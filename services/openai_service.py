# services/openai_service.py
from openai import OpenAI
from config import OPENAI_API_KEY


def get_advice(val1, val2, val3, val4, val5, val6, val7, val8, result):
    gender = "Male" if val1 == 1 else "Female"
    hypertension = "Yes" if val3 == 1 else "No"
    heart_disease = "Yes" if val4 == 1 else "No"
    smoking_history = ["No Info", "Current", "Ever", "Former", "Never", "Not Current"][
        val5
    ]

    prompt = f"""
    You are a health advisor. Here is the information about the patient:
    - Gender: {gender}
    - Age: {val2}
    - Hypertension: {hypertension}
    - Heart Disease: {heart_disease}
    - Smoking History: {smoking_history}
    - BMI: {val6}
    - HBA1C Level: {val7}
    - Blood Glucose Level: {val8}

    The prediction result indicates that you are {'diabetic' if result == 1 else 'not diabetic'}.

    MAKE IT AS CONVERSATIONAL AS POSSIBLE, and CONCISE.
    Based on this information, please provide personalized recommendations directly for the patient. 

    Format your response as follows:
    - Start with a friendly greeting and address the patient directly using "you."
    - Provide specific dietary recommendations, including fruits and other foods.
    - Offer general health advice and lifestyle changes.
    - Advise on whether a doctor's visit is necessary and the urgency of the visit.
    - Use bullet points or a clear format to make it easy to follow..
    """

    client = OpenAI(api_key=OPENAI_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a health advisor providing personalized recommendations directly to the patient based on their information.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content.strip()
