from flask import Flask, request, jsonify, render_template_string, url_for
import uuid
import os
import json

app = Flask(__name__)

# Path to the JSON file in the /tmp directory
cards_file_path = "/tmp/cards.json"


def load_cards():
    """Load cards from the JSON file."""
    try:
        with open(cards_file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cards(cards):
    """Save cards to the JSON file."""
    with open(cards_file_path, "w") as file:
        json.dump(cards, file)


# Load existing cards into memory
cards = load_cards()


@app.route("/")
def index():
    # Template path using os
    path = os.path.join(os.path.dirname(__file__), "templates/index.html")
    return render_template_string(open(path).read())


@app.route("/create-card", methods=["POST"])
def create_card():
    data = request.json
    card_id = str(uuid.uuid4())
    cards = load_cards()  # Reload cards in case they've been updated elsewhere
    cards[card_id] = data
    save_cards(cards)  # Save updated cards
    link = url_for("view_card", card_id=card_id, _external=True)
    return jsonify({"link": link})


@app.route("/card/<card_id>")
def view_card(card_id):
    cards = load_cards()  # Ensure we have the latest cards
    card = cards.get(card_id)
    if not card:
        return "Card not found", 404

    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8"/>
            <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"/>
            <meta content="ie=edge" http-equiv="X-UA-Compatible"/>
            <meta content="noindex, follow" name="robots"/>
            <meta content="summary_large_image" name="twitter:card"/>
            <meta content="{{ title }}" name="twitter:title"/>
            <meta content="{{ description }}" name="twitter:description"/>
            <meta content="{{ image_url }}" name="twitter:image"/>
            <meta content="1718023163" property="og:updated_time">
            <meta content="website" property="og:type">
            <meta content="{{ title }}" property="og:title">
            <meta content="{{ description }}" property="og:description">
            <meta content="{{ image_url }}" property="og:image"/>
            <meta content="1281" property="og:image:width">
            <meta content="719" property="og:image:height">
            <title>{{ title }}</title>
        </head>
        <body style="color: white !important;">
            <script>
                location.href = '{{ url }}';
            </script>
        </body>
        </html>
    """,
        **card
    )


if __name__ == "__main__":
    # Note: Do not use debug=True in production
    app.run(debug=True)
