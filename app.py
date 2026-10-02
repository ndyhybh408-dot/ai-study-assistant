import streamlit as st
import os
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Assistant (Gemini)")
st.write("مساعدك الذكي للمذاكرة وشرح الدروس (مجاني)")

# وضع المفتاح بطريقة مباشرة ومتوافقة مع مكتبة genai
API_KEY = "AQ.Ab8RN6Iy3Wu2vHj_86tRUGmwaKQxyPo1lCUnQqjkwVCxyA8bKA"

try:
    # تهيئة العميل باستخدام متغير البيئة لضمان عدم حدوث خطأ 401
    os.environ["GEMINI_API_KEY"] = API_KEY
    client = genai.Client()
except Exception as e:
    st.error(f"خطأ في الاتصال: {e}")

system_instruction = "أنت مساعد مذاكرة عربي للطلاب. مهمتك شرح الدروس وحل المسائل ببساطة."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("اكتب سؤالك هنا...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": msg["content"]}]})

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config={"system_instruction": system_instruction}
                )
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"عذراً، حدث خطأ: {e}")
 
