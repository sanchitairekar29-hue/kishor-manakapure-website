from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/author")
def about():
    return render_template("about.html")


@app.route("/books")
def books():
    return render_template("books.html")


@app.route("/awards")
def awards():
    return render_template("awards.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/sahityik-vatchal")
def sahityik_vatchal():
    return render_template("sahityik-vatchal.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)