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

left, right =  st.columns(2)

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
          display: flex;
          animation: fadeOut 4s;
        }}
    </style>
    """,
    unsafe_allow_html=True
    )

# OpenAIのAPIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# print(openai_api_key))
left.header("例え上手さん")
add_bg_from_local('static/background.png')  


# 送信ボタンとClearボタンを横並びに配置
col1, col2, col3, col4 = left.columns(4)

word_to_explain = col1.text_input("説明してほしい単語", value="", placeholder="相対性理論")
example_word = col2.text_input("例えてほしい身近なもの", value="", placeholder="漫画ワンピース")

is_submit = col3.button("送信")
is_clear = col4.button("Clear")

if is_clear:
    st.experimental_rerun()  # Streamlitのセッションをリセット


if is_submit:
    # ぐるぐるのアニメーションを表示
    with st.spinner("説明考え中..."):
        sleep(2)  # 2秒待機

        prompt = f"{word_to_explain}について、{example_word}に例えて説明してください。"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.5,
            messages=[
                {"role": "user", "content": prompt}],
        )
        left.write(response.choices[0].message.content)

else:
    left.write("説明文がここに表示されます。")


# class SimpleStreamlitCallbackHandler(BaseCallbackHandler):
#     """ Copied only streaming part from StreamlitCallbackHandler """
    
#     def __init__(self) -> None:
#         self.tokens_area = st.empty()
#         self.tokens_stream = ""
        
#     def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
#         """Run on new LLM token. Only available when streaming is enabled."""
        
#         token = token.replace('\n\n', '\n')
#         token = token.replace('\n', '  \n')
        
#         if token==' ':
#             print('space')
#         if token=='\n':
#             print('n')
#         # if token=='\n\n':
#             # print('nn')

#         if len(token)>1:
#             for s in token:
#                 self.tokens_stream += s
#                 self.tokens_area.markdown(self.tokens_stream)
#         else:
#             self.tokens_stream += token
#             self.tokens_area.markdown(self.tokens_stream)
