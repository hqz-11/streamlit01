import streamlit as st
import openai
import os

# Set the API key
openai.api_key = st.secrets["pd"]#鍵はopenaiの会員登録で入手する必要があります。

# Create a text input widget
question = st.text_input("Ask a question:")

# Call the OpenAI API to get the answer
completion = openai.Completion.create(
    engine="text-davinci-002",
    prompt=question,
    max_tokens=1024,
    temperature=0.5,
)

# Get the answer from the API response
answer = completion.choices[0].text

# Display the answer in a text output widget
st.text(answer)
