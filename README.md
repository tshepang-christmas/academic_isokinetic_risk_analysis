# Athlete Isokinetic Risk (PHR 799)
### University of Botswana | Master of Education in Sports Science

This is a research prototype that calculates functional hamstring-to-quadriceps (H:Q) ratios and eccentric bilateral hamstring asymmetry from isokinetic peak torque values, and classifies each player's profile as either a **normal profile** or **strength imbalance present**. It adapts the classification approach of Croisier et al. (2008) to a single testing velocity (60 degrees per second) on the HUMAC NORM dynamometer. It is the artefact developed within a Design Science Research methodology (Hevner et al., 2004).

---
## Status and intended use
 
- This is a **research prototype**. It runs locally on one computer and is not deployed.
- It has **no user login**. Anyone who can opens the application on a machine can use it.
- It is **not a medical device** and must not be used for clinical decisions.
- The thresholds are reference values taken from the literature. They were derived at different testing velocities and on different dynamometers, and they have not been validated in a Botswana population or on the HUMAC NORM.
---
## What it does
 
1. Ingests six inputs: a player identifier, the dominant leg, and four peak torque values in Nm (concentric quadriceps and eccentric hamstring, for each leg).
2. Converts the player identifier into a pseudonymous ID. Names are never stored.
3. Calculates, using the formulas below.
4. Flags deficits against fixed thresholds and returns a classification.
5. Lets the user save the result to a local database or run a temporary calculation that is not saved.
6. Shows an interactive scatter plot and a table of saved records, with a CSV export, a "rollback latest entry" control and a player report.
---
## Code Architecture and File Layout

To ensure data protection compliance under Botswana's Data Protection Act (2024) and maintain structural code modularity, the system is separated into three standalone files:

* **calculation_engine.py**: Houses the pure mathematical formulas and clinical thresholds (below 80 percent for H:Q ratios and greater than or equal to 15 percent for hamstring asymmetry) completely independent of the user interface layout for clear academic evaluation and grading.
* **db_handler.py**: Handles local relational isolation. Initializing a new cohort name creates a separate, sharded .db file on the hard drive so that datasets from different teams or research groups never mix.
* **app.py**: The Streamlit user interface panel. Natively reads the local folder to automatically find and list existing database files, controls data logging form inputs, and renders interactive cohort risk scatter matrices.
---
## Repository layout

Clone the repo onto your machine.
 
| File | Role |
|---|---|
| `App.py` | Streamlit interface: input form, results, plot, table, export |
| `calculation_engine.py` | Formulas, thresholds and classification, independent of the interface |
| `db_handler.py` | SQLite storage; one database file per workspace name |
| `security_wrapper.py` | Pseudonymisation of player identifiers (HMAC-SHA256), reads the secret key from an environment variable |
| `assets/` | Images used by the interface |
| `requirements.txt` | Pinned package versions |
`tests/synthetic_dataset`
---
### Indicators and thresholds
 
| Indicator | Formula | Deficit flagged when |
|---|---|---|
| Functional H:Q ratio, dominant leg | eccentric hamstring / concentric quadriceps x 100 | below 80% |
| Functional H:Q ratio, non-dominant leg | eccentric hamstring / concentric quadriceps x 100 | below 80% |
| Eccentric hamstring asymmetry | (stronger leg - weaker leg) / stronger leg x 100 | 15% or more |
---
**Classification rule:** "strength imbalance present at 1 or more deficits".
---
## How to Run the Application
## Installation
 
Requires Python 3.14.0. From the folder that contains `App.py`:
 
1. Create and activate a virtual environment.
2. Install the packages:
```
   pip install -r requirements.txt
```
 
## Set your secret key (required)
 
The application pseudonymises player identifiers with a secret key that is **not** included in this repository. Generate your own before the first run.
 
**1. Generate a key.** This uses only Python's standard library, so nothing needs installing:
 
```
python -c "import secrets; print(secrets.token_hex(32))"
```
 The output is a 64-character string. Store it in your trusted password manager.
 
**2. Set the environment variable `PHR799_SECRET_KEY` to that value.**
 
Windows PowerShell, current terminal only:
```
$env:PHR799_SECRET_KEY = "paste-your-key-here"
```
 
Windows, saved for future terminals (close and reopen the terminal afterwards):
```
setx PHR799_SECRET_KEY "paste-your-key-here"
```
 
macOS or Linux, current terminal only:
```
export PHR799_SECRET_KEY="paste-your-key-here"
```
 
**Important**
 
- The application will not start if the variable is not set.
- Use the same key for the whole replication study. A different key gives every player a different ID, so earlier records no longer match.
- If the key is lost, the IDs cannot be regenerated.
- Use a private key for real participant data.

## Run
 
```
streamlit run App.py
```
 
Open the local address that Streamlit prints. Enter a workspace name in the sidebar to choose or create a database.
 
---
## Check your installation

Refer to synthetic_dataset to test for your use case.
 
## Data protection and repository rules
 
- Player names are never stored. Each identifier is converted to a pseudonymous ID using a keyed hash, so IDs cannot be reversed without the key. Anyone holding the key and a list of names could regenerate them, so this is pseudonymisation and not anonymisation.
- **Never commit** real participant data, database files (`*.db`), exported CSV records or any file containing a key. Make sure the ignore file covers these.
- Any example data in this repository is synthetic.
- 
## Limitations
 
- Single-user prototype with no authentication, role-based access, audit logging or encryption inside the application.
- Records are stored in a single table with one row per saved screening. Repeated screenings of one player accumulate, but the schema is not normalised.
- CSV export is file-based data exchange, not standards-based interoperability.
- Tested with synthetic data and test cases; not clinically validated.
- 
## How to cite
 
Christmas, T. (2026). *Athlete Isokinetic Risk* [Computer software]. University of Botswana. https://github.com/tshepang-christmas/academic_isokinetic_risk_analysis
 
## Author and supervision
 
**Author:** Tshepang Christmas, MSc Sport Science, University of Botswana
---

## 🏛️ Academic Supervision & Credits

* **Research & Architecture Supervisor:** **Dr. Kagiso Ndlovu**, **Dr. D. M. Tladi** and **Dr. M. A. Gaesenngwe**