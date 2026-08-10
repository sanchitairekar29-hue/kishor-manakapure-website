from flask import Flask, render_template, request, flash
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/google169b32e847ac0d7d.html")
def google_verification():
    return "google-site-verification: google169b32e847ac0d7d.html"
    
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "kishor-website-secret-key"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/author")
def author():
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


@app.route("/sahityik-vatchal")
def sahityik_vatchal():
    return render_template("sahityik-vatchal.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("कृपया सर्व माहिती पूर्ण भरा.", "error")
            return render_template("contact.html")

        mail_username = os.environ.get("MAIL_USERNAME")
        mail_password = os.environ.get("MAIL_PASSWORD")
        mail_receiver = os.environ.get("MAIL_RECEIVER")

        if not mail_username or not mail_password or not mail_receiver:
            flash("ई-मेल सेवा सध्या configure केलेली नाही.", "error")
            return render_template("contact.html")

        try:

            email_message = EmailMessage()

            email_message["Subject"] = f"Website Contact Message - {name}"
            email_message["From"] = mail_username
            email_message["To"] = mail_receiver
            email_message["Reply-To"] = email

            email_message.set_content(
                f"""
नवीन संदेश वेबसाइटच्या Contact Form मधून आला आहे.

नाव:
{name}

ई-मेल:
{email}

संदेश:
{message}
"""
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(mail_username, mail_password)
                smtp.send_message(email_message)

            flash(
                "तुमचा संदेश यशस्वीरित्या पाठवला गेला आहे. धन्यवाद!",
                "success"
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

            flash(
                "संदेश पाठवताना अडचण आली. कृपया पुन्हा प्रयत्न करा.",
                "error"
            )

        return render_template("contact.html")

    return render_template("contact.html")


@app.route("/sitemap.xml")
def sitemap():
    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
<loc>https://kishor-manakapure-website.onrender.com/</loc>
</url>
<url>
<loc>https://kishor-manakapure-website.onrender.com/author</loc>
</url>
<url>
<loc>https://kishor-manakapure-website.onrender.com/books</loc>
</url>
<url>
<loc>https://kishor-manakapure-website.onrender.com/awards</loc>
</url>
<url>
<loc>https://kishor-manakapure-website.onrender.com/gallery</loc>
</url>
<url>
<loc>https://kishor-manakapure-website.onrender.com/sahityik-vatchal</loc>
</url>
<url>
<loc>https://kishor-manakapure-website.onrender.com/contact</loc>
</url>
</urlset>"""

    return sitemap_xml, 200, {
        "Content-Type": "application/xml; charset=utf-8"
    }


# ================= ROBOTS.TXT =================

@app.route("/robots.txt")
def robots():
    robots_txt = """User-agent: *
Allow: /

Sitemap: https://kishor-manakapure-website.onrender.com/sitemap.xml
"""
    return robots_txt, 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )