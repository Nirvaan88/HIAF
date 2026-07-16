import pandas as pd

try:
    df = pd.read_excel('Designation.xlsx')
    print("Columns:", df.columns.tolist())
    if 'Job Title' in df.columns:
        titles = sorted(df['Job Title'].dropna().unique().tolist())
        print("Found", len(titles), "titles.")
        import json
        with open('designations.json', 'w', encoding='utf-8') as f:
            json.dump(titles, f)
    else:
        print("Job Title column not found!")
except Exception as e:
    print("Error:", e)
