from flask import Flask, render_template, request, jsonify, url_for
import subprocess
import os
import signal
import pandas as pd
import platform
import webbrowser

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-recording')
def start_recording():
    try:
        python_cmd = 'python' if platform.system() == 'Windows' else 'python3'
        script_path = os.path.join(os.path.dirname(__file__), 'main.py')
        subprocess.Popen([python_cmd, script_path],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "Started face recognition (main.py)"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/exit')
def exit_app():
    os.kill(os.getpid(), signal.SIGTERM)
    return "Exiting..."

@app.route('/get-attendance')
def get_attendance():
    date_param = request.args.get('date')
    if not date_param:
        return jsonify({'error': 'No date provided'})

    try:
        date_parts = date_param.split("-")
        formatted_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
        excel_path = os.path.join(os.path.dirname(__file__), "AI_department.xlsx")
        df = pd.read_excel(excel_path)

        if formatted_date not in df.columns:
            return jsonify({'error': f"Date {formatted_date} not found in attendance sheet"})

        records = []
        for _, row in df.iterrows():
            status = "Present" if str(row[formatted_date]).strip() == "✓" else "Absent"
            records.append({
                "roll": row["Roll Number"],
                "name": row["Name"],
                "status": status
            })

        return jsonify({"attendance": records})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get-stats')
def get_stats():
    try:
        excel_path = os.path.join(os.path.dirname(__file__), "AI_department.xlsx")
        df = pd.read_excel(excel_path)

        if "Status" not in df.columns:
            return jsonify({'error': "'Status' column not found in the Excel file."})

        records = []
        for _, row in df.iterrows():
            records.append({
                "roll": row["Roll Number"],
                "name": row["Name"],
                "stats": f"{row['Status']}%"
            })

        return jsonify({"stats": records})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
