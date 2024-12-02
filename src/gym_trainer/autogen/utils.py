import streamlit as st
import os

from typing import Union, Literal

LLM_PROVIDER: Union[Literal["google"], Literal["groq"]] = "google" # "google" | "groq"

def get_llm_config():
    llm_config_gemini = {
        "config_list": [
            {
                "model": "gemini-pro",
                "api_key": os.environ.get("GOOGLE_API_KEY"),
                "api_type": "google"
            }
        ]
    }

    llm_config_groq = {
        "config_list": [
            {
                "model": "llama-3.1-8b-instant",
                "api_key": os.environ.get("GROQ_API_KEY"),
                "api_type": "groq",
            }
        ]
    }

    configs = {
        "google": llm_config_gemini,
        "groq": llm_config_groq
    }

    return configs[LLM_PROVIDER]
