import re

from django.shortcuts import render
from .models import RemoveWord


def remove_words(text, words):
    if not words:
        return text
    for word in sorted(words, key=len, reverse=True):
        if not word:
            continue
        pattern = re.compile(re.escape(word), re.IGNORECASE)
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

    return render(request, "index.html", context)
