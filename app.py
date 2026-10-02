import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Assistant (Gemini)")
st.write("مساعدك الذكي للمذاكرة وحل الأسئلة وشرح الدروس (مجاني)")

# قراءة مفتاح Gemini من الـ Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ لم يتم إعداد مفتاح GEMINI_API_KEY بعد في الـ Secrets.")
    st.stop()

# إعداد عميل جوجل جيميناي
client = genai.Client(api_key=api_key)

# إعدادات شخصية المساعد (System Instructions)
system_instruction = """
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
"""

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
                # تجهيز محتوى المحادثة ليرسله لـ Gemini
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": msg["content"]}]})

                # استخدام النموذج السريع والمجاني gemini-2.5-flash
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config={
                        "system_instruction": system_instruction,
                    }
                )

                answer = response.text
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"حدث خطأ: {e}")
