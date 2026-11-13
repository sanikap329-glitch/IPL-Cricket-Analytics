# IPL INSIGHT – Batter Intelligence & Strategy Platform

An interactive IPL cricket analytics dashboard built using Python and Streamlit to analyse batter performance, compare batting strategies across match phases, and explore historical performance patterns.

## Project Overview

IPL INSIGHT transforms IPL ball-by-ball data into meaningful cricket insights through data processing, statistical analysis, player ratings, and interactive visualizations.

## Key Features

- **Batter Intelligence:** Analyse individual batter performance.
- **Phase-Aware Ratings:** Evaluate batters across Powerplay, Middle Overs, and Death Overs.
- **Season Analysis:** Explore player and team performance across IPL seasons.
- **Temporal Validation:** Examine historical versus future performance patterns.
- **Interactive Dashboard:** Explore insights through Streamlit visualizations.

## Technology Stack

- Python
- Streamlit
- Pandas and NumPy
- Plotly
- MySQL (local analysis workflows)

## Project Structure

```text
IPL-Cricket-Analytics/
├── app.py
├── requirements.txt
├── dashboard/
├── Data/
│   └── outputs/
├── Outputs/
│   └── Charts/
├── Notebook/
└── Reports/
```

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/sanikap329-glitch/IPL-Cricket-Analytics.git
   cd IPL-Cricket-Analytics
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it on Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the dashboard:

   ```bash
   streamlit run app.py
   ```

## Data

The dashboard uses processed IPL datasets stored in `Data/outputs/` and analytical outputs stored in `Outputs/`.

Raw source datasets and temporary files are excluded from the repository.

## Author

**Sanika Pawar**

B.Tech – Data Science

GitHub: [sanikap329-glitch](https://github.com/sanikap329-glitch)