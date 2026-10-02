import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Assistant")
st.write("مساعدك الذكي للمذاكرة وحل الأسئلة وشرح الدروس")

# API Key
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("⚠️ لم يتم إعداد مفتاح OpenAI API بعد.")
    st.stop()

client = OpenAI(api_key=api_key)

# حفظ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# سؤال الطالب
question = st.chat_input("اكتب سؤالك هنا...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                response = client.responses.create(
                    model="gpt-5.6-mini",
                    instructions="""
أنت مساعد مذاكرة عربي للطلاب.

مهمتك:
- شرح الدروس بطريقة بسيطة وواضحة.
- حل المسائل خطوة بخطوة.
- مساعدة الطالب على فهم الإجابة وليس مجرد إعطائها.
- استخدم اللغة العربية البسيطة.
- إذا كان السؤال علميًا، اذكر السبب والتفسير.
- إذا كان السؤال رياضيات، وضح خطوات الحل.
- إذا كان السؤال غير واضح، اطلب توضيح الجزء الناقص.
- لا تخترع معلومات. إذا لم تكن متأكدًا، وضح ذلك.
""",
                    input=question
                )

                answer = response.output_text
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
