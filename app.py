import streamlit as st
import openai
from time import sleep
import os
import base64
from dotenv import load_dotenv

st.set_page_config(
    layout = "wide",
    page_title = "例え上手さん",

)

file_name = 'src/style.css'
with open(file_name) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_dotenv()

# left, right =  st.columns([3,2])
left, right =  st.columns([3,2])

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    right.markdown(
    f"""
    <style>
        .stApp {{
          background: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1)),
          url(data:image/{"png"};base64,{encoded_string.decode()});
          background-repeat: no-repeat;
          right:0%;
          background-position: right;
          background-size:40%, 40%;
          display: flex;
          animation: fadeOut 4s;
        }}
    </style>
    """,
    unsafe_allow_html=True
    )

# OpenAIのAPIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

text_container = left.markdown(f'<div class="text_container"></div>', unsafe_allow_html=True)
left.header("例え上手さん")
add_bg_from_local('static/background.png')  


# 送信ボタンとClearボタンを横並びに配置
col1, col2, col3, col4 = left.columns(4)

word_to_explain = col1.text_input("説明してほしいこと", value="", placeholder="相対性理論")
example_word = col2.text_input("例えてほしい身近なもの", value="", placeholder="漫画ワンピース")

is_submit = col3.button("送信")
is_clear = col4.button("Clear")

if is_clear:
    st.experimental_rerun()  # Streamlitのセッションをリセット


teacher_container = left.markdown(f'<div class="teacher_container"></div>', unsafe_allow_html=True)
if is_submit:
    teacher_container.empty()
    stop_container = left.markdown(f'<div class="stop_container"></div>', unsafe_allow_html=True)
    student_container = left.markdown(f'<div class="student_container"></div>', unsafe_allow_html=True)
    # ぐるぐるのアニメーションを表示
    with st.spinner("説明考え中..."):
        sleep(2)  # 2秒待機

        prompt = f"{word_to_explain}について、{example_word}に例えて、説明してください。"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.5,
            messages=[
                {"role": "user", "content": prompt}],
        )
        left.write(response.choices[0].message.content)
    stop_container.empty()
    student_container.empty()

else:
    left.write("説明文がここに表示されます。")

