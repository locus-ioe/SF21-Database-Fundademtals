from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Tag {self.name}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

    tags = db.relationship(
        "Tag", secondary=tags, lazy="subquery", backref=db.backref("posts", lazy=True)
    )

    def __repr__(self):
        return f"<Post {self.title}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"


@app.route("/tags", methods=["GET", "POST"])
def get_tags():
    if request.method == "POST":
        name = request.form["name"]

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()

    return render_template("tags.html", tags=Tag.query.all())


@app.route("/posts", methods=["GET", "POST"])
def get_posts():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        category_id = request.form["category_id"]
        tag_id = request.form["tag_id"]

        post = Post(title=title, body=body, category_id=category_id)
        post.tags.append(Tag.query.get(tag_id))
        db.session.add(post)
        db.session.commit()

    return render_template(
        "posts.html",
        posts=Post.query.all(),
        tags=Tag.query.all(),
        categories=Category.query.all(),
    )


@app.route("/categories", methods=["GET", "POST"])
def get_categories():
    if request.method == "POST":
        name = request.form["name"]

        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

    return render_template("categories.html", categories=Category.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
