# 🛡️ PlagCheck AI - Text Plagiarism & Similarity Engine

PlagCheck AI is an advanced Text Plagiarism Checker and similarity comparison web application powered by **Python**, **scikit-learn** (`TF-IDF Vectorization`, `Cosine Similarity`), character n-grams, and sentence-level semantic alignment algorithms.

---

## ✨ Features

- **TF-IDF & Cosine Similarity Engine**: Computes high-dimensional document similarity using word and character n-gram vectors.
- **Sentence-Level Alignment**:
  - Classifies matched sentences into **Exact Matches** ($\ge 92\%$), **Paraphrased / High Matches** ($65\% - 91\%$), **Moderate Overlap** ($40\% - 64\%$), and **Original Content**.
- **Interactive Highlighting & Synchronized Viewers**:
  - Side-by-side text viewers with hover synchronization: hovering over a sentence in Document A auto-scrolls to and highlights its matching pair in Document B.
- **Top Shared TF-IDF Keywords**: Identifies key shared domain terms and weight contributions.
- **Document Support**: Drag-and-drop & file upload for `.txt`, `.pdf`, and `.docx` files.
- **Multi-Document Matrix Heatmap**: Batch compare up to 8 documents simultaneously in an $N \times N$ similarity matrix.
- **Linguistic Statistics**: Word count, character count, sentence count, average sentence length, and lexical richness percentage.
- **Export Options**: Save printable PDF reports or raw JSON analysis data.

---

## 📁 Project Structure

```text
├── app.py                 # Flask REST API backend & static file server
├── plagiarism_engine.py   # Core NLP engine (TF-IDF, Cosine Sim, Sentence Alignment)
├── doc_parser.py          # Document parser for TXT, PDF, and DOCX files
├── samples.py             # Pre-configured benchmark test scenarios
├── test_plagiarism.py     # Unit test suite
├── requirements.txt       # Python package dependencies
└── static/
    ├── index.html         # Modern web frontend interface
    ├── css/
    │   └── style.css      # Glassmorphic responsive styling
    └── js/
        └── app.js         # Frontend interactive logic & chart gauge
```

---



---

## 📄 License
MIT License
