from jinja2 import Template
import os

# Contenu du guide structuré
guide_data = {
    "title": "Guide Complet - Kommz Access",
    "version": "v1.2 (2025)",
    "sections": [
        {
            "id": "intro",
            "title": "🛠 Installation & Configuration",
            "content": """
            <ul>
                <li><strong>Système :</strong> Compatible Windows 10 et 11.</li>
                <li><strong>Pont Audio :</strong> Utilise VB-CABLE pour capturer le son du système sans latence.</li>
                <li><strong>Mode Fantôme :</strong> Activez la superposition pour lire les sous-titres tout en travaillant sur vos logiciels habituels.</li>
            </ul>
            """
        },
        {
            "id": "zero-cloud",
            "title": "🔒 Sécurité & Mode Zéro Cloud",
            "content": """
            <p>Le mode <strong>Zéro Cloud</strong> garantit qu'aucune donnée ne quitte votre ordinateur.</p>
            <ul>
                <li>Traitement local par le processeur (CPU/GPU).</li>
                <li>Conformité RGPD et Secret Médical.</li>
                <li>Fonctionne sans connexion internet après téléchargement des modèles IA.</li>
            </ul>
            """
        },
        {
            "id": "medical",
            "title": "🩺 Focus : Secteur Médical",
            "content": """
            <p>Optimisez la relation patient-praticien :</p>
            <ul>
                <li><strong>Lexique Précis :</strong> Reconnaissance des termes techniques et posologies complexes.</li>
                <li><strong>Lien Visuel :</strong> Le patient lit la transcription en temps réel tout en gardant le contact visuel avec le médecin.</li>
                <li><strong>Résumé Automatique :</strong> Génération d'une fiche de suivi claire à la fin de la consultation.</li>
            </ul>
            """
        },
        {
            "id": "juridique",
            "title": "⚖️ Focus : Droit et Justice",
            "content": """
            <p>Pour les avocats et notaires :</p>
            <ul>
                <li><strong>Fidélité Totale :</strong> Transcription mot à mot des témoignages et auditions.</li>
                <li><strong>Export PDF :</strong> Archivez vos échanges sous format numérique sécurisé.</li>
                <li><strong>Analyse Sémantique :</strong> L'IA aide à détecter les nuances d'intonation (stress, doute).</li>
            </ul>
            """
        }
    ]
}

# Template HTML avec CSS intégré (Tailwind-like style)
html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --primary: #2563eb;
            --dark: #0f172a;
            --light: #f8fafc;
            --accent: #3b82f6;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background-color: var(--light);
            margin: 0;
            padding: 0;
        }
        header {
            background: linear-gradient(135deg, var(--dark) 0%, #1e293b 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-bottom: 4px solid var(--primary);
        }
        .container {
            max-width: 900px;
            margin: -3rem auto 3rem;
            padding: 0 1rem;
        }
        .section-card {
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-left: 5px solid var(--primary);
        }
        h1 { margin: 0; font-size: 2.5rem; }
        h2 { color: var(--primary); border-bottom: 1px solid #e2e8f0; padding-bottom: 0.5rem; }
        .version { opacity: 0.7; font-size: 0.9rem; }
        ul { padding-left: 1.2rem; }
        li { margin-bottom: 0.5rem; }
        footer {
            text-align: center;
            padding: 2rem;
            font-size: 0.8rem;
            color: #64748b;
        }
        @media (max-width: 600px) {
            h1 { font-size: 1.8rem; }
        }
    </style>
</head>
<body>

<header>
    <h1>{{ title }}</h1>
    <p class="version">Version logicielle {{ version }}</p>
</header>

<div class="container">
    {% for section in sections %}
    <div class="section-card" id="{{ section.id }}">
        <h2>{{ section.title }}</h2>
        <div>{{ section.content }}</div>
    </div>
    {% endfor %}
</div>

<footer>
    &copy; 2025 Kommz Innovations. Tous droits réservés. <br>
    Logiciel d'accessibilité universelle.
</footer>

</body>
</html>
"""

def generate_guide():
    # Création du template
    template = Template(html_template)
    
    # Rendu du HTML avec les données
    output_html = template.render(guide_data)
    
    # Écriture du fichier
    file_name = "guide_kommz_access.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print(f"✅ Guide généré avec succès : {os.path.abspath(file_name)}")

if __name__ == "__main__":
    generate_guide()