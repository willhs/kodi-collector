import os
import openai as openai


def ask_gpt_for_response(messages, max_response_tokens=5, model="gpt-3.5-turbo"):
    openai.api_key = os.environ['OPENAI_API_KEY']

    gpt_response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_response_tokens,
        temperature=0.01,
        top_p=1,
        # frequency_penalty=0.0
    )

    response_text = gpt_response.choices[0]['message']['content']
    # trim string
    trimmed_response = response_text.strip()
    return trimmed_response
