import pandas as pd
from bs4 import BeautifulSoup

def test_jobs_csv_has_at_least_10_rows():
    df = pd.read_csv("data/jobs.csv")
    assert len(df) >= 10, "jobs.csv contient moins de 10 lignes."

def test_index_html_has_table_and_10_rows():
    with open("public/index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    table = soup.find("table")
    assert table is not None, "Balise <table> non trouvée dans index.html."
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else []
    assert len(rows) >= 10, "Moins de 10 lignes de données dans le tableau HTML."