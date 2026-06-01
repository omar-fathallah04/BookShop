from django.shortcuts import render

from .services import recommend_for_query


def assistant(request):
    query = request.GET.get("q", "").strip()
    recommendations = recommend_for_query(query) if query else []
    examples = [
        "Je veux apprendre Django et Python",
        "Un roman facile a lire",
        "Livre sur intelligence artificielle",
        "Un livre management pas trop cher",
    ]
    return render(
        request,
        "recommendation/assistant.html",
        {"query": query, "recommendations": recommendations, "examples": examples},
    )
