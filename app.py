# app.py
# Long Beach Demographic Dashboard (Excel-backed)

import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget

LB2023_XLSX          = "Long Beach 2023 Estimates - Copy.xlsx"
RACE_BY_YEAR_XLSX    = "Long Beach race by year US Estimates - Copy.xlsx"
RACE_ETH_2023_XLSX   = "Long Beach gen and total US Estimates - Copy.xlsx"
ZIP_YEAR_XLSX        = "Long Beach zip and year Estimates - Copy.xlsx"
ZIP_GENDER_AGE_XLSX  = "Long Beach zip gender year Estimates - Copy.xlsx"

def load_population_trend():
    """
    Sheet: Long Beach (2023)
    Header row: 98 (Year | Total | Male | Female)
    13 rows for 2011–2023
    """
    try:
        df = pd.read_excel(
            LB2023_XLSX,
            sheet_name="Long Beach (2023)",
            header=98,
            nrows=13,
            usecols=[0, 1],  # Year, Total
        ).dropna()
        df["Year"] = df["Year"].astype(int)
        df["Total"] = pd.to_numeric(df["Total"]).astype(int)
        return df
    except Exception as e:
        print("load_population_trend:", e)
        return pd.DataFrame(columns=["Year", "Total"])


def load_zip_population_2023():
    """
    Sheet: Long Beach (2023)
    Header row: 113 (Zip Code | LB 2023)
    11 ZIP rows (+ sometimes a total row—drop it)
    """
    try:
        df = pd.read_excel(
            LB2023_XLSX,
            sheet_name="Long Beach (2023)",
            header=113,
            nrows=12,
            usecols=[0, 1],
        ).dropna()
        df.columns = ["ZIP Code", "Population"]
        zips = df["ZIP Code"].astype(str).str.extract(r"(\d{5})")[0]
        df = df[zips.notna()].copy()
        df["ZIP Code"] = "ZIP " + zips
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
        df = df.dropna()
        return df
    except Exception as e:
        print("load_zip_population_2023:", e)
        return pd.DataFrame(columns=["ZIP Code", "Population"])


def load_population_pyramid_2023():
    """
    Sheet: Long Beach (2023)
    Header row: 50 (Age Group | Male | Female | Total)
    Drop the 'Total' summary row. Make male negative for a population pyramid.
    """
    try:
        df = pd.read_excel(
            LB2023_XLSX,
            sheet_name="Long Beach (2023)",
            header=50,
            usecols=[0, 1, 2],
            nrows=20,  
        )
        df.columns = ["Age Group", "Male", "Female"]
        df = df[df["Age Group"].astype(str).str.lower() != "total"].copy()
        df["Age Group"] = df["Age Group"].astype(str).str.strip()
        df["Male"] = pd.to_numeric(df["Male"], errors="coerce") * -1
        df["Female"] = pd.to_numeric(df["Female"], errors="coerce")
        out = df.melt(
            id_vars="Age Group",
            value_vars=["Male", "Female"],
            var_name="Gender",
            value_name="Population",
        ).dropna()
        return out
    except Exception as e:
        print("load_population_pyramid_2023:", e)
        return pd.DataFrame(columns=["Age Group", "Gender", "Population"])


def load_age_group_trends():
    """
    Sheet: Long Beach (2023)
    Header row: 14 (Age Cat1 | LB 2023 | LB 2022 | LB 2021 | LB 2020 | LB 2019)
    """
    try:
        df = pd.read_excel(
            LB2023_XLSX,
            sheet_name="Long Beach (2023)",
            header=14,
            nrows=8,
        )
        df = df[
            ["Age Cat1", "LB 2023", "LB 2022", "LB 2021", "LB 2020", "LB 2019"]
        ].copy()
        df.columns = ["Age Group", "2023", "2022", "2021", "2020", "2019"]
        out = df.melt(
            id_vars="Age Group", var_name="Year", value_name="Population"
        )
        out["Population"] = pd.to_numeric(out["Population"], errors="coerce")
        out = out.dropna()
        return out
    except Exception as e:
        print("load_age_group_trends:", e)
        return pd.DataFrame(columns=["Age Group", "Year", "Population"])


