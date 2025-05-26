#!/usr/bin/env python3

from models.author import Author
from models.article import Article
from models.magazine import Magazine

def main():
    print("Welcome to the Article Management System Debug Console!")
    print("\nAvailable models: Author, Article, Magazine")
    print("\nExample commands:")
    print("1. Create an author:")
    print("   author = Author.create('John Doe')")
    print("\n2. Find author by ID:")
    print("   author = Author.find_by_id(1)")
    print("\n3. Get author's articles:")
    print("   articles = author.articles()")
    print("\n4. Create a magazine:")
    print("   magazine = Magazine.create('Tech Weekly', 'Technology')")
    print("\n5. Add an article:")
    print("   author.add_article(magazine.id, 'My New Article')")
    print("\n6. Find most prolific author:")
    print("   top_author = Author.most_prolific()")
    print("\n7. Find magazine's contributors:")
    print("   contributors = magazine.contributors()")
    print("\nType 'exit()' to quit")

if __name__ == '__main__':
    main()
    import code
    code.interact(local=locals())
