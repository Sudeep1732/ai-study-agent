from openai import OpenAI
import streamlit as st

# 🔑 PUT YOUR API KEY HERE
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.title("📚 AI Study Assistant")
st.caption("📚 Your personal AI tutor for explanations, summaries, and quick learning")
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask your study question:")

if st.button("📄 Summarize"):
    summary = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize clearly"},
            {"role": "user", "content": user_input}
        ]
    )
    st.write(summary.choices[0].message.content)

if st.button("🧠 Explain Simply"):
    eli5 = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Explain like a beginner"},
            {"role": "user", "content": user_input}
        ]
    )
    st.write(eli5.choices[0].message.content)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a smart study assistant. Explain answers in simple terms, like teaching a student. Give short, clear explanations with examples."
            }
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑‍🎓 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **AI:** {msg['content']}")
