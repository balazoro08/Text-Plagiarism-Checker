from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from plagiarism_engine import PlagiarismEngine
from doc_parser import DocumentParser
from samples import SAMPLES
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

engine = PlagiarismEngine()

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/api/check', methods=['POST'])
def check_plagiarism():
    data = request.get_json(force=True, silent=True) or {}
    doc1 = data.get('doc1', '').strip()
    doc2 = data.get('doc2', '').strip()

    if not doc1 and not doc2:
        return jsonify({'error': 'Please provide text for both Document 1 and Document 2'}), 400

    if not doc1:
        return jsonify({'error': 'Document 1 is empty'}), 400
    if not doc2:
        return jsonify({'error': 'Document 2 is empty'}), 400

    result = engine.analyze(doc1, doc2)
    return jsonify(result)

@app.route('/api/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        content = file.read()
        extracted_text = DocumentParser.extract_text_from_bytes(content, file.filename)
        return jsonify({
            'filename': file.filename,
            'text': extracted_text,
            'char_count': len(extracted_text),
            'word_count': len(extracted_text.split())
        })
    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

@app.route('/api/samples', methods=['GET'])
def get_samples():
    summary_samples = {}
    for k, v in SAMPLES.items():
        summary_samples[k] = {
            "title": v["title"],
            "description": v["description"]
        }
    return jsonify(summary_samples)

@app.route('/api/samples/<sample_id>', methods=['GET'])
def get_sample_detail(sample_id):
    sample = SAMPLES.get(sample_id)
    if not sample:
        return jsonify({'error': 'Sample not found'}), 404
    return jsonify(sample)

@app.route('/api/matrix', methods=['POST'])
def compute_matrix():
    data = request.get_json(force=True, silent=True) or {}
    docs = data.get('docs', [])
    if len(docs) < 2:
        return jsonify({'error': 'Matrix comparison requires at least 2 documents'}), 400

    result = engine.compute_similarity_matrix(docs)
    return jsonify(result)

if __name__ == '__main__':
    print("Starting Text Plagiarism Checker Server at http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
