import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

print("All Authors:")
for author in Author.all():
    print(f"- {author.name}")

print("\nAll Articles:")
for article in Article.all():
    print(f"- {article.title}")

print("\nAll Magazines:")
for mag in Magazine.all():
    print(f"- {mag.name} ({mag.category})")


author = Author.all()[0]
magazine = Magazine.all()[0]

new_article = author.add_article(magazine, "My New Article")
print(f"Article added: {new_article.title}, ID: {new_article.id}")

author = Author.all()[0]
print(f"{author.name}'s topic areas: {author.topic_areas()}")


magazine = Magazine.all()[0]
print(f"{magazine.name} contributors:")
for author in magazine.contributors():
    print(f"- {author.name}")
    