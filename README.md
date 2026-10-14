# Isokinetic Risk Factor Profiling Analysis (PHR 799)
### University of Botswana | Master of Education in Sports Science

This repository contains the software implementation for my master's research project, automating the clinical risk-stratification metrics of the Croisier et al. (2008) framework. 

The application processes concentric quadriceps and eccentric hamstring peak torque data tested at 60 degrees per second on the HUMAC NORM dynamometer to calculate functional H:Q ratios and bilateral muscle asymmetries natively.

---

## Code Architecture and File Layout

To ensure data protection compliance under Botswana's Data Protection Act and maintain structural code modularity, the system is separated into three standalone files:

* **calculation_engine.py**: Houses the pure mathematical formulas and clinical thresholds (below 80 percent for H:Q ratios and greater than or equal to 15 percent for hamstring asymmetry) completely independent of the user interface layout for clear academic evaluation and grading.
* **db_handler.py**: Handles local relational isolation. Initializing a new cohort name creates a separate, sharded .db file on the hard drive so that datasets from different teams or research groups never mix.
* **app.py**: The Streamlit user interface panel. Natively reads the local folder to automatically find and list existing database files, controls data logging form inputs, and renders interactive cohort risk scatter matrices.

---

## How to Run the Application

1. Install the required external Python packages via your terminal:
   ```bash
   pip install streamlit pandas plotly
   ```

2. Launch the application locally:
   ```bash
   streamlit run app.py
   ```

---

## Developer Profile

* **Author:** Tshepang Christmas
* **Institution:** University of Botswana
* **Student ID:** 202005567
* **Location:** Gaborone, Botswana

## 🏛️ Academic Supervision & Credits

* **Research & Architecture Supervisor:** **Dr. Kagiso Ndlovu** (Head of Research Information & Data Management, University of Botswana)

### 🔬 Informatics Oversight Credit
Special acknowledgment is extended to **Dr. Kagiso Ndlovu** for his invaluable mentorship, structural review, and architectural oversight during the development of this platform. His guidance was instrumental in transitioning this project from a basic calculations utility into a rigorous **Design Science Research (DSR)** instantiation. Specifically, his supervision directly guided. Infinite thanks Dr.