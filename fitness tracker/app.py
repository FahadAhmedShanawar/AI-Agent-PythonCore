from flask import Flask, render_template, request, redirect, url_for, send_file, flash, Response
import io, datetime, os, csv
from fitness import init_db, add_entry, get_entries_df, summary_stats, recommend_for_latest, export_csv_bytes, fetch_google_fit_data

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")
DB_PATH = os.path.join(os.path.dirname(__file__), "fitness.db")
init_db(DB_PATH)

@app.route("/", methods=["GET"])
def index():
    # optional date filters from query params
    start = request.args.get("start")
    end = request.args.get("end")
    df = get_entries_df(DB_PATH, start, end)
    summary = summary_stats(df)
    recs = recommend_for_latest(df)
    return render_template("index.html", entries=(df.to_dict(orient="records") if not df.empty else []),
                           summary=summary, recommendations=recs)

@app.route("/add", methods=["POST"])
def add():
    # Accept manual input
    date_str = request.form.get("date") or datetime.date.today().isoformat()
    steps = int(request.form.get("steps") or 0)
    calories = float(request.form.get("calories") or 0.0)
    duration = float(request.form.get("duration") or 0.0)
    add_entry(DB_PATH, date_str, steps, calories, duration)
    flash("Entry added.")
    return redirect(url_for("index"))

@app.route("/plot.png")
def plot_png():
    # Returns PNG bytes for the trend chart
    df = get_entries_df(DB_PATH)
    img_bytes = io.BytesIO()
    from fitness import plot_trends_png
    plot_trends_png(df, img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype="image/png")

@app.route("/export")
def export():
    df = get_entries_df(DB_PATH)
    csv_bytes = export_csv_bytes(df)
    return Response(csv_bytes, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=fitness_export.csv"})

@app.route("/fetch_google_fit", methods=["POST"])
def fetch_google_fit():
    # Minimal helper: user supplies an OAuth2 access token obtained via their own Google Cloud OAuth flow.
    access_token = request.form.get("access_token")
    start = request.form.get("start") or (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
    end = request.form.get("end") or datetime.date.today().isoformat()
    if not access_token:
        flash("Provide an access token to fetch Google Fit data.")
        return redirect(url_for("index"))
    added = fetch_google_fit_data(DB_PATH, access_token, start, end)
    flash(f"Fetched and added {added} data points from Google Fit (if any).")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
