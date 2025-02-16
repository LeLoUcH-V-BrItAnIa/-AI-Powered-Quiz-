import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_questions(text_content, quiz_level):
    RESPONSE_JSON = {
        "mcq": [
            {
                "mcq": "Multiple Choice Question1",
                "a": "choice here1",
                "b": "choice here2",
                "c": "choice here3",
                "d": "choice here4",
                "correct": "a"
            }
        ]
    }

    PROMPT_TEMPLATE = """
    Text: {text_content}
    You are an expert in generating MCQ-type quizzes based on provided content.
    Given the above text, create a quiz of 3 multiple-choice questions keeping difficulty level as {quiz_level}.
    Make sure the questions are not repeated and are unique.
    Ensure the format of your responses follows RESPONSE_JSON below.

    {RESPONSE_JSON}
    """

    formatted_template = PROMPT_TEMPLATE.format(
        text_content=text_content, quiz_level=quiz_level, RESPONSE_JSON=json.dumps(RESPONSE_JSON)
    )

    # API request
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": formatted_template}],
        temperature=0.3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        max_tokens=1000
    )

    extracted_responses = response.choices[0].message.content
    try:
        return json.loads(extracted_responses).get('mcq', [])
    except json.JSONDecodeError:
        st.error("Error parsing API response. Check your OpenAI output format.")
        return []

def main():
    st.title("Quiz Generator App")

    text_content = st.text_area("Paste the text content here:")
    quiz_level = st.selectbox("Select the quiz level", ['easy', 'medium', 'hard'])

    if st.button("Generate Quiz"):
        questions = fetch_questions(text_content, quiz_level.lower())

        selected_options = []
        correct_answers = []

        for question in questions:
            options = [question["a"], question["b"], question["c"], question["d"]]
            selected_option = st.radio(question["mcq"], options, index=None)
            selected_options.append(selected_option)
            correct_answers.append(question[question["correct"]])  # Fix here

        if st.button("Submit"):
            marks = 0
            st.header("Results")
            for i, question in enumerate(questions):
                st.subheader(f"{question['mcq']}")
                st.write(f"Your Answer: {selected_options[i]}")
                st.write(f"Correct Answer: {correct_answers[i]}")
                if selected_options[i] == correct_answers[i]:
                    marks += 1

            st.subheader(f"You scored {marks} out of {len(questions)}")

if __name__ == "__main__":
    main()