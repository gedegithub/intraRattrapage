import pandas as pd
import os

# Lire le CSV
df = pd.read_csv("data/jobs.csv")

# Générer les lignes du tableau HTML
rows = []
for _, row in df.iterrows():
    rows.append(
        f"<tr>"
        f"<td>{row['Titre']}</td>"
        f"<td>{row['Entreprise']}</td>"
        f"<td>{row['Source']}</td>"
        f"<td><a href='{row['Lien']}' target='_blank'>Lien</a></td>"
        f"</tr>"
    )

# HTML complet avec DataTables.js pour tri/recherche
html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Offres d'emploi agrégées</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; background: #fafbfc; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 0.5em; text-align: left; }}
        @media (max-width: 600px) {{
            table, thead, tbody, th, td, tr {{ display: block; }}
            th {{ position: absolute; top: -9999px; left: -9999px; }}
            td {{ border: none; position: relative; padding-left: 50%; }}
            td:before {{
                position: absolute;
                top: 0; left: 0;
                width: 45%;
                white-space: nowrap;
                font-weight: bold;
            }}
            td:nth-of-type(1):before {{ content: "Titre"; }}
            td:nth-of-type(2):before {{ content: "Entreprise"; }}
            td:nth-of-type(3):before {{ content: "Source"; }}
            td:nth-of-type(4):before {{ content: "Lien"; }}
        }}
    </style>
</head>
<body>
    <h1>Offres d'emploi agrégées</h1>
    <table id="jobs">
        <thead>
            <tr>
                <th>Titre</th>
                <th>Entreprise</th>
                <th>Source</th>
                <th>Lien</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function() {{
            $('#jobs').DataTable({{
                responsive: true,
                language: {{
                    search: "Recherche:",
                    lengthMenu: "Afficher _MENU_ offres",
                    info: "Affichage de _START_ à _END_ sur _TOTAL_ offres",
                    paginate: {{
                        first: "Premier",
                        last: "Dernier",
                        next: "Suivant",
                        previous: "Précédent"
                    }},
                    zeroRecords: "Aucune offre trouvée"
                }}
            }});
        }});
    </script>
</body>
</html>
"""

os.makedirs("public", exist_ok=True)
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)