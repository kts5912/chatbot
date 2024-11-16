
import streamlit as st
import openai

# Show title and description.
st.title("💬 삼국시대 챗봇 (GPT-4)")
st.write(
    "이 챗봇은 중국 삼국시대(위, 촉, 오)의 주요 인물, 전투 및 역사적 사건에 대해 전문적으로 대화할 수 있습니다. "
    "또한 GPT-4 모델을 사용하여 보다 복잡한 질문에도 답변합니다."
)

# Load sample Three Kingdoms data (Replace or expand this with a full dataset)
three_kingdoms_data = [
    {
        "title": "Battle of Red Cliffs",
        "content": "The Battle of Red Cliffs (208 CE) was a decisive naval battle fought between Cao Cao and the allied forces of Sun Quan and Liu Bei."
    },
    {
        "title": "Zhuge Liang",
        "content": "Zhuge Liang was a renowned strategist and statesman who served Liu Bei during the Three Kingdoms period."
    }
]

# Function to search Three Kingdoms data
def search_three_kingdoms(query, data):
    results = [item for item in data if query.lower() in item['content'].lower() or query.lower() in item['title'].lower()]
    return results

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set the API key for OpenAI
    openai.api_key = openai_api_key

    # Get user input for question.
    query = st.text_input("질문을 입력하세요:", "")

    if query:
        # Search for relevant information in Three Kingdoms data
        results = search_three_kingdoms(query, three_kingdoms_data)

        if results:
            st.write("### 삼국시대 데이터에서 찾은 결과:")
            for result in results:
                st.write(f"#### {result['title']}")
                st.write(result['content'])
        
        # If no relevant data, use OpenAI GPT-4 for extended response
        if not results:
            st.write("관련 데이터를 찾을 수 없습니다. GPT-4를 사용하여 답변을 생성합니다.")
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a historian specializing in China's Three Kingdoms period."},
                        {"role": "user", "content": query}
                    ]
                )
                st.write("### GPT-4 응답:")
                st.write(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"Error generating response: {e}")
