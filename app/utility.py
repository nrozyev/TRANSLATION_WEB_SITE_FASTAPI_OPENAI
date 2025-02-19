import openai
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv


import os
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def perform_translation(task: int, text: str, Languages:list, db: Session):
    translations = {}
    for lang in Languages:
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-4o-mini",
                messages = [{"role": "system", "content": f"You are helpful assistant that translates text to {lang}."},
                            {"role": "user", "content": text}],
                engine="text-davinci-003",
                prompt=f"Translate '{text}' from English to {lang}.",
                max_tokens=1000,
                temperature=0.7,
                n=1,
            )
            translations[lang] = response.choices[0].text.strip()
