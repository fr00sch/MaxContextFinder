from flask import Flask, send_file
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def results():
    db_path = 'results.db'
    results_data = []
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT date, context_window_size, token_rate, model_name FROM results ORDER BY date DESC")
        results_data = cursor.fetchall()
        conn.close()

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama Context Test Results</title>
    <style>
        body {
            font-family: sans-serif;
            margin: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Ollama Context Test Results</h1>
    <table id="resultsTable">
        <thead>
            <tr>
                <th>Date</th>
                <th>Context Window Size</th>
                <th>Token Rate (tokens/sec)</th>
                <th>Model Name</th>
            </tr>
        </thead>
        <tbody>
    """

    if results_data:
        for row in results_data:
            html_content += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]:.2f}</td>
                <td>{row[3]}</td>
            </tr>
            """
    else:
        html_content += """
            <tr>
                <td colspan="4">No results found yet. Run main.py to generate data.</td>
            </tr>
        """

    html_content += """
        </tbody>
    </table>
</body>
</html
    """
    return html_content

if __name__ == '__main__':
    # Ensure Flask is installed: pip install Flask
    app.run(debug=True)