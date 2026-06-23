import time

from google import genai
from google.genai import types

from config import GEMINI_API_KEY
from prompt_templates import COMMON_TEMPLATE, PROMPT_TEMPLATES

client = genai.Client(api_key=GEMINI_API_KEY)


def optimize_prompt(user_prompt, platform, prompt_type):

    template = PROMPT_TEMPLATES.get(prompt_type, "")

    system_prompt = f"""
{COMMON_TEMPLATE}

Target AI Platform:
{platform}

Prompt Category:
{prompt_type}

Category-Specific Instructions:

{template}

Final Instructions:

- Produce a prompt that is immediately usable.
- Do not ask the user unnecessary follow-up questions.
- If reasonable assumptions improve the prompt, make them.
- Prefer creating a complete prompt over returning a questionnaire.
- Return ONLY the optimized prompt.
"""

    last_exception = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model="gemini-3.1-flash-lite",

                contents=user_prompt,

                config=types.GenerateContentConfig(

                    system_instruction=system_prompt,

                    temperature=0.35,

                    max_output_tokens=1000

                )

            )

            return response.text.strip()

        except Exception as e:

            last_exception = e

            if attempt < 2:
                time.sleep(2)

    raise Exception(
        f"Prompt optimization failed after multiple attempts.\n\n{last_exception}"
    )