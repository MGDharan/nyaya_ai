import requests
from app.config import settings

class LLMUnavailable(RuntimeError):
    pass

def generate(system: str, prompt: str) -> str:
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        try:
            r = requests.post(f"{settings.ollama_base_url.rstrip('/')}/api/chat", json={
                "model": settings.ollama_model,
                "stream": False,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                "options": {"temperature": 0.1}
            }, timeout=120)
            r.raise_for_status()
            return r.json()["message"]["content"]
        except Exception as exc:
            raise LLMUnavailable(str(exc)) from exc

    if provider == "openai":
        if not settings.openai_api_key:
            raise LLMUnavailable("OPENAI_API_KEY is not configured")
        try:
            r = requests.post(f"{settings.openai_base_url.rstrip('/')}/chat/completions", headers={
                "Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"
            }, json={"model": settings.openai_model, "temperature": 0.1, "messages": [
                {"role": "system", "content": system}, {"role": "user", "content": prompt}
            ]}, timeout=120)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
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
                "generationConfig": {"temperature": 0.1}
            }
            r = requests.post(url, json=body, timeout=120)
            r.raise_for_status()
            data = r.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text_parts = [p.get("text", "") for p in parts if "text" in p]
                if text_parts:
                    return "".join(text_parts)
            raise LLMUnavailable(f"No text returned from Gemini API: {data}")
        except Exception as exc:
            raise LLMUnavailable(str(exc)) from exc

    raise LLMUnavailable(f"Unknown LLM_PROVIDER: {provider}")
