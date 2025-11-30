========================================
README.txt
Long Beach Demographic Dashboard (Shiny for Python)
========================================

Author: [Yash Madan]

------------------------------------------------
1. PROJECT OVERVIEW
------------------------------------------------

This project is an interactive **Long Beach Demographic Dashboard** built using:

- Python
- Shiny for Python (web framework)
- Plotly (interactive charts)
- Pandas + openpyxl (data loading and cleaning)

The goal is to visualize demographic data for the City of Long Beach using the official Excel workbooks provided. The app allows users to explore population patterns by:

- Year
- Age group
- Gender
- Race/Ethnicity
- ZIP code

The dashboard runs locally (on `localhost`) and is intended to be launched by anyone who has Python installed and the same data files.


------------------------------------------------
2. HOW TO INSTALL & RUN (READ THIS FIRST)
------------------------------------------------

This is the most important section for anyone trying to run the project.

You will need:

- Python 3.10 or newer (3.11 also works)
- Internet browser (Chrome, Firefox, Edge, or Safari)
- The Excel files listed below, in the SAME folder as `app.py`


2.1 Required Excel Files
------------------------

The following files must be present in the same directory as `app.py`:

- Long Beach 2023 Estimates - Copy.xlsx
- Long Beach race by year US Estimates - Copy.xlsx
- Long Beach gen and total US Estimates - Copy.xlsx
- Long Beach zip and year Estimates - Copy.xlsx
- Long Beach zip gender year Estimates - Copy.xlsx

If any of these file names are changed or moved to another folder, the application’s data loaders will fail to locate the data and the charts may show “no data”.


2.2 Recommended Folder Structure
--------------------------------

Put everything in a single project folder, for example:

  LongBeachDashboard/
  ├── app.py
  ├── Long Beach 2023 Estimates - Copy.xlsx
  ├── Long Beach race by year US Estimates - Copy.xlsx
  ├── Long Beach gen and total US Estimates - Copy.xlsx
  ├── Long Beach zip and year Estimates - Copy.xlsx
  └── Long Beach zip gender year Estimates - Copy.xlsx


2.3 Installing Python Packages
------------------------------

Open a terminal or command prompt and navigate to the project folder.

(Optional but recommended) Create and activate a virtual environment:

On Windows:

  python -m venv .venv
  .venv\Scripts\activate

On macOS / Linux:

  python -m venv .venv
  source .venv/bin/activate

Then install the required packages:

  pip install --upgrade pip
  pip install shiny shinywidgets plotly pandas openpyxl


2.4 Running the Application
---------------------------

From the same folder (containing `app.py`), run:

  python -m shiny run --reload app.py

After a few seconds, the terminal will print a URL such as:

  http://localhost:8000

Open that URL in your web browser to view and use the dashboard.

NOTE:
- This application is NOT deployed online.
- It only runs locally on your machine via `localhost`.


------------------------------------------------
3. PURPOSE AND SCOPE OF THE PROJECT
------------------------------------------------

The primary purpose of this project is to:

- Present Long Beach demographic data in an interactive, easy-to-understand format.
- Give users the ability to explore how population changes by time, age, race, gender, and geography (ZIP code).
- Demonstrate technical skills in data cleaning, transformation, and visualization using Python and Shiny.

In my own words:

I built this dashboard to turn complex Long Beach demographic Excel files into clear visual stories. Instead of scrolling through spreadsheets, a user can click through tabs and charts that summarize:

- How the population has changed over time
- How age and gender are distributed
- How race and ethnicity are structured by age and gender
- How population varies across ZIP codes


------------------------------------------------
4. APPLICATION STRUCTURE (WHAT EACH TAB SHOWS)
------------------------------------------------

When the app runs at `http://localhost:8000`, it displays a navigation bar with four main tabs:

- Summary Overview
- Age & Gender Deep Dive
- Race & Ethnicity Deep Dive
- Geographic Deep Dive (ZIP Code)


4.1 Tab 1: Summary Overview
---------------------------

This is the high-level “dashboard home page” for 2023.

Elements:

1. Value Boxes
   - Total Population (2023)
   - Male Population (2023)
   - Female Population (2023)
   - Largest Age Group (e.g., 20–44 with its count)

   These values give a quick snapshot of the city’s size and general structure.

2. Population Trend (2011–2023)
   - A Plotly line chart of total population by year.
   - Data comes from the "Long Beach (2023)" sheet in:
       Long Beach 2023 Estimates - Copy.xlsx

