from flask import Flask, request, jsonify, render_template
from vector_store import VectorStore
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
i2_file_loc = os.path.join(BASE_DIR, 'i2.json')


with open(i2_file_loc, 'r') as f:
    data = json.load(f)
    card_list = [item['card'] for item in data if 'card' in item]

app = Flask(__name__)

# Initialize the vector store
vs = VectorStore()
vs.build_index()

@app.route('/cards', methods=['GET'])
def get_cards():
    return jsonify(card_list)


@app.route('/', methods=['GET'])
@app.route('/index.html')
@app.route('/index')
@app.route('/home')
def home():
    return render_template('index.html')  # This will render templates/index.html

# @app.route('/admin/rebuild', methods=['POST'])
# def rebuild_index():
#     vs.build_index()
#     return jsonify({"message": "Vector database rebuilt successfully."})

# @app.route('/recommend', methods=['POST'])
# def recommend_cards():
#     data = request.get_json()
#     cards = data.get("cards", [])
#     prompt = data.get("prompt", "")

#     if not cards or not prompt:
#         return jsonify({"error": "Missing params"}), 400

#     # recommendations = vs.get_recommendations(cards, prompt)
#     recommendations = vs.r2(cards, prompt)
#     return jsonify(recommendations)


# # Only run locally
# if __name__ == "__main__":
#     app.run(port=int(os.environ.get("PORT", 5000)))