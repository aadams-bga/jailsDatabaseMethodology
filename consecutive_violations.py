import pandas as pd

INFILE = "jail inspection data - logic implemented_dirty_combined_2017_2025.csv"
OUTDIR = "consecutive_violation_tables"

df = pd.read_csv(INFILE, low_memory=False)

category_cols = list(df.columns[22:52])
category_cols = [c for c in category_cols if not str(c).startswith("Unnamed")]

df["year"] = df["year"].astype(str).str.extract(r"(\d{4})").astype(float)
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

df[category_cols] = df[category_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

violated = df[category_cols] > 0

long = (violated
        .assign(name_clean=df["name_clean"], year=df["year"])
        .melt(id_vars=["name_clean", "year"], var_name="category", value_name="violated"))
long = long[long["violated"]]


def longest_consecutive_run(years):
    ys = sorted(set(int(y) for y in years))
    s = pd.Series(ys)
    run_id = (s.diff() != 1).cumsum()
    best_len, best_start, best_end = 0, None, None
    for _, grp in s.groupby(run_id):
        if len(grp) > best_len:
            best_len, best_start, best_end = len(grp), grp.iloc[0], grp.iloc[-1]
    return best_len, best_start, best_end


records = []
for (jail, category), grp in long.groupby(["name_clean", "category"]):
    length, start, end = longest_consecutive_run(grp["year"])
    if length >= 2:
        records.append({
            "name_clean": jail,
            "category": category,
            "max_consecutive_years": length,
            "streak_start": start,
            "streak_end": end,
            "streak_span": f"{start}-{end}",
        })

streaks = (pd.DataFrame(records)
           .sort_values(["max_consecutive_years", "name_clean", "category"],
                        ascending=[False, True, True])
           .reset_index(drop=True))

import os
os.makedirs(OUTDIR, exist_ok=True)

if streaks.empty:
    print("No jail/category had a violation in 2+ consecutive years.")
else:
    streaks.to_csv(os.path.join(OUTDIR, "all_consecutive_streaks.csv"), index=False)
    max_n = int(streaks["max_consecutive_years"].max())
    print(f"Longest streak found: {max_n} consecutive years\n")
    for n in range(2, max_n + 1):
        table = streaks[streaks["max_consecutive_years"] >= n]
        path = os.path.join(OUTDIR, f"consecutive_{n}plus_years.csv")
        table.to_csv(path, index=False)
        print(f"{n}+ consecutive years: {len(table):3d} jail/category pairs  ->  {path}")

    print("\nTop of the master table (all streaks >= 2 years):")
    print(streaks.head(15).to_string(index=False))
