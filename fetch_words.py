import requests, json, time

WORDS = [
    ("Hund", "der", "Hunde", "dog"),
    ("Katze", "die", "Katzen", "cat"),
    ("Buch", "das", "Bücher", "book"),
]

def get_tatoeba(word):
    url = f"https://tatoeba.org/eng/api_v0/search?query={word}&from=deu&to=eng&orphans=no&unapproved=no"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        sentences = [hit["text"] for hit in data.get("results", [])[:3]]
        return sentences if sentences else [f"Beispielsatz mit {word}."]
    except Exception as e:
        print("Error fetching sentences:", e)
        return [f"Beispielsatz mit {word}."]

def make_card(word, article, plural, trans):
    return {
        "id": f"{word}-{int(time.time())}",
        "word": word,
        "article": article,
        "plural": plural,
        "trans": trans,
        "sentences": get_tatoeba(word),
        "box": 1,
        "due": 0,
        "stats": {"seen": 0, "correct": 0}
    }

def main():
    deck = {
        "created": int(time.time() * 1000),
        "streak": 0,
        "todayDone": 0,
        "cards": [make_card(*w) for w in WORDS]
    }

    with open("deck.json", "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
