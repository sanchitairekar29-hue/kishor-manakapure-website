from flask import Flask, render_template, request, flash, Response
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Flash message साठी secret key
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "kishor-website-secret-key"
)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ABOUT / AUTHOR
# =========================

@app.route("/author")
def about():
    return render_template("about.html")


# =========================
# BOOKS
# =========================

@app.route("/books")
def books():
    return render_template("books.html")


# =========================
# AWARDS
# =========================

@app.route("/awards")
def awards():
    return render_template("awards.html")


# =========================
# GALLERY
# =========================

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# =========================
# SAHITYIK VATCHAL
# =========================

@app.route("/sahityik-vatchal")
def sahityik_vatchal():
    return render_template("sahityik-vatchal.html")


# =========================
# CONTACT
# =========================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # Form validation
        if not name or not email or not message:
            flash(
                "कृपया सर्व माहिती पूर्ण भरा.",
                "error"
            )
            return render_template("contact.html")

        # Render Environment Variables
        mail_username = os.environ.get("MAIL_USERNAME")
        mail_password = os.environ.get("MAIL_PASSWORD")
        mail_receiver = os.environ.get("MAIL_RECEIVER")

        # Email settings नसतील तर
        if not mail_username or not mail_password or not mail_receiver:
            flash(
                "ई-मेल सेवा सध्या configure केलेली नाही.",
                "error"
            )
            return render_template("contact.html")

        try:

            # Email तयार करणे
            email_message = EmailMessage()

            email_message["Subject"] = (
                f"Website Contact Message - {name}"
            )

            email_message["From"] = mail_username
            email_message["To"] = mail_receiver

            # Visitor ला reply करता यावा
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

            # Gmail SMTP
            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465
            ) as smtp:

                smtp.login(
                    mail_username,
                    mail_password
                )

                smtp.send_message(
                    email_message
                )

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


# =========================
# SITEMAP
# =========================

@app.route("/sitemap.xml")
def sitemap():

    sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/</loc>
    </url>

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/author</loc>
    </url>

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/books</loc>
    </url>

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/awards</loc>
    </url>

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/gallery</loc>
    </url>

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/sahityik-vatchal</loc>
    </url>

    <url>
        <loc>https://kishor-manakpure-website.onrender.com/contact</loc>
    </url>

</urlset>
"""

    return Response(
        sitemap_xml,
        status=200,
        mimetype="application/xml"
    )


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get("PORT", 5000)
        ),
        debug=False
    )