import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Configure the Generative AI API with the API key from .env
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("API_KEY not found in .env file. Please set it to your Gemini API key.")
    st.stop()
genai.configure(api_key=API_KEY)
generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
# Initialize the GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", # Using gemini-2.0-flash as per instructions
    generation_config=generation_config
)
# Define a function to start the chat session with dynamic inputs as seen in image_12c512.png
def generate_horror_story(character_name, situation, no_of_lines):
    """
    Generates a horror story based on the provided character, situation, and desired length.

    Args:
        character_name (str): The name of the character in the story.
        situation (str): The situation or setting for the horror story.
        no_of_lines (int): The approximate number of lines for the story.

    Returns:
        str: The generated horror story.
    """
    prompt = (
        f"Write me a horror story with the character name \"{character_name}\" "
        f"and situation \"{situation}\" in {no_of_lines} lines."
    )

    # Start the chat session with the provided prompt
    # history is initialized with the user's prompt
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [prompt],
            },
        ]
    )

    # Send the message and get the response
    response = chat_session.send_message(prompt)

    return response.text

# Streamlit UI as seen in image_12cb85.png and image_12c7da.png
st.set_page_config(layout="centered", page_title="Horror Story Generator")

st.markdown(
    """
    <style>
    .main {
        background-color: #1a1a1a;
        color: #f0f0f0;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input {
        background-color: #333333;
        color: #f0f0f0;
        border: 1px solid #555555;
        border-radius: 8px;
        padding: 10px;
    }
    .stNumberInput>div>div>input {
        background-color: #333333;
        color: #f0f0f0;
        border: 1px solid #555555;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #8b0000;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        background-color: #a00000;
    }
    .stMarkdown h1 {
        color: #ff4d4d;
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    .stMarkdown h3 {
        color: #f0f0f0;
        margin-top: 30px;
        border-bottom: 2px solid #8b0000;
        padding-bottom: 10px;
    }
    .stSpinner > div > div {
        color: #8b0000 !important;
    }
    .stText {
        color: #cccccc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Horror Story Generator")
st.write("Enter the details below to generate your custom horror story:")

# Inputs for the story
character_name = st.text_input("Character Name")
situation = st.text_input("Situation")
no_of_lines = st.number_input("Number of Lines", min_value=1, value=10)

# Button to generate the story
if st.button("Generate Story"):
    if not character_name or not situation:
        st.warning("Please fill in both Character Name and Situation to generate a story.")
    else:
        with st.spinner("Generating your horror story..."):
            try:
                # Generate and display the story
                story = generate_horror_story(character_name, situation, no_of_lines)
                st.subheader("Your Horror Story:")
                st.write(story)
            except Exception as e:
                st.error(f"An error occurred: {e}")


