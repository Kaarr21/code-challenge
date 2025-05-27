from lib.db.transactions import add_author_with_articles

articles = [
    {"title": "Climate Shift", "magazine_id": 1},
    {"title": "Tech Trends", "magazine_id": 3}
]

add_author_with_articles("Asha Nyambura", articles)