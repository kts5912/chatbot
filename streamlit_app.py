import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 삼국시대 전문 챗봇")
st.write(
    "이 챗봇은 OpenAI의 GPT 모델을 활용해 중국 삼국시대에 대한 전문적인 답변을 제공합니다. "
    "사용하려면 OpenAI API 키를 입력하세요. API 키는 [여기서](https://platform.openai.com/account/api-keys) 얻을 수 있습니다. "
    "또한, 앱 제작 방법에 대한 자세한 내용을 [이곳에서](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) 확인할 수 있습니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        # Add a system message with instructions specific to the Three Kingdoms period.
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert on China's Three Kingdoms period (220-280 AD). "
                    "Answer questions with detailed, accurate, and professional-level knowledge. "
                    "When needed, include historical context, key events, and the roles of famous figures like Cao Cao, Liu Bei, Sun Quan, and Zhuge Liang. "
                    "Feel free to discuss the cultural, military, and political aspects of the era."
                ),
            }
        ]

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Enter your question about the Three Kingdoms period:"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4",
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