3. Race/Ethnicity Breakdown (2023)
   - A donut (pie) chart showing the proportion of:
     Hispanic/Latino, White (Not Hispanic), Asian (Not Hispanic),
     Black (Not Hispanic), NHPI (Not Hispanic)
   - Data is based on a TOTAL row in:
       Long Beach gen and total US Estimates - Copy.xlsx
     Sheet: "Race_Ethnicity (2023)"

4. Population by ZIP Code (2023)
   - Horizontal bar chart ranking each ZIP code by population.
   - Data comes from the Long Beach 2023 estimates workbook,
     "Long Beach (2023)" sheet, in the ZIP summary area.


4.2 Tab 2: Age & Gender Deep Dive
---------------------------------

Focuses on population structure by age and gender.

1. Population Pyramid (2023)
   - Classic age-sex pyramid:
     - Male counts plotted as negative values (left side of chart)
     - Female counts as positive values (right side of chart).
   - Visualizes which age bands have more men/women.
   - Data from "Long Beach (2023)" age/sex table.

2. Population Change by Age Group (2019–2023)
   - Area chart showing trends for predefined age groups over the last 5 years.
   - Example age groups: Under 5, 5–19, 20–44, etc.
   - Data extracted from the age category trend table in the same workbook.


4.3 Tab 3: Race & Ethnicity Deep Dive
-------------------------------------

Examines race/ethnicity across time, age, and gender.

1. Population Trends by Race/Ethnicity (2017–2023)
   - Line chart with separate lines for:
     - Hispanic
     - White
     - Asian
     - Black
   - Data from:
       Long Beach race by year US Estimates - Copy.xlsx
     Sheet: "RACE BY YEAR"
   - Uses a specially indexed row that stores totals for each race and year.

2. Age Distribution by Race/Ethnicity (2023)
   - Stacked bar chart:
     - X-axis: Race/Ethnicity
     - Colors: age groups
   - Shows how age breakdown differs by race.
   - Data from a compact age-by-race block in:
       Long Beach gen and total US Estimates - Copy.xlsx
     Sheet: "Race_Ethnicity (2023)"

3. Gender by Race/Ethnicity (2023)
   - Grouped bar chart:
     - X-axis: Race/Ethnicity
     - Bars: Male vs Female counts
   - Data from rows that record total male and total female by race.


4.4 Tab 4: Geographic Deep Dive (ZIP Code)
------------------------------------------

Explores geography-based population differences.

1. Population by ZIP Code (2023)
   - Similar to the Summary tab’s ZIP chart, ranking ZIPs by total population.

2. ZIP Code Population Trends (2016–2023)
   - Multi-line chart.
   - Users can select one or more ZIP codes from a dropdown.
   - The chart updates to show each selected ZIP’s trend over time.
   - Data from:
       Long Beach zip and year Estimates - Copy.xlsx
     Sheet: "Zip and Year"
   - The loader locates “Year 2016”, “Year 2017”, etc., and extracts totals.

3. Age Distribution by ZIP Code (2023)
   - Stacked bar chart:
     - X-axis: ZIP code
     - Colors: age groups
   - Shows which ZIPs skew younger or older.
   - Data from:
       Long Beach zip gender year Estimates - Copy.xlsx
     Sheet: "Zip, Gender, Age by Year"
   - The loader finds the "Year 2023" section and uses each ZIP’s “Total” column across age rows.


------------------------------------------------
5. TECHNICAL IMPLEMENTATION DETAILS
------------------------------------------------

5.1 Main Technologies
---------------------

- **Shiny for Python**
  - Used to define the UI (`ui.page_navbar`, `ui.nav_panel`, `ui.value_box`, etc.).
  - Defines server-side reactive logic with `@reactive.Calc`.
  - Outputs charts using `@render_widget`.

- **shinywidgets**
  - Integrates Plotly figures into Shiny using `output_widget` and `render_widget`.

- **Plotly**
  - Used for all interactive charts (line, bar, pie, area, etc.).
  - Provides hover interactions, legends, zooming, and more.

- **Pandas + openpyxl**
  - Reads `.xlsx` files.
  - Cleans and reshapes the data:
    - `read_excel(..., header=..., skiprows=..., nrows=...)`
    - `melt` for long-form data
    - Type conversions with `pd.to_numeric`


5.2 Data Loading Strategy
-------------------------

The raw Excel files are NOT perfectly clean tables. They contain:

- Multiple header lines
- Notes and description rows
- Extra totals and sub-totals
- Different layouts per sheet

