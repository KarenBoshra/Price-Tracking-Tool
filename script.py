from flask import Flask, request, render_template, jsonify
from datetime import datetime
import csv
from modules.extractor import extract_data, save_to_csv
from modules.text_processing import tag_visible, text_from_html
from modules.generative_model import generate_content
import re

app = Flask(__name__)

def process_extracted_data(extracted_data):
    cleaned_data = extracted_data.replace('"', '').replace(',', '')
    cleaned_data = cleaned_data.lstrip('>')

    match = re.search(r'(?<=product price as a number, and what is the currency\? please separate each answer with a \*\*\*)\d+', cleaned_data)
    if match:
        product_price = match.group()
        product_price = int(product_price.replace(',', ''))
    else:
        product_price = None

    save_to_csv(cleaned_data.split('***'))

    return {'data': cleaned_data, 'product_price': product_price}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form['url']
    try:
        full_text = extract_data(url)
        extracted_data = generate_content(full_text)
        processed_data = process_extracted_data(extracted_data)

        return jsonify(processed_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
