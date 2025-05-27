#!/usr/bin/env python3
"""
Interactive CLI tool for querying the Articles database
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.transactions import add_author_with_articles

class DatabaseCLI:
    def __init__(self):
        self.commands = {
            '1': self.list_all_authors,
            '2': self.list_all_magazines,
            '3': self.list_all_articles,
            '4': self.find_author_articles,
            '5': self.find_magazine_articles,
            '6': self.author_topic_areas,
            '7': self.magazine_contributors,
            '8': self.top_publisher,
            '9': self.most_prolific_author,
            '10': self.magazine_article_counts,
            '11': self.add_new_author,
            '12': self.add_new_magazine,
            '13': self.add_new_article,
            'q': self.quit
        }

    def display_menu(self):
        print("\n" + "="*50)
        print("📚 ARTICLES DATABASE QUERY TOOL")
        print("="*50)
        print("1.  List all authors")
        print("2.  List all magazines")
        print("3.  List all articles")
        print("4.  Find articles by author")
        print("5.  Find articles by magazine")
        print("6.  Author's topic areas")
        print("7.  Magazine contributors")
        print("8.  Top publisher (most articles)")
        print("9.  Most prolific author")
        print("10. Article counts per magazine")
        print("11. Add new author")
        print("12. Add new magazine")
        print("13. Add new article")
        print("q.  Quit")
        print("-"*50)

    def run(self):
        print("Welcome to the Articles Database CLI!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip().lower()
            
            if choice in self.commands:
                try:
                    self.commands[choice]()
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❌ Invalid choice. Please try again.")

    def list_all_authors(self):
        print("\n📝 ALL AUTHORS:")
        authors = Author.all()
        if not authors:
            print("No authors found.")
            return
        
        for i, author in enumerate(authors, 1):
            print(f"{i:2d}. {author.name} (ID: {author.id})")

    def list_all_magazines(self):
        print("\n📖 ALL MAGAZINES:")
        magazines = Magazine.all()
        if not magazines:
            print("No magazines found.")
            return
            
        for i, magazine in enumerate(magazines, 1):
            print(f"{i:2d}. {magazine.name} - {magazine.category} (ID: {magazine.id})")

    def list_all_articles(self):
        print("\n📄 ALL ARTICLES:")
        articles = Article.all()
        if not articles:
            print("No articles found.")
            return
            
        for i, article in enumerate(articles, 1):
            author = article.author()
            magazine = article.magazine()
            print(f"{i:2d}. '{article.title}' by {author.name if author else 'Unknown'} in {magazine.name if magazine else 'Unknown'}")

    def find_author_articles(self):
        author_name = input("Enter author name: ").strip()
        author = Author.find_by_name(author_name)
        
        if not author:
            print(f"❌ Author '{author_name}' not found.")
            return
            
        articles = author.articles()
        print(f"\n📄 ARTICLES BY {author.name}:")
        
        if not articles:
            print("No articles found.")
            return
            
        for i, article in enumerate(articles, 1):
            magazine = article.magazine()
            print(f"{i:2d}. '{article.title}' in {magazine.name if magazine else 'Unknown'}")

    def find_magazine_articles(self):
        magazine_name = input("Enter magazine name: ").strip()
        magazine = Magazine.find_by_name(magazine_name)
        
        if not magazine:
            print(f"❌ Magazine '{magazine_name}' not found.")
            return
            
        articles = magazine.articles()
        print(f"\n📄 ARTICLES IN {magazine.name}:")
        
        if not articles:
            print("No articles found.")
            return
            
        for i, article in enumerate(articles, 1):
            author = article.author()
            print(f"{i:2d}. '{article.title}' by {author.name if author else 'Unknown'}")

    def author_topic_areas(self):
        author_name = input("Enter author name: ").strip()
        author = Author.find_by_name(author_name)
        
        if not author:
            print(f"❌ Author '{author_name}' not found.")
            return
            
        topics = author.topic_areas()
        print(f"\n🏷️  TOPIC AREAS FOR {author.name}:")
        
        if not topics:
            print("No topic areas found.")
            return
            
        for i, topic in enumerate(topics, 1):
            print(f"{i:2d}. {topic}")

    def magazine_contributors(self):
        magazine_name = input("Enter magazine name: ").strip()
        magazine = Magazine.find_by_name(magazine_name)
        
        if not magazine:
            print(f"❌ Magazine '{magazine_name}' not found.")
            return
            
        contributors = magazine.contributors()
        print(f"\n✍️  CONTRIBUTORS TO {magazine.name}:")
        
        if not contributors:
            print("No contributors found.")
            return
            
        for i, author in enumerate(contributors, 1):
            print(f"{i:2d}. {author.name}")

    def top_publisher(self):
        top_mag = Magazine.top_publisher()
        if top_mag:
            article_count = len(top_mag.articles())
            print(f"\n🏆 TOP PUBLISHER: {top_mag.name} with {article_count} articles")
        else:
            print("❌ No magazines found.")

    def most_prolific_author(self):
        top_author = Author.most_articles()
        if top_author:
            article_count = len(top_author.articles())
            print(f"\n🏆 MOST PROLIFIC AUTHOR: {top_author.name} with {article_count} articles")
        else:
            print("❌ No authors found.")

    def magazine_article_counts(self):
        counts = Magazine.article_counts()
        print("\n📊 ARTICLE COUNTS BY MAGAZINE:")
        
        if not counts:
            print("No data found.")
            return
            
        for i, (name, count) in enumerate(counts, 1):
            print(f"{i:2d}. {name}: {count} articles")

    def add_new_author(self):
        name = input("Enter author name: ").strip()
        if not name:
            print("❌ Author name cannot be empty.")
            return
            
        author = Author.create(name)
        print(f"✅ Author '{author.name}' added successfully! (ID: {author.id})")

    def add_new_magazine(self):
        name = input("Enter magazine name: ").strip()
        category = input("Enter magazine category: ").strip()
        
        if not name or not category:
            print("❌ Magazine name and category cannot be empty.")
            return
            
        magazine = Magazine.create(name, category)
        print(f"✅ Magazine '{magazine.name}' added successfully! (ID: {magazine.id})")

    def add_new_article(self):
        title = input("Enter article title: ").strip()
        content = input("Enter article content (optional): ").strip()
        
        # Show available authors
        authors = Author.all()
        if not authors:
            print("❌ No authors available. Please add an author first.")
            return
            
        print("\nAvailable authors:")
        for i, author in enumerate(authors, 1):
            print(f"{i}. {author.name}")
        
        try:
            author_choice = int(input("Select author (number): ")) - 1
            selected_author = authors[author_choice]
        except (ValueError, IndexError):
            print("❌ Invalid author selection.")
            return
        
        # Show available magazines
        magazines = Magazine.all()
        if not magazines:
            print("❌ No magazines available. Please add a magazine first.")
            return
            
        print("\nAvailable magazines:")
        for i, magazine in enumerate(magazines, 1):
            print(f"{i}. {magazine.name}")
        
        try:
            magazine_choice = int(input("Select magazine (number): ")) - 1
            selected_magazine = magazines[magazine_choice]
        except (ValueError, IndexError):
            print("❌ Invalid magazine selection.")
            return
        
        article = Article.create(title, content, selected_author.id, selected_magazine.id)
        print(f"✅ Article '{article.title}' added successfully! (ID: {article.id})")

    def quit(self):
        print("\n👋 Thank you for using the Articles Database CLI!")
        sys.exit(0)

if __name__ == "__main__":
    cli = DatabaseCLI()
    cli.run()
    