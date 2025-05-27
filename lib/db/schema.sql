DROP TABLE IF EXISTS articles;

DROP TABLE IF EXISTS authors;

DROP TABLE IF EXISTS magazines;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors (id),
    FOREIGN KEY (magazine_id) REFERENCES magazines (id)
);

-- Add to your schema.sql for better query performance
CREATE INDEX idx_articles_author_id ON articles(author_id);
CREATE INDEX idx_articles_magazine_id ON articles(magazine_id);
CREATE INDEX idx_magazines_category ON magazines(category);