To deal with this, I wrote custom loader functions for each dataset, such as:

- `load_population_trend()`
- `load_zip_population_2023()`
- `load_population_pyramid_2023()`
- `load_age_group_trends()`
- `load_race_2023()`
- `load_race_trends()`
- `load_race_age_dist_2023()`
- `load_race_gender_2023()`
- `load_zip_trends()`
- `load_zip_age_dist_2023()`

Each function:

- Targets a specific sheet (e.g., "Long Beach (2023)", "RACE BY YEAR").
- Uses fixed header row indices and `skiprows` values based on inspection.
- Selects specific columns with `usecols` (e.g., `[0, 1]` for Year and Total).
- Drops empty rows and performs numeric conversion.
- Returns a tidy DataFrame ready for plotting.

If sheet structures change (for example, if someone inserts an extra row above a table), the chart can break. In that case, the fix is usually to adjust the `header=` or `skiprows=` numbers in the corresponding loader.


5.3 Server and UI Structure
---------------------------

- The UI is defined with `app_ui = ui.page_navbar(...)` and multiple `ui.nav_panel` sections.
- The server function:
  - Declares reactive data sources using `@reactive.Calc`.
  - Connects them to Plotly charts via `@render_widget`-decorated functions.
- Each chart function:
  - Pulls from a reactive DataFrame (e.g., `df_trend()`, `df_race_trends()`).
  - If the DataFrame is empty, returns a blank Plotly figure with a "no data" title.
  - Otherwise, builds and returns the appropriate Plotly figure.


------------------------------------------------
6. HOW SOMEONE ELSE CAN REPRODUCE OR MODIFY
------------------------------------------------

To reproduce:

1. Get the same Excel files.
2. Place them in the same folder as `app.py`.
3. Install `shiny`, `shinywidgets`, `plotly`, `pandas`, and `openpyxl`.
4. Run the app with:

   python -m shiny run --reload app.py

To modify:

- If you add a new data source, create a new loader function.
- Add a new `@reactive.Calc` for that dataset.
- Add a new `@output` / `@render_widget` function for the chart.
- Wire it into the UI inside an existing or new `ui.nav_panel`.


------------------------------------------------
7. TROUBLESHOOTING
------------------------------------------------

Common issues and solutions:

1. ISSUE: Terminal shows an import error (e.g., "No module named 'shiny'")
   SOLUTION: Install or reinstall dependencies:

     pip install shiny shinywidgets plotly pandas openpyxl

2. ISSUE: Charts show “— no data” as the title
   POSSIBLE CAUSES:
   - Excel file is missing or misnamed.
   - Sheet name changed.
   - Header row indices (e.g., 98, 113, etc.) shifted due to edited rows.

   SOLUTIONS:
   - Confirm that all file names match exactly:
       Long Beach 2023 Estimates - Copy.xlsx
       Long Beach race by year US Estimates - Copy.xlsx
       Long Beach gen and total US Estimates - Copy.xlsx
       Long Beach zip and year Estimates - Copy.xlsx
       Long Beach zip gender year Estimates - Copy.xlsx
   - Open the Excel file and confirm the sheet names:
       "Long Beach (2023)"
       "Race_Ethnicity (2023)"
       "RACE BY YEAR"
       "Zip and Year"
       "Zip, Gender, Age by Year"
   - If a table is clearly shifted down one row, adjust the `header=` or `skiprows=` in the relevant loader.

3. ISSUE: App doesn’t open in browser
   - Ensure the Shiny command is still running.
   - Make sure you are visiting the URL printed in the terminal (usually `http://localhost:8000`).
   - Check firewall/antivirus issues if running in a heavily locked-down environment.


------------------------------------------------
8. PERSONAL SUMMARY (WHAT I DID / LEARNED)
------------------------------------------------

In this project I:

- Built an interactive dashboard using Shiny for Python.
- Loaded multiple complex Excel workbooks, each with different structures.
- Wrote custom data-cleaning logic to extract only the needed data.
- Designed multiple interconnected visualizations:
  - Summary statistics
  - Time-series trends
  - Population pyramids
  - Race and age distributions
  - ZIP-level geographic insights
- Learned how to integrate Plotly with Shiny via shinywidgets.
- Organized the project in a way that someone else can run it locally.

This midterm deliverable demonstrates my ability to:

- Work with real-world messy data files (Excel).
- Turn tables into tidy DataFrames.
- Build a small, but complete, analytical web application in Python.
- Document the installation and usage clearly so others can understand and reproduce it.

END OF README
