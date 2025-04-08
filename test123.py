import streamlit as st
from openai import OpenAI
import time

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("💬 Groq 기반 챗봇")

# 사이드바 설정
with st.sidebar:
    st.markdown("## 🤖 GroqBot 설정")
    
    api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_로 시작하는 키 입력")
    
    model_choice = st.selectbox("🧠 사용할 AI 모델 선택", [
        "llama3-8b-8192",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ])
    
    if st.button("🔄 대화 내역 초기화"):
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        st.success("대화 내역이 초기화되었습니다!")
    
    st.markdown("ℹ️ 좌측에 API 키와 모델을 설정한 뒤 대화를 시작하세요.")
    st.markdown("---")
    st.markdown("### 📚 모델 정보")
    st.markdown("""
    - **llama3-8b-8192**: 가벼운 모델, 빠른 응답
    - **llama3-70b-8192**: 고성능 모델, 더 정확한 응답
    - **mixtral-8x7b-32768**: 긴 컨텍스트 지원, 다양한 능력
    - **gemma-7b-it**: 구글의 경량 모델
    """)

# API 키가 입력되어야 진행
if not api_key:
    st.warning("👈 왼쪽 사이드바에서 Groq API 키를 입력해주세요.")
    st.stop()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# 이전 메시지 출력
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 최대 토큰 관리
def manage_token_limit(messages, max_messages=20):
    if len(messages) > max_messages + 1:
        return [messages[0]] + messages[-(max_messages):]
    return messages

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요!..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages = manage_token_limit(st.session_state.messages)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 생각 중...")

        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )

            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                temperature=0.7
            )
            msg = response.choices[0].message.content

            message_placeholder.empty()
            message_placeholder.markdown(msg)

            st.session_state.messages.append({"role": "assistant", "content": msg})

        except Exception as e:
            message_placeholder.error(f"오류가 발생했습니다: {str(e)}")
