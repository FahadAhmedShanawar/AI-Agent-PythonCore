import sqlite3
import os
import pandas as pd
import datetime as dt
import io
import requests
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        steps INTEGER DEFAULT 0,
        calories REAL DEFAULT 0,
        duration_minutes REAL DEFAULT 0,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def add_entry(db_path, date_str, steps, calories, duration):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO entries (date, steps, calories, duration_minutes) VALUES (?, ?, ?, ?)",
              (date_str, int(steps), float(calories), float(duration)))
    conn.commit()
    conn.close()

def get_entries_df(db_path, start=None, end=None):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(
            "SELECT date, steps, calories, duration_minutes FROM entries ORDER BY date ASC",
            conn, parse_dates=["date"]
        )
    finally:
        conn.close()

    # ensure DataFrame has expected columns
    if df is None or df.empty:
        # return empty dataframe with correct columns and dtypes
        return pd.DataFrame(columns=["date", "steps", "calories", "duration_minutes"])

    # normalize date column to date objects and sort
    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.sort_values('date').reset_index(drop=True)

    if start:
        start_date = pd.to_datetime(start).date()
        df = df[df['date'] >= start_date]
    if end:
        end_date = pd.to_datetime(end).date()
        df = df[df['date'] <= end_date]

    # aggregate by date (in case multiple entries per day)
    df = df.groupby('date', as_index=False).sum()
    return df

def summary_stats(df):
    if df is None or df.empty:
        return {
            "daily": {},
            "weekly_steps": 0,
            "monthly_steps": 0,
            "days_recorded": 0,
            "goal_pct": 0
        }
    # ensure df sorted and date type
    df = df.sort_values('date').reset_index(drop=True)
    today = dt.date.today()
    last_7 = df[df['date'] >= (today - dt.timedelta(days=6))]
    last_30 = df[df['date'] >= (today - dt.timedelta(days=29))]
    daily = df[df['date'] == today]
    steps_goal = 10000
    weekly_steps = int(last_7['steps'].sum()) if not last_7.empty else 0
    monthly_steps = int(last_30['steps'].sum()) if not last_30.empty else 0
    days_recorded = int(df.shape[0])
    goal_pct = round((weekly_steps / (steps_goal * 7)) * 100, 1) if steps_goal > 0 else 0
    return {
        "daily": (daily.to_dict(orient="records")[0] if not daily.empty else {}),
        "weekly_steps": weekly_steps,
        "monthly_steps": monthly_steps,
        "days_recorded": days_recorded,
        "goal_pct": goal_pct
    }

def recommend_for_latest(df):
    # simple rule-based recommendations
    recs = []
    if df is None or df.empty:
        recs.append("No data yet — start by adding today's steps and calories.")
        return recs
    # ensure chronological order
    df = df.sort_values('date').reset_index(drop=True)
    last = df.iloc[-1]
    steps_goal = 10000
    calories_goal = 500  # example per-day burned goal, adjust as desired
    steps = int(last.get('steps', 0))
    calories = float(last.get('calories', 0.0))
    if steps >= steps_goal:
        recs.append("🔥 Great job! Maintain or slightly increase your step count tomorrow (e.g., +5%).")
    else:
        # suggest a relative increase (at least +500 or 10% of goal)
        suggested_inc = max(math.ceil(steps * 0.10), 500 - steps if steps < 500 else math.ceil(steps * 0.10))
        recs.append(f"🚶 Increase steps by about {suggested_inc} steps (~10% suggested) tomorrow to improve activity.")
    if calories < calories_goal:
        recs.append("💧 You burned fewer calories today — consider a 20-min jog or higher-intensity 20–30 min workout tomorrow.")
    else:
        recs.append("🔥 Calories burned look good — try mixing in strength training 2x/week.")
    # weekly advice based on recent trend (safe check)
    recent = df['steps'].tail(7)
    if not recent.empty and recent.mean() < steps_goal * 0.8:
        recs.append("📈 Weekly steps are below target — add a 30 min walk 3x this week.")
    return recs

def plot_trends_png(df, out_bytes_io):
    plt.figure(figsize=(8,3.5))
    if df is None or df.empty:
        plt.text(0.5, 0.5, "No data to plot yet", ha='center', va='center')
    else:
        # convert dates for plotting
        dates = pd.to_datetime(df['date'])
        plt.plot(dates, df['steps'], marker='o', label='Steps', color='tab:blue')
        plt.bar(dates, df['calories'], alpha=0.3, label='Calories', color='tab:orange', width=0.6)
        plt.legend()
        plt.xlabel("Date")
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
    plt.savefig(out_bytes_io, format='png')
    plt.close()

def export_csv_bytes(df):
    out = io.StringIO()
    # ensure columns present
    if df is None or df.empty:
        out.write("date,steps,calories,duration_minutes\n")
    else:
        df.to_csv(out, index=False)
    return out.getvalue().encode('utf-8')

def fetch_google_fit_data(db_path, access_token, start_iso=None, end_iso=None):
    """
    Minimal fetch: uses Google Fit aggregate API. The user must supply a valid OAuth2 access token for scope:
    https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.body.read
    This function requests daily aggregation for steps and calories and inserts them into the DB.
    Returns number of daily buckets added.
    """
    # default to last 7 days if no inputs
    try:
        if not end_iso:
            end_dt = pd.to_datetime(dt.date.today())
        else:
            end_dt = pd.to_datetime(end_iso)
        if not start_iso:
            start_dt = end_dt - pd.Timedelta(days=6)
        else:
            start_dt = pd.to_datetime(start_iso)
    except Exception:
        # invalid dates -> use last 7 days
        end_dt = pd.to_datetime(dt.date.today())
        start_dt = end_dt - pd.Timedelta(days=6)

    # normalize to day boundaries
    start_dt = start_dt.floor('D')
    end_dt = end_dt.floor('D')
    start_ms = int(start_dt.timestamp() * 1000)
    # include last day fully
    end_ms = int((end_dt + pd.Timedelta(days=1)).timestamp() * 1000)

    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    body = {
      "aggregateBy": [
        {"dataTypeName": "com.google.step_count.delta"},
        {"dataTypeName": "com.google.calories.expended"}
      ],
      "bucketByTime": {"durationMillis": 24 * 60 * 60 * 1000},
      "startTimeMillis": start_ms,
      "endTimeMillis": end_ms
    }

    added = 0
    try:
        r = requests.post(url, json=body, headers=headers, timeout=30)
        r.raise_for_status()
    except Exception:
        return added

    data = r.json()
    # Parse buckets
    for bucket in data.get("bucket", []):
        start_time_ms = bucket.get("startTimeMillis")
        if start_time_ms is None:
            continue
        try:
            date = dt.date.fromtimestamp(int(start_time_ms) / 1000.0).isoformat()
        except Exception:
            continue
        steps = 0
        calories = 0.0
        for dataset in bucket.get("dataset", []):
            for point in dataset.get("point", []):
                for val in point.get("value", []):
                    if isinstance(val, dict):
                        # prefer intVal for steps, fpVal for calories
                        if "intVal" in val:
                            try:
                                steps += int(val.get("intVal", 0))
                            except Exception:
                                pass
                        if "fpVal" in val:
                            try:
                                calories += float(val.get("fpVal", 0.0))
                            except Exception:
                                pass
        # only add if some data present
        if steps > 0 or calories > 0:
            add_entry(db_path, date, steps, calories, 0.0)
            added += 1
    return added
