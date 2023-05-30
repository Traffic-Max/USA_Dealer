from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import Post

app = FastAPI()
session = Session()


@app.get("/autopost")
def autopost():
    post = session.query(Post).filter(Post.posted == False).first()  # Выбираем первый непостнутый пост
    if post:
        add_to_post_queue(post)  # Функция добавления поста в очередь публикаций
        post.posted = True
        session.commit()
    else:
        return {"message": "Нет доступных постов для автопостинга"}


def add_to_post_queue(post):
    # Здесь добавьте логику для добавления поста в очередь публикаций в Instagram
    pass
