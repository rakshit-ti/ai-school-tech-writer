
import openai

# from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

import logging

logger = logging.getLogger(__name__)

GPT_TEXT_MODEL = "gpt-4-turbo"


@retry(
    reraise=True,
    wait=wait_exponential(multiplier=1.5, min=30, max=180),
    stop=stop_after_attempt(3),
)
def completion_with_backoff(messages, temperature=0.0) -> str:
    gpt_model = GPT_TEXT_MODEL
    logger.info(f"OpenAI Completion for {gpt_model}, preview: \n{repr(messages)[:100]}")
    try:
        message = openai.chat.completions.create(
            model=gpt_model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
            max_tokens=4096,
        )
        logger.info(f"OpenAI Completion: \n{repr(message)}")

        prompt_tokens, completion_tokens, total_tokens = (
            message.usage.prompt_tokens,
            message.usage.completion_tokens,
            message.usage.total_tokens,
        )
        logger.info(
            f"OpenAI Completion stats: {gpt_model=}, {prompt_tokens=}, {completion_tokens=}, {total_tokens=}"
        )

        return message.choices[0].message.content
    except Exception as e:
        logger.error(type(e).__name__ + ": " + str(e))
        raise e
