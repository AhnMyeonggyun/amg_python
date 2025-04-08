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
    
    system_prompt = st.text_area(
        "시스템 프롬프트 설정",
        value="You are a helpful assistant.",
        help="AI의 성격과 역할을 정의합니다"
    )
    
    if st.button("🔄 대화 내역 초기화"):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
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
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 현재 시스템 프롬프트가 변경되면 업데이트
if st.session_state.messages[0]["content"] != system_prompt:
    st.session_state.messages[0]["content"] = system_prompt

# 이전 메시지 출력
for i, msg in enumerate(st.session_state.messages[1:], 1):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 최대 토큰 관리 (대략적인 방법)
def manage_token_limit(messages, max_messages=20):
    if len(messages) > max_messages + 1:  # +1 for system message
        # 시스템 메시지는 유지하고 가장 오래된 메시지부터 제거
        return [messages[0]] + messages[-(max_messages):]
    return messages

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요!..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 토큰 관리
    st.session_state.messages = manage_token_limit(st.session_state.messages)
    
    # 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 생각 중...")
        
        try:
            # API 클라이언트 초기화
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
            # 응답 요청
            response = client.chat.completions.create(
                model=model_choice,
                messages=st.session_state.messages,
                temperature=0.7
            )
            msg = response.choices[0].message.content
            
            # 응답 표시 (타이핑 효과)
            message_placeholder.empty()
            message_placeholder.markdown(msg)
            
            # 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": msg})
            
        except Exception as e:
            error_msg = f"오류가 발생했습니다: {str(e)}"
            message_placeholder.error(error_msg)
            # 오류 발생 시 마지막 사용자 메시지 유지 (응답 실패 상태)