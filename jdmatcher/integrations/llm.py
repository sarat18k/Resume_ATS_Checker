import logging
import time

from openai import OpenAI

from jdmatcher.settings import get_settings

logger = logging.getLogger(__name__)


def _client() -> OpenAI | None:
    api_key = get_settings().openai_api_key
    if not api_key:
        logger.warning("OPENAI_API_KEY is not configured")
        return None
    return OpenAI(api_key=api_key)


def llm_query(prompt: str, json_mode: bool = False, model: str | None = None) -> str:
    client = _client()
    if not client:
        return "Error: OpenAI API Key not configured."

    settings = get_settings()
    kwargs = {
        "model": model or settings.openai_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    for attempt in range(3):
        try:
            started = time.perf_counter()
            response = client.chat.completions.create(**kwargs)
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")

            usage = response.usage
            if usage:
                logger.info(
                    "LLM call %sms tokens prompt=%s completion=%s total=%s",
                    elapsed_ms,
                    usage.prompt_tokens,
                    usage.completion_tokens,
                    usage.total_tokens,
                )
            else:
                logger.info("LLM call completed in %sms", elapsed_ms)
            return content
        except Exception as exc:
            logger.warning("LLM attempt %s failed: %s", attempt + 1, exc)
            if attempt < 2:
                time.sleep(2**attempt)

    return "{}" if json_mode else "Error: LLM request failed after retries."
