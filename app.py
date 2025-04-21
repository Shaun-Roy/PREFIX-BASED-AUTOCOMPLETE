import redis 
from flask import Flask, request, jsonify, render_template
import sqlite3
import json
from mistralai import Mistral

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
app = Flask(__name__)

DB_PATH = 'autocomplete.db'

# Setup Mistral API
api_key = "ENTER API KEY HERE"
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

# Set Cache TTL (time-to-live) for Redis cache
CACHE_TTL = 3600  # 1 hour

def get_cached_or_fetch(user_input, needed=5):
    # Check Redis for cached suggestions
    cached_suggestions = r.get(user_input)
    if cached_suggestions:
        print("Cache hit")
        return json.loads(cached_suggestions)

    print("Cache miss, calling Mistral")
    suggestions = get_mistral_suggestions(user_input, needed)

    # Cache the suggestions in Redis with TTL
    r.setex(user_input, CACHE_TTL, json.dumps(suggestions))

    return suggestions

def get_mistral_suggestions(user_input, needed=5):
    prompt = (
f"generate up to {needed} possible completions for the prefix '{user_input}'. MAKE SURE THE COMPLETIONS ARE GRAMMATICALLY CORRECT AND LOGICAL. "
"Respond ONLY with a JSON array of strings like this: "
'["completion 1", "completion 2", ..., "completion n"]\n'
"THE OUTPUTS SHOULD INCLUDE ONLY THE PART OF THE COMPLETION THAT COMES AFTER THE PREFIX. IF THE INPUT IS 'WA' AND THE COMPLETIONS ARE 'was not' OR 'water', "
"THE OUTPUT SHOULD BE 's not' AND 'ter' (WITHOUT INCLUDING 'WA')."
"IF THE COMPLETION IS A CONTINUATION OF THE SAME WORD, DO NOT ADD A SPACE. IF IT IS A NEW WORD, ADD A LEADING SPACE."
"DO NOT include any explanation, formatting, markdown, or extra text. Just return the JSON array."



    )

    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature= 0.2
    )

    raw = response.choices[0].message.content.strip()
    print("Mistral raw output:", raw)  #Debugging line

    try:
        # Fix single quotes to double quotes only if needed
        if raw.startswith("[") and "'" in raw:
            raw = raw.replace("'", '"')

        suggestions = json.loads(raw)
        return suggestions[:needed]

    except Exception as e:
        print("Mistral parse error:", e)
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/autocomplete')
def autocomplete():
    prefix = request.args.get('prefix', '').lower()
    if not prefix:
        return jsonify({'suggestions': [], 'source': 'none'})

    # First, check Redis cache
    cached_suggestions = r.get(prefix)
    if cached_suggestions:
        print("Cache hit")
        return jsonify({'suggestions': json.loads(cached_suggestions), 'source':'redis'})

    # Query SQLite for suggestions
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT ngrams FROM ngrams WHERE ngrams LIKE ? ORDER BY count DESC LIMIT 5"
    cursor.execute(query, (prefix + '%',))
    results = cursor.fetchall()
    conn.close()

    sql_suggestions = [row[0] for row in results]

    # If there are suggestions from SQLite, cache them and return
    if sql_suggestions:
        print("SQL hit")
        r.setex(prefix, CACHE_TTL, json.dumps(sql_suggestions))
        return jsonify({'suggestions': sql_suggestions,'source':'sql'})

    # If fewer than 5 suggestions from SQLite, call Mistral
    print("SQL miss, calling Mistral")
    mistral_suggestions = get_mistral_suggestions(prefix, needed=5)

    # Cache Mistral results for future use
    r.setex(prefix, CACHE_TTL, json.dumps(mistral_suggestions))

    return jsonify({'suggestions': mistral_suggestions,'source':'llm'})




if __name__ == '__main__':
    app.run(debug=True)


