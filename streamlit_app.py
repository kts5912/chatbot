import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 챗봇")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})



# Three Kingdoms Chatbot Customization
# This modification enhances the chatbot to provide specialized responses about China's Three Kingdoms period.

import streamlit as st
import json

# Sample Data for Three Kingdoms (to be replaced with a complete dataset)
sample_data = [
    {
        "title": "Battle of Red Cliffs",
        "content": "The Battle of Red Cliffs (208 CE) was a decisive naval battle fought between Cao Cao and the allied forces of Sun Quan and Liu Bei."
    },
    {
        "title": "Zhuge Liang",
        "content": "Zhuge Liang was a renowned strategist and statesman who served Liu Bei during the Three Kingdoms period."
    }
]

# Function to load data (here using sample_data)
def load_data():
    return sample_data

# Search function to query Three Kingdoms data
def search_data(query, data):
    results = [item for item in data if query.lower() in item['content'].lower() or query.lower() in item['title'].lower()]
    return results

# Main Streamlit App
def main():
    st.title("Three Kingdoms Chatbot")
    st.write("Ask me anything about China's Three Kingdoms period!")

    data = load_data()
    query = st.text_input("Enter your question:", "")

    if query:
        results = search_data(query, data)
        if results:
            st.write("### Results:")
            for result in results:
                st.write(f"#### {result['title']}")
                st.write(result['content'])
        else:
            st.write("No relevant information found. Please try a different query.")

if __name__ == "__main__":
    main()
