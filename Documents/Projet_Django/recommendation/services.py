from decimal import Decimal

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from products.models import Product


FRENCH_STOP_WORDS = {
    "a",
    "au",
    "aux",
    "avec",
    "ce",
    "ces",
    "dans",
    "de",
    "des",
    "du",
    "elle",
    "en",
    "et",
    "la",
    "le",
    "les",
    "leur",
    "leurs",
    "lui",
    "ou",
    "par",
    "pour",
    "que",
    "qui",
    "sur",
    "un",
    "une",
}

POSITIVE_WORDS = {
    "excellent",
    "bon",
    "bonne",
    "utile",
    "clair",
    "claire",
    "parfait",
    "parfaite",
    "interessant",
    "interessante",
    "rapide",
    "qualite",
    "aime",
    "recommande",
}

NEGATIVE_WORDS = {
    "mauvais",
    "mauvaise",
    "lent",
    "lente",
    "cher",
    "chere",
    "decu",
    "decevant",
    "probleme",
    "faible",
    "difficile",
    "ennuyeux",
}


def _price_band(price):
    if price < Decimal("100"):
        return "prix economique"
    if price < Decimal("200"):
        return "prix moyen"
    return "prix premium"


def _product_text(product):
    category = product.category.name
    author = product.author or ""
    return " ".join(
        [
            product.title,
            product.title,
            product.author or "",
            author,
            category,
            product.category.name,
            category,
            product.description,
            _price_band(product.price),
            f"note {product.average_rating}",
        ]
    )


def _explain_match(source, candidate):
    reasons = []
    if source.category_id == candidate.category_id:
        reasons.append(f"meme categorie : {candidate.category.name}")
    if source.author and candidate.author and source.author.lower() == candidate.author.lower():
        reasons.append(f"meme auteur : {candidate.author}")
    if abs(source.price - candidate.price) <= Decimal("50"):
        reasons.append("prix proche")
    if candidate.average_rating >= 4:
        reasons.append("bien note par les clients")
    return ", ".join(reasons[:3]) or "description proche du livre consulte"


def similar_products(product, limit=4):
    products = list(Product.objects.filter(available=True).exclude(pk=product.pk).select_related("category"))
    if not products:
        return []

    corpus = [_product_text(product)] + [_product_text(item) for item in products]
    matrix = TfidfVectorizer(stop_words=list(FRENCH_STOP_WORDS), ngram_range=(1, 2), min_df=1).fit_transform(corpus)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    ranked = []
    for score, candidate in zip(scores, products):
        if product.category_id == candidate.category_id:
            score += 0.18
        if product.author and candidate.author and product.author.lower() == candidate.author.lower():
            score += 0.12
        if abs(product.price - candidate.price) <= Decimal("50"):
            score += 0.05
        candidate.ai_score = min(round(score * 100), 100)
        candidate.ai_reason = _explain_match(product, candidate)
        ranked.append((score, candidate))

    return [candidate for _, candidate in sorted(ranked, key=lambda pair: pair[0], reverse=True)[:limit]]


def recommend_for_query(query, limit=6):
    products = list(Product.objects.filter(available=True).select_related("category"))
    if not products:
        return []

    clean_query = query.strip()
    if not clean_query:
        return []

    corpus = [clean_query] + [_product_text(item) for item in products]
    matrix = TfidfVectorizer(stop_words=list(FRENCH_STOP_WORDS), ngram_range=(1, 2), min_df=1).fit_transform(corpus)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    ranked = []
    for score, candidate in zip(scores, products):
        if candidate.category.name.lower() in clean_query.lower():
            score += 0.15
        if candidate.author and candidate.author.lower() in clean_query.lower():
            score += 0.12
        candidate.ai_score = min(round(score * 100), 100)
        candidate.ai_reason = _query_reason(clean_query, candidate)
        ranked.append((score, candidate))

    sorted_candidates = sorted(ranked, key=lambda pair: pair[0], reverse=True)[:limit]
    return [candidate for score, candidate in sorted_candidates if score > 0]


def _query_reason(query, candidate):
    lower_query = query.lower()
    reasons = []
    if candidate.category.name.lower() in lower_query:
        reasons.append(f"categorie demandee : {candidate.category.name}")
    if candidate.author and candidate.author.lower() in lower_query:
        reasons.append(f"auteur demande : {candidate.author}")
    if any(word in candidate.description.lower() for word in lower_query.split() if len(word) > 3):
        reasons.append("description proche de votre besoin")
    if candidate.average_rating >= 4:
        reasons.append("avis clients favorables")
    return ", ".join(reasons[:3]) or "proximite semantique avec votre demande"


def review_sentiment_summary(product):
    reviews = list(product.reviews.all())
    if not reviews:
        return {
            "label": "Pas encore assez d'avis",
            "score": 0,
            "positive": 0,
            "negative": 0,
            "summary": "Ajoutez des avis clients pour activer l'analyse automatique.",
        }

    positive = 0
    negative = 0
    for review in reviews:
        words = {word.strip(".,;:!?()[]'\"").lower() for word in review.comment.split()}
        positive += len(words & POSITIVE_WORDS)
        negative += len(words & NEGATIVE_WORDS)
        if review.rating >= 4:
            positive += 1
        elif review.rating <= 2:
            negative += 1

    score = positive - negative
    if score > 0:
        label = "Tendance positive"
        summary = "Les clients semblent satisfaits par ce livre."
    elif score < 0:
        label = "Points a surveiller"
        summary = "Certains avis indiquent des reserves a prendre en compte."
    else:
        label = "Tendance neutre"
        summary = "Les avis sont equilibres ou encore insuffisamment detailles."

    return {"label": label, "score": score, "positive": positive, "negative": negative, "summary": summary}
