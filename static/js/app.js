/**
 * PlagCheck AI - Main Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- State Variables ---
    let currentAnalysis = null;
    let currentFilter = 'all';
    let samplePresets = {};

    // --- DOM Elements ---
    const textDoc1 = document.getElementById('text-doc1');
    const textDoc2 = document.getElementById('text-doc2');
    const statsDoc1 = document.getElementById('stats-doc1');
    const statsDoc2 = document.getElementById('stats-doc2');

    const fileInputDoc1 = document.getElementById('file-input-doc1');
    const fileInputDoc2 = document.getElementById('file-input-doc2');

    const dropDoc1 = document.getElementById('drop-doc1');
    const dropDoc2 = document.getElementById('drop-doc2');

    const btnAnalyze = document.getElementById('btn-analyze');
    const btnSwap = document.getElementById('btn-swap');
    const btnResetAll = document.getElementById('btn-reset-all');

    const loader = document.getElementById('analysis-loader');
    const resultsDashboard = document.getElementById('results-dashboard');

    const gaugeFillCircle = document.getElementById('gauge-fill-circle');
    const gaugeVal = document.getElementById('gauge-val');
    const riskBadge = document.getElementById('risk-badge');
    const riskLevelDesc = document.getElementById('risk-level-desc');

    const viewerDoc1 = document.getElementById('viewer-doc1');
    const viewerDoc2 = document.getElementById('viewer-doc2');

    // --- Tab Navigation Setup ---
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const target = btn.dataset.tab;
            document.getElementById(`tab-${target}`).classList.add('active');
        });
    });

    document.querySelectorAll('.dtab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.dtab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.dtab-content').forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const target = btn.dataset.dtab;
            document.getElementById(`dtab-${target}`).classList.add('active');
        });
    });

    // --- Text Count Listeners ---
    function updateCounts() {
        const t1 = textDoc1.value;
        const t2 = textDoc2.value;

        const w1 = t1.trim() ? t1.trim().split(/\s+/).length : 0;
        const c1 = t1.length;
        statsDoc1.textContent = `${w1} words | ${c1} chars`;

        const w2 = t2.trim() ? t2.trim().split(/\s+/).length : 0;
        const c2 = t2.length;
        statsDoc2.textContent = `${w2} words | ${c2} chars`;
    }

    textDoc1.addEventListener('input', updateCounts);
    textDoc2.addEventListener('input', updateCounts);

    // --- Clear & Swap Actions ---
    document.getElementById('clear-doc1').addEventListener('click', () => {
        textDoc1.value = '';
        updateCounts();
    });

    document.getElementById('clear-doc2').addEventListener('click', () => {
        textDoc2.value = '';
        updateCounts();
    });

    btnSwap.addEventListener('click', () => {
        const temp = textDoc1.value;
        textDoc1.value = textDoc2.value;
        textDoc2.value = temp;
        updateCounts();
    });

    btnResetAll.addEventListener('click', () => {
        textDoc1.value = '';
        textDoc2.value = '';
        updateCounts();
        resultsDashboard.classList.add('hidden');
    });

    // --- File Upload & Drag-and-Drop ---
    function handleFileUpload(file, targetDocArea) {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(`Upload error: ${data.error}`);
            } else {
                targetDocArea.value = data.text;
                updateCounts();
            }
        })
        .catch(err => {
            alert(`Failed to parse document file: ${err.message}`);
        });
    }

    fileInputDoc1.addEventListener('change', (e) => handleFileUpload(e.target.files[0], textDoc1));
    fileInputDoc2.addEventListener('change', (e) => handleFileUpload(e.target.files[0], textDoc2));

    // Setup Drag and Drop
    [
        { area: textDoc1.parentElement, target: textDoc1 },
        { area: textDoc2.parentElement, target: textDoc2 }
    ].forEach(item => {
        item.area.addEventListener('dragover', (e) => {
            e.preventDefault();
            item.area.classList.add('dragover');
        });

        item.area.addEventListener('dragleave', () => {
            item.area.classList.remove('dragover');
        });

        item.area.addEventListener('drop', (e) => {
            e.preventDefault();
            item.area.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                handleFileUpload(e.dataTransfer.files[0], item.target);
            }
        });
    });

    // --- Preset Samples Loader ---
    function fetchPresets() {
        fetch('/api/samples')
            .then(res => res.json())
            .then(data => {
                samplePresets = data;
                renderPresetButtons(data);
                renderPresetCards(data);
            });
    }

    function loadSample(key) {
        fetch(`/api/samples/${key}`)
            .then(res => res.json())
            .then(sample => {
                textDoc1.value = sample.doc1;
                textDoc2.value = sample.doc2;
                updateCounts();
                runAnalysis();
            });
    }

    function renderPresetButtons(samples) {
        const container = document.getElementById('quick-sample-buttons');
        container.innerHTML = '';
        Object.keys(samples).forEach(key => {
            const btn = document.createElement('button');
            btn.className = 'btn-sample';
            btn.textContent = samples[key].title.split('(')[0].trim();
            btn.addEventListener('click', () => loadSample(key));
            container.appendChild(btn);
        });
    }

    function renderPresetCards(samples) {
        const grid = document.getElementById('presets-cards-grid');
        grid.innerHTML = '';
        Object.keys(samples).forEach(key => {
            const card = document.createElement('div');
            card.className = 'preset-card';
            card.innerHTML = `
                <div>
                    <h3>${samples[key].title}</h3>
                    <p>${samples[key].description}</p>
                </div>
                <button class="btn-primary" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
                    Load Test Scenario <i class="fa-solid fa-arrow-right"></i>
                </button>
            `;
            card.addEventListener('click', () => {
                loadSample(key);
                document.querySelector('.nav-btn[data-tab="single-cmp"]').click();
            });
            grid.appendChild(card);
        });
    }

    // --- Main Plagiarism Analysis ---
    function runAnalysis() {
        const d1 = textDoc1.value.trim();
        const d2 = textDoc2.value.trim();

        if (!d1 || !d2) {
            alert('Please insert or upload text for both Document A and Document B before running analysis.');
            return;
        }

        resultsDashboard.classList.add('hidden');
        loader.classList.remove('hidden');

        fetch('/api/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ doc1: d1, doc2: d2 })
        })
        .then(res => res.json())
        .then(data => {
            loader.classList.add('hidden');
            if (data.error) {
                alert(`Analysis Error: ${data.error}`);
            } else {
                currentAnalysis = data;
                renderResults(data);
                resultsDashboard.classList.remove('hidden');
                resultsDashboard.scrollIntoView({ behavior: 'smooth' });
            }
        })
        .catch(err => {
            loader.classList.add('hidden');
            alert(`Analysis failed: ${err.message}`);
        });
    }

    btnAnalyze.addEventListener('click', runAnalysis);

    // --- Render Dashboard Output ---
    function renderResults(data) {
        // 1. Radial Gauge Animation
        const score = data.overall_similarity;
        gaugeVal.textContent = `${score.toFixed(1)}%`;

        const circumference = 427; // 2 * PI * 68
        const offset = circumference - (score / 100) * circumference;
        gaugeFillCircle.style.strokeDashoffset = offset;

        // Risk Classification styling
        const risk = data.risk_classification;
        riskBadge.textContent = risk.badge;
        riskBadge.style.backgroundColor = `${risk.color}25`;
        riskBadge.style.color = risk.color;

        gaugeFillCircle.style.stroke = risk.color;
        riskLevelDesc.textContent = risk.level;

        // 2. Metrics Breakdown
        const counts = data.sentence_analysis.match_counts;
        document.getElementById('metric-exact-count').textContent = counts.exact;
        document.getElementById('metric-paraphrase-count').textContent = counts.high;
        document.getElementById('metric-moderate-count').textContent = counts.moderate;
        document.getElementById('metric-unique-count').textContent = counts.unique;

        // 3. Render Sentence Highlighting View
        renderSentenceHighlighting(data.sentence_analysis);

        // 4. Render Keywords View
        renderKeywords(data.keywords);

        // 5. Render Sentence Pair Table
        renderSentenceTable(data.sentence_analysis);

        // 6. Render Document Statistics
        renderDocumentStats(data.document_stats);
    }

    // --- Sentence Highlighting & Synchronized Hovering ---
    function renderSentenceHighlighting(sentenceAnalysis) {
        const s1List = sentenceAnalysis.doc1_sentences;
        const s2List = sentenceAnalysis.doc2_sentences;

        viewerDoc1.innerHTML = '';
        viewerDoc2.innerHTML = '';

        s1List.forEach(s => {
            const span = document.createElement('span');
            span.className = `hl-sent ${s.match_type}`;
            span.textContent = s.text + ' ';
            span.dataset.sentId = `doc1-${s.id}`;
            span.dataset.matchId = s.best_match_id !== null ? `doc2-${s.best_match_id}` : '';
            span.dataset.matchType = s.match_type;
            span.title = s.match_type !== 'unique' ? `Match Similarity: ${s.similarity}%` : 'Unique Sentence';

            viewerDoc1.appendChild(span);
        });

        s2List.forEach(s => {
            const span = document.createElement('span');
            span.className = `hl-sent ${s.match_type}`;
            span.textContent = s.text + ' ';
            span.dataset.sentId = `doc2-${s.id}`;
            span.dataset.matchId = s.best_match_id !== null ? `doc1-${s.best_match_id}` : '';
            span.dataset.matchType = s.match_type;
            span.title = s.match_type !== 'unique' ? `Match Similarity: ${s.similarity}%` : 'Unique Sentence';

            viewerDoc2.appendChild(span);
        });

        // Add synchronized hover listeners
        document.querySelectorAll('.hl-sent').forEach(el => {
            el.addEventListener('mouseenter', () => {
                const targetId = el.dataset.matchId;
                if (!targetId) return;

                el.classList.add('active-hover');
                const targetEl = document.querySelector(`[data-sent-id="${targetId}"]`);
                if (targetEl) {
                    targetEl.classList.add('active-hover');
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });

            el.addEventListener('mouseleave', () => {
                document.querySelectorAll('.hl-sent').forEach(s => s.classList.remove('active-hover'));
            });
        });
    }

    // Filter Highlight Listener
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;
            currentFilter = filter;

            document.querySelectorAll('.hl-sent').forEach(span => {
                const mType = span.dataset.matchType;
                if (filter === 'all') {
                    span.style.opacity = '1';
                } else if (filter === mType) {
                    span.style.opacity = '1';
                } else {
                    span.style.opacity = '0.35';
                }
            });
        });
    });

    // --- Render Top Keywords ---
    function renderKeywords(keywords) {
        const container = document.getElementById('keywords-container');
        container.innerHTML = '';

        if (!keywords || keywords.length === 0) {
            container.innerHTML = '<p style="color: var(--text-muted)">No shared keywords detected.</p>';
            return;
        }

        const maxScore = Math.max(...keywords.map(k => k.score)) || 1.0;

        keywords.forEach(kw => {
            const pct = Math.round((kw.score / maxScore) * 100);
            const card = document.createElement('div');
            card.className = 'kw-card';
            card.innerHTML = `
                <div class="kw-term">${kw.term}</div>
                <div class="kw-bar-bg">
                    <div class="kw-bar-fill" style="width: ${pct}%"></div>
                </div>
                <div class="kw-scores">
                    <span>TF-IDF Score: ${kw.score}</span>
                    <span>Shared Term</span>
                </div>
            `;
            container.appendChild(card);
        });
    }

    // --- Render Sentence Pair Table ---
    function renderSentenceTable(sentenceAnalysis) {
        const tbody = document.getElementById('sentence-table-body');
        tbody.innerHTML = '';

        const s1List = sentenceAnalysis.doc1_sentences;

        s1List.forEach((s, idx) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${idx + 1}</td>
                <td>${s.text}</td>
                <td>${s.best_match_text || '<em>No close match found</em>'}</td>
                <td><strong>${s.similarity}%</strong></td>
                <td><span class="type-pill ${s.match_type}">${s.match_type}</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    // --- Render Document Statistics ---
    function renderDocumentStats(stats) {
        const tbody = document.getElementById('stats-table-body');
        tbody.innerHTML = '';

        const s1 = stats.doc1;
        const s2 = stats.doc2;

        const metrics = [
            { label: 'Total Words', key: 'word_count' },
            { label: 'Total Characters', key: 'char_count' },
            { label: 'Sentence Count', key: 'sentence_count' },
            { label: 'Unique Vocabulary', key: 'unique_words' },
            { label: 'Avg Sentence Length (words)', key: 'avg_sentence_length' },
            { label: 'Lexical Richness (%)', key: 'lexical_richness' }
        ];

        metrics.forEach(m => {
            const v1 = s1[m.key];
            const v2 = s2[m.key];
            const diff = typeof v1 === 'number' ? (v1 - v2).toFixed(1) : '-';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${m.label}</strong></td>
                <td>${v1}</td>
                <td>${v2}</td>
                <td>${diff}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    // --- Multi-Document Matrix Pane Setup ---
    const matrixDocList = document.getElementById('matrix-doc-list');
    let matrixDocCount = 0;

    function addMatrixDocRow(name = '', text = '') {
        matrixDocCount++;
        const id = matrixDocCount;
        const row = document.createElement('div');
        row.className = 'matrix-doc-row';
        row.id = `matrix-row-${id}`;
        row.innerHTML = `
            <input type="text" value="${name || 'Doc ' + id}" placeholder="Doc Name" class="matrix-doc-name">
            <textarea placeholder="Paste document content here..." class="matrix-doc-text">${text}</textarea>
            <button class="btn-icon" onclick="document.getElementById('matrix-row-${id}').remove()"><i class="fa-solid fa-trash"></i></button>
        `;
        matrixDocList.appendChild(row);
    }

    // Initial 3 rows
    addMatrixDocRow('Doc 1 (Artificial Intelligence)', 'Artificial Intelligence is enabling machines to process data and make decisions.');
    addMatrixDocRow('Doc 2 (Machine Learning)', 'Machine learning algorithms enable computers to process vast data automatically.');
    addMatrixDocRow('Doc 3 (Ancient Architecture)', 'Classical Greek architecture is celebrated for stone columns and Parthenon symmetry.');

    document.getElementById('btn-add-matrix-doc').addEventListener('click', () => addMatrixDocRow());

    document.getElementById('btn-run-matrix').addEventListener('click', () => {
        const rows = document.querySelectorAll('.matrix-doc-row');
        const docs = [];
        rows.forEach(r => {
            const name = r.querySelector('.matrix-doc-name').value.trim();
            const text = r.querySelector('.matrix-doc-text').value.trim();
            if (name && text) {
                docs.push({ name, text });
            }
        });

        if (docs.length < 2) {
            alert('Please provide text for at least 2 documents.');
            return;
        }

        fetch('/api/matrix', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ docs })
        })
        .then(res => res.json())
        .then(data => {
            renderMatrixTable(data);
        });
    });

    function renderMatrixTable(matrixData) {
        const table = document.getElementById('matrix-table');
        table.innerHTML = '';

        const labels = matrixData.labels;
        const matrix = matrixData.matrix;

        // Header
        const thead = document.createElement('thead');
        let headerRow = '<tr><th>Doc Name</th>';
        labels.forEach(l => headerRow += `<th>${l}</th>`);
        headerRow += '</tr>';
        thead.innerHTML = headerRow;
        table.appendChild(thead);

        // Body
        const tbody = document.createElement('tbody');
        matrix.forEach((row, i) => {
            let tr = `<tr><td><strong>${labels[i]}</strong></td>`;
            row.forEach((val, j) => {
                let bg = 'rgba(16, 185, 129, 0.15)';
                if (val >= 75) bg = 'rgba(239, 68, 68, 0.4)';
                else if (val >= 45) bg = 'rgba(245, 158, 11, 0.3)';
                else if (val >= 20) bg = 'rgba(59, 130, 246, 0.2)';

                tr += `<td style="background: ${bg}">${val.toFixed(1)}%</td>`;
            });
            tr += '</tr>';
            tbody.innerHTML += tr;
        });
        table.appendChild(tbody);

        document.getElementById('matrix-results-area').classList.remove('hidden');
    }

    // --- Export Options ---
    document.getElementById('btn-export-json').addEventListener('click', () => {
        if (!currentAnalysis) return;
        const blob = new Blob([JSON.stringify(currentAnalysis, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `plagiarism_report_${Date.now()}.json`;
        a.click();
    });

    document.getElementById('btn-export-pdf').addEventListener('click', () => {
        window.print();
    });

    // Initial load
    fetchPresets();
});
