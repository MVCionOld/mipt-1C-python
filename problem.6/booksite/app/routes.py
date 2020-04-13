from flask import render_template

from app import app
from mining import books_miner


@app.route('/')
@app.route('/index')
def index():
    data = books_miner.data
    return render_template(
        'index.html',
        title="Booksite",
        data=data,
    )


@app.route('/<author_href>/')
def author(author_href: str):
    author_storage = list(filter(
        lambda other: author_href in other.href,
        books_miner.data
    ))[0]
    texts, author_name = author_storage.texts, author_storage.author
    return render_template(
        'author.html',
        title=author_name,
        author_name=author_name,
        texts=texts,
    )


@app.route('/<author_name>/<title>')
def text(author_name: str, title: str):
    content = books_miner.get_content(f"{author_name}/{title}")
    return render_template(
        'content.html',
        title=title,
        content=content
    )
