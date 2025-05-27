# lib/debug.py
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

if __name__ == "__main__":
    # Load an author
    author = Author.find_by_name("Alice Smith")
    print("Author:", author.name)

    # View their articles
    for article in author.articles():
        print("Article:", article["title"])

    # Add new article
    magazine = Magazine.find_by_name("Tech Weekly")
    author.add_article(magazine, "New AI Breakthroughs")

    print("Updated Articles:")
    for article in author.articles():
        print("Article:", article["title"])

    # Magazines the author has contributed to
    for mag in author.magazines():
        print("Magazine:", mag["name"])