def load_race_2023():
    """
    Sheet: Race_Ethnicity (2023)
    TOTAL row at absolute row index 40 (0-based in pandas after header=None).
    Columns 1..5 are: Hispanic, White, Asian, Black, NHPI.
    """
    try:
        base = pd.read_excel(
            RACE_ETH_2023_XLSX,
            sheet_name="Race_Ethnicity (2023)",
            header=None,
        )
        totals = base.iloc[40, 1:6].tolist() 
        labels = [
            "Hispanic or Latino",
            "White (Not Hispanic)",
            "Asian (Not Hispanic)",
            "Black (Not Hispanic)",
            "NHPI (Not Hispanic)",
        ]
        df = pd.DataFrame({"Race/Ethnicity": labels, "Population": totals})
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
        return df.dropna()
    except Exception as e:
        print("load_race_2023:", e)
        return pd.DataFrame(columns=["Race/Ethnicity", "Population"])


def load_race_trends():
    """
    Sheet: RACE BY YEAR
    Totals row for each race is at absolute row index 2 (header=None).
    Blocks by columns:
      Hispanic: 1..7, White: 9..15, Asian: 17..23, Black: 25..31
    """
    try:
        row = pd.read_excel(
            RACE_BY_YEAR_XLSX, sheet_name="RACE BY YEAR", header=None
        ).iloc[2]
        years = [str(y) for y in range(2017, 2024)]
        blocks = {
            "Hispanic": row[1:8].tolist(),
            "White": row[9:16].tolist(),
            "Asian": row[17:24].tolist(),
            "Black": row[25:32].tolist(),
        }
        out = []
        for race, vals in blocks.items():
            for y, v in zip(years, vals):
                out.append({"Year": y, "Race/Ethnicity": race, "Population": v})
        df = pd.DataFrame(out)
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
        return df.dropna()
    except Exception as e:
        print("load_race_trends:", e)
        return pd.DataFrame(columns=["Year", "Race/Ethnicity", "Population"])


def load_race_age_dist_2023():
    """
    Sheet: Race_Ethnicity (2023)
    Compact Age x Race block starts at absolute row 58 (no header).
    5 rows of ages, columns: Age | Hispanic | White | Asian | Black
    """
    try:
        df = pd.read_excel(
            RACE_ETH_2023_XLSX,
            sheet_name="Race_Ethnicity (2023)",
            header=None,
            skiprows=58,
            nrows=5,
            usecols=[0, 1, 2, 3, 4],
        )
        df.columns = ["Age Group", "Hispanic", "White", "Asian", "Black"]
        melted = df.melt(
            id_vars="Age Group",
            var_name="Race/Ethnicity",
            value_name="Population",
        )
        melted["Population"] = pd.to_numeric(melted["Population"], errors="coerce")
        return melted.dropna()
    except Exception as e:
        print("load_race_age_dist_2023:", e)
        return pd.DataFrame(columns=["Age Group", "Race/Ethnicity", "Population"])


def load_race_gender_2023():
    """
    Sheet: Race_Ethnicity (2023)
    Male TOTAL row at 83, Female TOTAL row at 93 (header=None).
    Columns 1..5 map to: Hispanic, White, Asian, Black, NHPI.
    """
    try:
        base = pd.read_excel(
            RACE_ETH_2023_XLSX, sheet_name="Race_Ethnicity (2023)", header=None
        )
        male = base.iloc[83, 1:6].tolist()
        female = base.iloc[93, 1:6].tolist()
        races = ["Hispanic", "White", "Asian", "Black", "NHPI"]
        df_m = pd.DataFrame(
            {"Race/Ethnicity": races, "Gender": "Male", "Population": male}
        )
        df_f = pd.DataFrame(
            {"Race/Ethnicity": races, "Gender": "Female", "Population": female}
        )
        df = pd.concat([df_m, df_f], ignore_index=True)
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
        return df.dropna()
    except Exception as e:
        print("load_race_gender_2023:", e)
        return pd.DataFrame(columns=["Race/Ethnicity", "Gender", "Population"])


