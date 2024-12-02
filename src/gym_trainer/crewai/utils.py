import streamlit as st

from crewai import LLM
from langchain_groq import ChatGroq

LLM_PROVIDER = "groq" # "google" | "groq"

def get_llm():
    if LLM_PROVIDER == "google":
        return get_google_llm()
    return get_groq_llm()

def get_google_llm():

    llm_config = get_llm_config()
    llm = LLM(
        model="gemini/gemini-1.5-pro-002",
        # api_key=os.environ.get("GOOGLE_API_KEY"),
        provider="google",
        config=llm_config["llm"]["config"]
    )
    return llm

def get_groq_llm():
    llm = ChatGroq(
        temperature=0,
        max_tokens=512,
        groq_api_key=st.secrets["GROQ_API_KEY"],
        # model_name='groq/mixtral-8x7b-32768'
        model='groq/llama3-8b-8192'
    )
    return llm

def get_llm_config():  
    google_llm_config = dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini-pro",
            )
        ),
        embedder = dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        )
    )

    groq_llm_config = dict(
        llm=dict(
            provider="groq",
            config=dict(
                model="llama3-8b-8192",
            )
        ),
        embedder = dict(
            provider="google",
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        )
    )

    return google_llm_config if LLM_PROVIDER == "google" else groq_llm_config

