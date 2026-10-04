"""
Pre-configured sample document pairs for demonstration testing.
"""

SAMPLES = {
    "exact_plagiarism": {
        "title": "Exact Plagiarism Example (High Similarity)",
        "description": "Direct copy-paste of text with minor word adjustments.",
        "doc1": (
            "Artificial Intelligence (AI) is transforming modern technology by enabling machines "
            "to process vast datasets, recognize complex patterns, and make autonomous decisions. "
            "Machine learning algorithms form the backbone of modern AI systems, utilizing neural "
            "networks inspired by the human brain. These algorithms continuously improve their "
            "performance as they are exposed to more training data over time. Consequently, "
            "industries such as healthcare, finance, and autonomous transportation are undergoing "
            "unprecedented technological revolutions."
        ),
        "doc2": (
            "Artificial Intelligence (AI) is transforming modern technology by enabling machines "
            "to process vast datasets, recognize complex patterns, and make autonomous decisions. "
            "Machine learning algorithms form the backbone of modern AI systems, utilizing neural "
            "networks inspired by the human brain. These algorithms continuously improve their "
            "performance as they are exposed to more training data over time. Consequently, "
            "industries such as healthcare, finance, and autonomous transportation are undergoing "
            "unprecedented technological revolutions."
        )
    },
    "paraphrased": {
        "title": "Paraphrased Content (Moderate/High Similarity)",
        "description": "Rewritten paragraphs using synonyms and altered sentence structure.",
        "doc1": (
            "Quantum computing relies on quantum bits or qubits, which can exist in multiple states simultaneously "
            "due to the principle of superposition. Unlike classical bits that represent either a zero or a one, "
            "qubits allow quantum computers to process massive quantities of complex information in parallel. "
            "Furthermore, quantum entanglement connects qubits across distance, enabling instantaneous state synchronization. "
            "This capability holds immense promise for cryptography, material science, and drug discovery."
        ),
        "doc2": (
            "Quantum computers operate using qubits rather than conventional binary digits, leveraging the superposition "
            "phenomenon to exist in several states at the same time. While standard bits are restricted to values of 0 or 1, "
            "qubits empower quantum hardware to calculate vast amounts of complicated data concurrently. "
            "In addition, quantum entanglement links qubits regardless of space, permitting immediate state alignment. "
            "As a result, this breakthrough offers revolutionary potential for encryption, molecular research, and pharmaceutical developments."
        )
    },
    "partial_overlap": {
        "title": "Partial Overlap (Low/Moderate Similarity)",
        "description": "Articles sharing common domain terminology but covering different aspects.",
        "doc1": (
            "Global climate change poses severe ecological risks to coastal communities worldwide. Rising sea levels, "
            "driven by thermal expansion and melting polar ice caps, threaten marine habitats and urban infrastructure. "
            "Environmental scientists emphasize the urgent necessity of reducing carbon emissions through renewable energy adoption "
            "and sustainable urban planning initiatives."
        ),
        "doc2": (
            "The transition toward renewable energy technologies such as solar photovoltaic panels and wind turbines "
            "is accelerating globally. Decentralized power grids allow communities to generate clean electricity locally. "
            "Government incentives and falling production costs have made sustainable energy competitive with fossil fuels."
        )
    },
    "unique": {
        "title": "Completely Unique (No Similarity)",
        "description": "Two completely distinct topics with zero content overlap.",
        "doc1": (
            "Classical Greek architecture is celebrated for its harmonious proportions, majestic stone columns, "
            "and enduring influence on Western structural engineering. The Parthenon in Athens demonstrates the Doric order, "
            "featuring unadorned column capitals and meticulously engineered optical illusions."
        ),
        "doc2": (
            "Baking authentic French croissants requires lamination, a technique of repeatedly folding butter into dough. "
            "The yeast-leavened dough must be kept cold between folds to create delicate, crisp, golden-brown layers "
            "with a soft and airy interior."
        )
    }
}
