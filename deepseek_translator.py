import streamlit as st
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 初始化模型
model = ChatDeepSeek(model="deepseek-chat", temperature=0)

def translator_text(text, language):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system", f"""You are a professional translator. Your task is to accurately translate the given English text into {language}.
            - Preserve the original meaning, tone, and content.
            - Provide a natural, fluent translation.
            - Avoid unnecessary explanations or additional text - return only the translated sentence.
            """
        ),
        ("human", "{text}"),
    ])
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

# Streamlit 应用界面
st.title("WRJ_GenerativeAI_DeepSeek_Translator")

# 语言选择
languages = [
    "English", "Chinese", "Spanish", "German", "French", 
    "Arabic", "Hindi", "Portuguese", "Japanese", "Malaysian"
]
selection = st.multiselect(
    "Select languages to translate into:",
    languages,
    default=["Chinese", "Spanish", "German"],
)

# 用户输入
user_input = st.text_area("Enter text to translate:", "")

if st.button("Translate"):
  if user_input.strip():
    with st.spinner("Translating .."):
      translations={lang:translator_text(user_input,lang) for lang in selection}
    st.subheader("Translations")
    for lang,translation in translations.items():
      st.write(f"**{lang}:**{translation}")
  else:
    st.warning("Enter text please.")
