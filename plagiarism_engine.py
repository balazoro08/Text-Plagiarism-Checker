import re
import math
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

class PlagiarismEngine:
    def __init__(self):
        # Basic English stop words for cleaning keyword extractions if needed
        self.stop_words = {
            'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
            'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'can\'t', 'cannot',
            'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each',
            'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d',
            'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i',
            'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s',
            'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
            'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll',
            'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs',
            'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve',
            'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll',
            'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while',
            'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d', 'you\'ll',
            'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves'
        }

    def clean_text(self, text: str) -> str:
        """Normalizes whitespace and basic text formatting."""
        if not text:
            return ""
        # Replace multiple whitespaces/newlines with single space
        return re.sub(r'\s+', ' ', text).strip()

    def split_sentences(self, text: str) -> list[str]:
        """Splits text into clean sentences."""
        if not text:
            return []
        # Split by sentence-ending punctuation while preserving abbreviations reasonably
        raw_sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in raw_sentences if s.strip()]
        return sentences if sentences else [text.strip()]

    def compute_tfidf_similarity(self, doc1: str, doc2: str) -> float:
        """Computes global similarity between two documents combining TF-IDF and sequence matching."""
        c1 = self.clean_text(doc1)
        c2 = self.clean_text(doc2)
        
        if not c1 or not c2:
            return 0.0
        
        if c1 == c2:
            return 100.0

        seq_ratio = SequenceMatcher(None, c1.lower(), c2.lower()).ratio()

        try:
            # Word-level TF-IDF
            vectorizer_word = TfidfVectorizer(
                ngram_range=(1, 2),
                lowercase=True
            )
            tfidf_word = vectorizer_word.fit_transform([c1, c2])
            word_sim = float(cosine_similarity(tfidf_word[0:1], tfidf_word[1:2])[0][0])
            
            # Character n-gram TF-IDF (captures partial word matches, root words, stem changes)
            vectorizer_char = TfidfVectorizer(
                analyzer='char_wb',
                ngram_range=(3, 5),
                lowercase=True
            )
            tfidf_char = vectorizer_char.fit_transform([c1, c2])
            char_sim = float(cosine_similarity(tfidf_char[0:1], tfidf_char[1:2])[0][0])

            # Combined hybrid similarity
            hybrid_sim = max(word_sim, char_sim * 0.7 + word_sim * 0.3, seq_ratio * 0.6 + word_sim * 0.4)
            return round(hybrid_sim * 100, 2)
        except Exception:
            return round(seq_ratio * 100, 2)

    def compute_jaccard_similarity(self, str1: str, str2: str) -> float:
        """Computes Jaccard similarity between two token sets."""
        words1 = set(re.findall(r'\b\w+\b', str1.lower()))
        words2 = set(re.findall(r'\b\w+\b', str2.lower()))
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)

    def extract_top_keywords(self, doc1: str, doc2: str, top_n: int = 15) -> list[dict]:
        """Extracts top shared terms and their TF-IDF impact scores."""
        c1, c2 = self.clean_text(doc1), self.clean_text(doc2)
        if not c1 or not c2:
            return []

        try:
            vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([c1, c2]).toarray()
            feature_names = np.array(vectorizer.get_feature_names_out())

            # Combined geometric mean score for term presence in both docs
            scores = np.sqrt(tfidf_matrix[0] * tfidf_matrix[1])
            shared_indices = np.where(scores > 0)[0]

            if len(shared_indices) == 0:
                # Fallback to single doc features if no shared terms found
                scores = (tfidf_matrix[0] + tfidf_matrix[1]) / 2.0
                shared_indices = np.argsort(scores)[::-1][:top_n]

            top_indices = shared_indices[np.argsort(scores[shared_indices])[::-1][:top_n]]

            keywords = []
            for idx in top_indices:
                keywords.append({
                    "term": str(feature_names[idx]),
                    "score": round(float(scores[idx]), 4),
                    "doc1_weight": round(float(tfidf_matrix[0][idx]), 4),
                    "doc2_weight": round(float(tfidf_matrix[1][idx]), 4)
                })
            return keywords
        except Exception:
            return []

    def get_document_stats(self, text: str) -> dict:
        """Calculates linguistic and structural metrics for a document."""
        clean = self.clean_text(text)
        words = re.findall(r'\b\w+\b', clean)
        sentences = self.split_sentences(clean)
        
        total_words = len(words)
        unique_words = len(set(w.lower() for w in words))
        total_chars = len(text)
        sentence_count = len(sentences)

        avg_sentence_len = round(total_words / sentence_count, 1) if sentence_count > 0 else 0
        lexical_richness = round((unique_words / total_words) * 100, 1) if total_words > 0 else 0

        return {
            "char_count": total_chars,
            "word_count": total_words,
            "sentence_count": sentence_count,
            "unique_words": unique_words,
            "avg_sentence_length": avg_sentence_len,
            "lexical_richness": lexical_richness
        }

    def analyze_sentences(self, doc1: str, doc2: str) -> dict:
        """Detailed sentence-by-sentence cross comparison and alignment."""
        s1_list = self.split_sentences(doc1)
        s2_list = self.split_sentences(doc2)

        if not s1_list or not s2_list:
            return {"doc1_sentences": [], "doc2_sentences": [], "summary": {}}

        # Sentence vectorization
        all_sentences = s1_list + s2_list
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        try:
            tfidf_matrix = vectorizer.fit_transform(all_sentences)
            s1_matrix = tfidf_matrix[:len(s1_list)]
            s2_matrix = tfidf_matrix[len(s1_list):]
            sim_matrix = cosine_similarity(s1_matrix, s2_matrix)
        except Exception:
            # Fallback if text contains insufficient vocabulary
            sim_matrix = np.zeros((len(s1_list), len(s2_list)))
            for i, s1 in enumerate(s1_list):
                for j, s2 in enumerate(s2_list):
                    sim_matrix[i][j] = SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

        doc1_matches = []
        doc2_matches = []

        exact_count = 0
        high_count = 0
        moderate_count = 0

        # Process Document 1 Sentences
        for i, s1 in enumerate(s1_list):
            best_match_idx = -1
            best_score = 0.0

            # Find best matching sentence in Document 2
            for j, s2 in enumerate(s2_list):
                cos_sim = float(sim_matrix[i][j])
                # Exact string check
                if s1.strip().lower() == s2.strip().lower():
                    cos_sim = 1.0
                else:
                    # Hybrid score combining Cosine Sim & Sequence Matcher
                    seq_ratio = SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
                    cos_sim = max(cos_sim, seq_ratio)

                if cos_sim > best_score:
                    best_score = cos_sim
                    best_match_idx = j

            sim_pct = round(best_score * 100, 1)

            if sim_pct >= 92.0:
                match_type = "exact"
                exact_count += 1
            elif sim_pct >= 65.0:
                match_type = "high"
                high_count += 1
            elif sim_pct >= 40.0:
                match_type = "moderate"
                moderate_count += 1
            else:
                match_type = "unique"

            doc1_matches.append({
                "id": i,
                "text": s1,
                "best_match_id": best_match_idx if best_match_idx != -1 and best_score >= 0.40 else None,
                "best_match_text": s2_list[best_match_idx] if best_match_idx != -1 and best_score >= 0.40 else "",
                "similarity": sim_pct,
                "match_type": match_type
            })

        # Process Document 2 Sentences for symmetric back-referencing
        for j, s2 in enumerate(s2_list):
            best_match_idx = -1
            best_score = 0.0

            for i, s1 in enumerate(s1_list):
                cos_sim = float(sim_matrix[i][j])
                if s1.strip().lower() == s2.strip().lower():
                    cos_sim = 1.0
                else:
                    seq_ratio = SequenceMatcher(None, s1.lower(), s2.lower()).ratio()
                    cos_sim = max(cos_sim, seq_ratio)

                if cos_sim > best_score:
                    best_score = cos_sim
                    best_match_idx = i

            sim_pct = round(best_score * 100, 1)

            if sim_pct >= 92.0:
                match_type = "exact"
            elif sim_pct >= 65.0:
                match_type = "high"
            elif sim_pct >= 40.0:
                match_type = "moderate"
            else:
                match_type = "unique"

            doc2_matches.append({
                "id": j,
                "text": s2,
                "best_match_id": best_match_idx if best_match_idx != -1 and best_score >= 0.40 else None,
                "best_match_text": s1_list[best_match_idx] if best_match_idx != -1 and best_score >= 0.40 else "",
                "similarity": sim_pct,
                "match_type": match_type
            })

        return {
            "doc1_sentences": doc1_matches,
            "doc2_sentences": doc2_matches,
            "match_counts": {
                "exact": exact_count,
                "high": high_count,
                "moderate": moderate_count,
                "unique": len(s1_list) - (exact_count + high_count + moderate_count)
            }
        }

    def analyze(self, doc1: str, doc2: str) -> dict:
        """Full plagiarism analysis pipeline."""
        overall_similarity = self.compute_tfidf_similarity(doc1, doc2)
        sentence_analysis = self.analyze_sentences(doc1, doc2)
        top_keywords = self.extract_top_keywords(doc1, doc2)
        stats1 = self.get_document_stats(doc1)
        stats2 = self.get_document_stats(doc2)

        # Risk Classification
        if overall_similarity >= 75.0:
            risk_level = "Severe Plagiarism Risk"
            risk_color = "#ef4444"
            risk_badge = "High Plagiarism"
        elif overall_similarity >= 45.0:
            risk_level = "Moderate Plagiarism Risk"
            risk_color = "#f59e0b"
            risk_badge = "Paraphrased Content"
        elif overall_similarity >= 20.0:
            risk_level = "Low Similarity"
            risk_color = "#3b82f6"
            risk_badge = "Minor Overlap"
        else:
            risk_level = "Original Content"
            risk_color = "#10b981"
            risk_badge = "Passed / Original"

        return {
            "overall_similarity": overall_similarity,
            "risk_classification": {
                "level": risk_level,
                "color": risk_color,
                "badge": risk_badge
            },
            "sentence_analysis": sentence_analysis,
            "keywords": top_keywords,
            "document_stats": {
                "doc1": stats1,
                "doc2": stats2
            }
        }

    def compute_similarity_matrix(self, docs: list[dict]) -> dict:
        """Computes similarity matrix across N documents."""
        names = [d.get("name", f"Doc {i+1}") for i, d in enumerate(docs)]
        texts = [self.clean_text(d.get("text", "")) for d in docs]
        
        n = len(texts)
        matrix = [[100.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                score = self.compute_tfidf_similarity(texts[i], texts[j])
                matrix[i][j] = score
                matrix[j][i] = score

        return {
            "labels": names,
            "matrix": matrix
        }
