import random
import time
from typing import Tuple

import requests
from app.config import settings
from app.services.data_pipeline import estimate_tokens


class LLMUnavailable(RuntimeError):
    pass


def _post_with_retry(url: str, *, json_body: dict, headers: dict | None = None, timeout: int = 120, max_retries: int = 2) -> requests.Response:
    """HTTP POST with exponential backoff + jitter for transient 429/503/network errors."""
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            r = requests.post(url, headers=headers, json=json_body, timeout=timeout)
            if r.status_code in (429, 502, 503, 504) and attempt < max_retries:
                sleep_sec = (0.6 * (2 ** attempt)) + random.uniform(0.05, 0.25)
                time.sleep(sleep_sec)
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as exc:
            last_exc = exc
            if attempt < max_retries:
                sleep_sec = (0.6 * (2 ** attempt)) + random.uniform(0.05, 0.25)
                time.sleep(sleep_sec)
                continue
            raise
    raise LLMUnavailable(str(last_exc))


def generate_with_usage(system: str, prompt: str) -> Tuple[str, int, int, str]:
    """
    Calls configured LLM provider and returns:
    (response_text, input_tokens, output_tokens, model_used)
    """
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        try:
            r = _post_with_retry(
                f"{settings.ollama_base_url.rstrip('/')}/api/chat",
                json_body={
                    "model": settings.ollama_model,
                    "stream": False,
                    "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                    "options": {"temperature": 0.1},
                },
                timeout=120,
            )
            data = r.json()
            text = data["message"]["content"]
            in_tok = int(data.get("prompt_eval_count") or estimate_tokens(system + prompt))
            out_tok = int(data.get("eval_count") or estimate_tokens(text))
            return text, in_tok, out_tok, f"ollama/{settings.ollama_model}"
        except Exception as exc:
            raise LLMUnavailable(str(exc)) from exc

    if provider == "openai":
        if not settings.openai_api_key:
            raise LLMUnavailable("OPENAI_API_KEY is not configured")
        try:
            r = _post_with_retry(
                f"{settings.openai_base_url.rstrip('/')}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json_body={
                    "model": settings.openai_model,
                    "temperature": 0.1,
                    "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                },
                timeout=120,
            )
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage") or {}
            in_tok = int(usage.get("prompt_tokens") or estimate_tokens(system + prompt))
            out_tok = int(usage.get("completion_tokens") or estimate_tokens(text))
            return text, in_tok, out_tok, f"openai/{settings.openai_model}"
        except Exception as exc:
            raise LLMUnavailable(str(exc)) from exc

    if provider == "gemini":
        if not settings.gemini_api_key:
            raise LLMUnavailable("GEMINI_API_KEY is not configured")
        try:
            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
            )
            body = {
                "system_instruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.1},
            }
            r = _post_with_retry(url, json_body=body, timeout=120)
            data = r.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text_parts = [p.get("text", "") for p in parts if "text" in p]
                if text_parts:
                    text = "".join(text_parts)
                    usage = data.get("usageMetadata") or {}
                    in_tok = int(usage.get("promptTokenCount") or estimate_tokens(system + prompt))
                    out_tok = int(usage.get("candidatesTokenCount") or estimate_tokens(text))
                    return text, in_tok, out_tok, f"gemini/{settings.gemini_model}"
            raise LLMUnavailable(f"No text returned from Gemini API: {data}")
        except Exception as exc:
            raise LLMUnavailable(str(exc)) from exc

    raise LLMUnavailable(f"Unknown LLM_PROVIDER: {provider}")


def generate(system: str, prompt: str) -> str:
    text, _, _, _ = generate_with_usage(system, prompt)
    return text
