import streamlit as st
from openai import OpenAI

# Groq API 설정
client = OpenAI(
    api_key="your-api-key",  # 🔐 여기에 Groq API 키 입력
    base_url="https://api.groq.com/openai/v1"
)

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")

# 사이드바 설정
with st.sidebar:
    st.markdown("## 🤖 GroqBot")
    st.markdown("AI와 대화할 수 있는 챗봇입니다. Groq API를 사용 중이에요!")
    temperature = st.slider("🎛️ 창의성 (temperature)", 0.0, 1.0, 0.7, 0.1)
    st.markdown("---")
    st.markdown("🔗 [GitHub 저장소](https://github.com/your-repo)")
    st.markdown("📬 문의: your@email.com")

st.title("💬 Groq 기반 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# 이모지 설정
user_emoji = "🧑‍💻"
bot_emoji = "🤖"

# 이전 메시지 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        emoji = user_emoji if msg["role"] == "user" else bot_emoji
        st.markdown(f"{emoji} **{msg['content']}** {emoji}")

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요!..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"{user_emoji} **{prompt}** {user_emoji}")

    # 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🤔 생각 중..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages,
                temperature=temperature  # 👈 사이드바에서 설정한 값 사용
            )
            msg = response.choices[0].message.content
            st.markdown(f"{bot_emoji} **{msg}** {bot_emoji}")

    # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": msg})
