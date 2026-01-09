import re

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


def index(request):
    words = list(
        RemoveWord.objects.filter(active=True).values_list("word", flat=True)
    )
    context = {
        "input_text": "",
        "result_text": "",
        "words": words,
    }

    if request.method == "POST":
        text = request.POST.get("input_text", "")
        result = remove_words(text, words)
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
