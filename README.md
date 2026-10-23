# ThermoLab Cycle Simulator
BAMEE203 Assignment II, Set A — Jobern Danny Barreto, 25BME1031.

Features: Diesel-cycle analysis with r=20,19,18,17,16,15; Rankine-cycle analysis with boiler pressures 3,5,6 MPa; interactive graphs and tables.

Run locally with Python 3.10+:
1. `python -m venv .venv`
2. Activate the environment (`.venv\\Scripts\\activate` on Windows, `source .venv/bin/activate` on macOS/Linux)
3. `pip install -r requirements.txt`
4. `python app.py`
5. Open http://127.0.0.1:5000

Host online: upload these files to GitHub, create a Render Web Service from the repository, build command `pip install -r requirements.txt`, start command `gunicorn app:app`. `render.yaml` is included.

Diesel assumptions: p1=95 kPa, T1=20°C, Tmax=2400°C, cp=1.004, cv=0.718 kJ/kg K, k=1.4. Rankine assumptions: condenser 0.05 MPa, turbine inlet 300°C, mass flow 46 kg/s, boiler pressures 3/5/6 MPa. Rankine steam properties use CoolProp. These are idealized academic models; verify against class notes and steam tables.