def load_zip_trends():
    """
    Sheet: Zip and Year
    Year blocks begin at these absolute row indices (header=None):
      2016:2, 2017:40, 2018:77, 2019:115, 2020:153, 2021:191, 2022:229, 2023:266
    For each block: header with zips at start+2; 'Total' row holds the counts.
    """
    try:
        raw = pd.read_excel(ZIP_YEAR_XLSX, sheet_name="Zip and Year", header=None)
        year_rows = {
            2016: 2,
            2017: 40,
            2018: 77,
            2019: 115,
            2020: 153,
            2021: 191,
            2022: 229,
            2023: 266,
        }
        out = []
        for year, start in year_rows.items():
            zips = raw.iloc[start + 2, 1:12].astype(str).tolist()
            block = raw.iloc[start : start + 25, :]
            total_rel_idx = block[0].astype(str).str.fullmatch("Total", na=False)
            if not total_rel_idx.any():
                continue
            total_row = block[total_rel_idx].index[0]
            vals = raw.iloc[total_row, 1:12].tolist()
            for z, v in zip(zips, vals):
                if re.fullmatch(r"\d{5}", str(z)):
                    out.append({"ZIP Code": f"ZIP {z}", "Population": v, "Year": year})
        df = pd.DataFrame(out)
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
        return df.dropna()
    except Exception as e:
        print("load_zip_trends:", e)
        return pd.DataFrame(columns=["ZIP Code", "Population", "Year"])


def load_zip_age_dist_2023():
    """
    Sheet: Zip, Gender, Age by Year
    Find the 'Year 2023' marker, then for each ZIP take its 'Total' column
    across the standard age rows.
    """
    try:
        raw = pd.read_excel(
            ZIP_GENDER_AGE_XLSX, sheet_name="Zip, Gender, Age by Year", header=None
        )

        year_mask = raw[0].astype(str).str.contains("Year 2023", na=False)
        if not year_mask.any():
            return pd.DataFrame(columns=["Age Group", "ZIP Code", "Population"])
        start = year_mask[year_mask].index[0]

        header_row = start + 2  
        zip_row = start + 1     

        cols = []
        for c in range(raw.shape[1]):
            if str(raw.iloc[header_row, c]).strip().lower() == "total":
                z = str(raw.iloc[zip_row, c]).strip()
                if re.fullmatch(r"\d{5}", z):
                    cols.append((f"ZIP {z}", c))

        ages = []
        r = start + 4
        while (
            r < raw.shape[0]
            and isinstance(raw.iloc[r, 0], str)
            and raw.iloc[r, 0].strip()
        ):
            ages.append((raw.iloc[r, 0].strip(), r))
            r += 1

        out = []
        for age_label, rr in ages:
            for zip_lbl, cc in cols:
                out.append(
                    {
                        "Age Group": age_label,
                        "ZIP Code": zip_lbl,
                        "Population": raw.iloc[rr, cc],
                    }
                )
        df = pd.DataFrame(out)
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
        return df.dropna()
    except Exception as e:
        print("load_zip_age_dist_2023:", e)
        return pd.DataFrame(columns=["Age Group", "ZIP Code", "Population"])


