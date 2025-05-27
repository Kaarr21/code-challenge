import sys
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def top_magazine():
    mag = Magazine.top_publisher()  # Your method to get magazine with most articles
    if mag:
        print(f"Top Magazine: {mag.name} ({mag.category})")
    else:
        print("No magazines found.")

def author_articles(author_name):
    author = Author.find_by_name(author_name)
    if not author:
        print(f"No author found with name '{author_name}'.")
        return
    articles = author.articles()
    if articles:
        print(f"Articles by {author_name}:")
        for art in articles:
            print(f" - {art.title}")
    else:
        print(f"No articles found for author '{author_name}'.")

def magazine_articles(magazine_name):
    mag = Magazine.find_by_name(magazine_name)
    if not mag:
        print(f"No magazine found with name '{magazine_name}'.")
        return
    articles = mag.articles()
    if articles:
        print(f"Articles in {magazine_name}:")
        for art in articles:
            print(f" - {art.title}")
    else:
        print(f"No articles found for magazine '{magazine_name}'.")

def main():
    print("Welcome to Articles CLI. Commands:")
    print("  1. top_magazine")
    print("  2. author_articles <author_name>")
    print("  3. magazine_articles <magazine_name>")
    print("  4. exit")

    while True:
        user_input = input(">>> ").strip()

        if user_input == '1':
            top_magazine()
        elif user_input.startswith('2 '):
            author_name = user_input[2:].strip()
            if author_name:
                author_articles(author_name)
            else:
                print("Please enter author name after command. Usage: 2 <author_name>")
        elif user_input == '2':
            print("Please enter author name after command. Usage: 2 <author_name>")
        elif user_input.startswith('3 '):
            magazine_name = user_input[2:].strip()
            if magazine_name:
                magazine_articles(magazine_name)
            else:
                print("Please enter magazine name after command. Usage: 3 <magazine_name>")
        elif user_input == '3':
            print("Please enter magazine name after command. Usage: 3 <magazine_name>")
        elif user_input == '4':
            print("Exiting CLI.")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
