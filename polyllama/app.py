import streamlit as st
import requests
import json

# Streamlit app title and description
st.title("मराठी LLM")  # Marathi title

# Define Marathi messages
marathi_messages = {
    "question_placeholder": "तुमचे प्रश्न लिहा",
    "button_text": "पाठवा",
    # "no_answer": "उत्तर मिळवण्यात अडचण येत आहे.",
    # "invalid_json": "उत्तर JSON स्वरूपात नाही",
    # "general_error": "अपेक्षित नसलेली त्रुटी",
    # "answer_label": "उत्तर:"
}

# Use a unique key for text input
unique_key = "marathi_text_input"  # More descriptive key
question_placeholder = "question"
button_text = marathi_messages["button_text"]

user_question = st.text_input(question_placeholder, key=unique_key)

if st.button(button_text) and user_question.strip():
    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask_marathi",  # Your FastAPI endpoint
            json={"question": user_question, "language": "marathi"}, # Always send "marathi"
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_data = response.json()

        if "answer" in response_data:  # Correct key!
            response_text = response_data["answer"]  # Correct key!
            # st.write(marathi_messages["answer_label"])  # Use the dictionary for label
            st.write(response_text)
        else:
            st.error("no_answer")

    except requests.exceptions.RequestException as e:
        # Handle API request errors more gracefully
        st.error(f"{'general_error'}: {e}")
    except json.JSONDecodeError as e:
        st.error(f"{'invalid_json'}: {e}")
    except Exception as e:
        st.error(f"{'general_error'}: {e}")