ZIP_CODES_LABEL = [
    "ZIP 90802",
    "ZIP 90803",
    "ZIP 90804",
    "ZIP 90805",
    "ZIP 90806",
    "ZIP 90807",
    "ZIP 90808",
    "ZIP 90810",
    "ZIP 90813",
    "ZIP 90814",
    "ZIP 90815",
]

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Summary Overview",
        ui.tags.h2("Summary Overview (2023)"),
        ui.layout_columns(
            ui.value_box("Total Population", "458,491", theme="primary"),
            ui.value_box("Male Population", "226,934"),
            ui.value_box("Female Population", "231,557"),
            ui.value_box("Largest Age Group", "20-44 (174,952)"),
        ),
        ui.layout_columns(
            output_widget("summary_pop_trend"),
            output_widget("summary_race_pie"),
        ),
        ui.layout_columns(
            output_widget("summary_zip_bar"),
        ),
    ),
    ui.nav_panel(
        "Age & Gender Deep Dive",
        ui.tags.h2("Age & Gender Deep Dive (2023)"),
        ui.layout_columns(
            output_widget("age_population_pyramid"),
            output_widget("age_group_trends"),
        ),
    ),
    ui.nav_panel(
        "Race & Ethnicity Deep Dive",
        ui.tags.h2("Race & Ethnicity Deep Dive"),
        ui.layout_columns(
            output_widget("race_pop_trends"),
        ),
        ui.layout_columns(
            output_widget("race_age_dist"),
            output_widget("race_gender_dist"),
        ),
    ),
    ui.nav_panel(
        "Geographic Deep Dive",
        ui.tags.h2("Geographic Deep Dive (ZIP Code)"),
        ui.layout_columns(
            output_widget("geo_zip_bar_rank"),
        ),
        ui.layout_columns(
            ui.card(
                ui.tags.h4("Population Trends by ZIP Code (2016–2023)"),
                ui.input_selectize(
                    "zip_select",
                    "Select ZIP Codes:",
                    choices=ZIP_CODES_LABEL,
                    selected=["ZIP 90805", "ZIP 90814"],
                    multiple=True,
                ),
                output_widget("geo_zip_trends"),
            ),
            output_widget("geo_zip_age_dist"),
        ),
    ),
    title="Long Beach Demographic Dashboard",
    footer=ui.tags.p(
        "Data sourced from 2023 ACS 5-Year Estimates Excel workbooks.",
        style="text-align: center; margin-top: 20px;",
    ),
)


