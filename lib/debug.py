from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def main():
    print("🔁 Running debug test...\n")

    conn = get_connection()

    # === AUTHOR TEST ===
    author = Author.create("Octavia Butler")
    if author:
        print(f"✅ Author created: {author.id} - {author.name}")
    else:
        print("❌ Author creation failed")

    fetched_author = Author.find_by_id(author.id) if author else None
    if fetched_author:
        print(f"✅ Author fetched: {fetched_author.id} - {fetched_author.name}")
    else:
        print("❌ Author not found")

    # === MAGAZINE TEST ===
    magazine = Magazine.create("Tech Weekly", "Technology")
    if magazine:
        print(f"✅ Magazine created: {magazine.id} - {magazine.name} ({magazine.category})")
    else:
        print("❌ Magazine creation failed")

    fetched_magazine = Magazine.find_by_id(magazine.id) if magazine else None
    if fetched_magazine:
        print(f"✅ Magazine fetched: {fetched_magazine.id} - {fetched_magazine.name}")
    else:
        print("❌ Magazine not found")

    # === ARTICLE TEST ===
    if author and magazine:
        article = Article.create("Inside the Mind of Gen Z", author.id, magazine.id)
        if article:
            print(f"✅ Article created: {article.id} - '{article.title}' by Author ID {article.author_id}")
        else:
            print("❌ Article creation failed")

        fetched_article = Article.find_by_id(article.id) if article else None
        if fetched_article:
            print(f"✅ Article fetched: {fetched_article.id} - '{fetched_article.title}'")
        else:
            print("❌ Article not found")
    else:
        print("⚠️ Skipping article test — Author or Magazine missing.")

    from lib.models.magazine import Magazine

print("\n🔁 Running magazine debug test...")

mag1 = Magazine.create("The Atlantic", "Politics")
print(f"✅ Created: {mag1}")

fetched_mag = Magazine.find_by_id(mag1.id)
print(f"✅ Fetched by ID: {fetched_mag.id} - {fetched_mag.name} ({fetched_mag.category})")

def main():
    print("\n🔁 Running debug test...\n")

    # Create Author
    author = Author.create("Octavia Butler")
    print(f"✅ Author created: {author.id} - {author.name}")

    # Find Author
    fetched_author = Author.find_by_id(author.id)
    print(f"✅ Author fetched: {fetched_author.id} - {fetched_author.name}")

    # Create Magazine
    magazine = Magazine.create("Tech Weekly", "Technology")
    print(f"✅ Magazine created: {magazine.id} - {magazine.name} ({magazine.category})")

    # ...continue with Article creation



if __name__ == "__main__":
    main()
