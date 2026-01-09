import json
import re
import urllib.error
import urllib.request

from django.conf import settings
from django.shortcuts import render
from .models import AccessLog, RemoveWord


def build_phrase_pattern(phrase):
    parts = re.split(r"\s+", phrase.strip())
    if not parts or parts == [""]:
        return None
    escaped = [re.escape(part) for part in parts]
    return re.compile(r"\s+".join(escaped), re.IGNORECASE)


def remove_words(text, words):
    if not words:
        return text
    for word in sorted(words, key=len, reverse=True):
        if not word:
            continue
        pattern = build_phrase_pattern(word)
        if pattern:
            text = pattern.sub("", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def extract_response_text(payload):
    output = payload.get("output", [])
    texts = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                text = content.get("text", "")
                if text:
                    texts.append(text)
    if texts:
        return "\n".join(texts)
    return payload.get("output_text", "")


def analyze_with_openai(text):
    if not settings.OPENAI_API_KEY:
        return "", "OpenAI API key is not configured."

    request_body = {
        "model": settings.OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "text", "text": settings.OPENAI_SYSTEM_PROMPT}],
            },
            {"role": "user", "content": [{"type": "text", "text": text}]},
        ],
    }
    data = json.dumps(request_body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=data, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=settings.OPENAI_TIMEOUT) as resp:
            payload = json.load(resp)
        result = extract_response_text(payload)
        if not result:
            return "", "OpenAI returned an empty response."
        return result, ""
    except urllib.error.HTTPError as exc:
        return "", f"OpenAI request failed ({exc.code})."
    except urllib.error.URLError:
        return "", "OpenAI request failed (network error)."


def index(request):
    words = list(
        RemoveWord.objects.filter(active=True).values_list("word", flat=True)
    )
    context = {
        "input_text": "",
        "result_text": "",
        "words": words,
        "error": "",
    }

    if request.method == "POST":
        text = request.POST.get("input_text", "")
        cleaned = remove_words(text, words)
        result = ""
        if text.strip():
            result, error = analyze_with_openai(cleaned or text)
            context["error"] = error
            if not result:
                result = cleaned
        context["input_text"] = text
        context["result_text"] = result
        ip_address = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if ip_address:
            ip_address = ip_address.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR", "")
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        AccessLog.objects.create(
            ip_address=ip_address,
            user_agent=user_agent[:300],
            input_length=len(text),
            output_length=len(result),
        )

    return render(request, "index.html", context)