def server(input, output, session):
    @reactive.Calc
    def df_trend():
        return load_population_trend()

    @reactive.Calc
    def df_race_2023():
        return load_race_2023()

    @reactive.Calc
    def df_zip_2023():
        return load_zip_population_2023()

    @reactive.Calc
    def df_pyramid_2023():
        return load_population_pyramid_2023()

    @reactive.Calc
    def df_age_trends():
        return load_age_group_trends()

    @reactive.Calc
    def df_race_trends():
        return load_race_trends()

    @reactive.Calc
    def df_race_age_dist():
        return load_race_age_dist_2023()

    @reactive.Calc
    def df_race_gender_dist():
        return load_race_gender_2023()

    @reactive.Calc
    def df_zip_trends():
        return load_zip_trends()

    @reactive.Calc
    def df_zip_age_dist():
        return load_zip_age_dist_2023()

    @output
    @render_widget
    def summary_pop_trend():
        d = df_trend()
        if d.empty:
            return go.Figure().update_layout(title="Long Beach Population Trend (no data)")
        fig = px.line(d, x="Year", y="Total", title="Long Beach Population Trend (2011–2023)", markers=True)
        fig.update_layout(yaxis_title="Total Population")
        return fig

    @output
    @render_widget
    def summary_race_pie():
        d = df_race_2023()
        if d.empty:
            return go.Figure().update_layout(title="2023 Race/Ethnicity Breakdown (no data)")
        fig = px.pie(d, names="Race/Ethnicity", values="Population", title="2023 Race/Ethnicity Breakdown", hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        return fig

    @output
    @render_widget
    def summary_zip_bar():
        d = df_zip_2023()
        if d.empty:
            return go.Figure().update_layout(title="Population by ZIP Code (2023) — no data")
        d = d.sort_values("Population", ascending=True)
        return px.bar(d, x="Population", y="ZIP Code", title="Population by ZIP Code (2023)", orientation="h")

    @output
    @render_widget
    def age_population_pyramid():
        d = df_pyramid_2023()
        if d.empty:
            return go.Figure().update_layout(title="Population Pyramid (2023) — no data")

        ages = list(d["Age Group"].unique())
        fig = go.Figure()
        for gender in ["Male", "Female"]:
            g = d[d["Gender"] == gender]
            fig.add_trace(go.Bar(y=g["Age Group"], x=g["Population"], name=gender, orientation="h"))

        max_abs = int(abs(d["Population"]).max()) if len(d) else 0
        step = max(1, max_abs // 5) if max_abs else 1
        ticks = list(range(-max_abs, max_abs + 1, step)) if max_abs else [-1, 0, 1]

        fig.update_layout(
            title="Population Pyramid (2023)",
            barmode="relative",
            yaxis=dict(title="Age Group", categoryorder="array", categoryarray=ages),
            xaxis=dict(title="Population", tickvals=ticks, ticktext=[f"{abs(t):,}" for t in ticks]),
            bargap=0.1,
            legend_title_text="Gender",
        )
        return fig

    @output
    @render_widget
    def age_group_trends():
        d = df_age_trends()
        if d.empty:
            return go.Figure().update_layout(title="Population Change by Age Group (2019–2023) — no data")
        fig = px.area(d, x="Year", y="Population", color="Age Group", title="Population Change by Age Group (2019–2023)")
        return fig

    @output
    @render_widget
    def race_pop_trends():
        d = df_race_trends()
        if d.empty:
            return go.Figure().update_layout(title="Population Trends by Race/Ethnicity (2017–2023) — no data")
        fig = px.line(d, x="Year", y="Population", color="Race/Ethnicity", title="Population Trends by Race/Ethnicity (2017–2023)", markers=True)
        return fig

    @output
    @render_widget
    def race_age_dist():
        d = df_race_age_dist()
        if d.empty:
            return go.Figure().update_layout(title="Age Distribution by Race/Ethnicity (2023) — no data")
        fig = px.bar(d, x="Race/Ethnicity", y="Population", color="Age Group", title="Age Distribution by Race/Ethnicity (2023)", barmode="stack")
        return fig

    @output
    @render_widget
    def race_gender_dist():
        d = df_race_gender_dist()
        if d.empty:
            return go.Figure().update_layout(title="Gender by Race/Ethnicity (2023) — no data")
        fig = px.bar(d, x="Race/Ethnicity", y="Population", color="Gender", title="Gender by Race/Ethnicity (2023)", barmode="group")
        return fig


    @output
    @render_widget
    def geo_zip_bar_rank():
        d = df_zip_2023()
        if d.empty:
            return go.Figure().update_layout(title="Population by ZIP Code (2023) — no data")
        d = d.sort_values("Population", ascending=True)
        return px.bar(d, x="Population", y="ZIP Code", title="Population by ZIP Code (2023)", orientation="h")

    @output
    @render_widget
    def geo_zip_trends():
        selected = input.zip_select()
        d = df_zip_trends()
        if not selected:
            return go.Figure().update_layout(title="Please select at least one ZIP code.")
        if d.empty:
            return go.Figure().update_layout(title="Selected ZIP Code Population Trends — no data")
        d = d[d["ZIP Code"].isin(selected)]
        fig = px.line(d, x="Year", y="Population", color="ZIP Code", title="Selected ZIP Code Population Trends", markers=True)
        return fig

    @output
    @render_widget
    def geo_zip_age_dist():
        d = df_zip_age_dist()
        if d.empty:
            return go.Figure().update_layout(title="Age Distribution by ZIP Code (2023) — no data")
        fig = px.bar(d, x="ZIP Code", y="Population", color="Age Group", title="Age Distribution by ZIP Code (2023)", barmode="stack")
        fig.update_xaxes(categoryorder="total descending")
        return fig

app = App(app_ui, server)
