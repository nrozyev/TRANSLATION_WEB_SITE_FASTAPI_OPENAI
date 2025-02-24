from openai import OpenAI
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv
import logging
from typing import List

import os
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def perform_translation(task: int, text: str, Languages:List[str], db: Session):
    logging.log(logging.INFO, "I am in perform")
    translations = {}
    for lang in Languages:
        try:
            response = client.chat.completions.create(
                model = "gpt-4o",
                messages = [{"role": "system", "content": f"You are helpful assistant that translates text to {lang}."},
                            {"role": "user", "content": text}],
                max_tokens=1000
            )
            translated_text = response['choices'][0]['message']['content'].strip()
            translations[lang] = translated_text
        except Exception as e:
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Error:{e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            translations[lang] = f"Unexpected error: {e}"
            update_translation_task(db, task_id, translations)

