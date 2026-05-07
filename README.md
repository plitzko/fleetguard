# PREMA – Predictive Maintenance

**PRE**diktive **MA**intenance Dashboard · MVP Click-Demo

Klickbares Streamlit-Frontend für die MVP-Konzept-Präsentation am 08.05.2026.

**Hochschule München · Big Data SS2026 · Team 1 (Predictive)**  
Ujjwal · Max · Edel · Walter

---

## Was das ist

PREMA ist ein klickbarer Prototyp mit drei Screens:

1. **Flottenübersicht** – Statusampel über 10 LKW, KPIs, sortiert nach Priorität
2. **Einzelfahrzeug-Detail** – Sensorwerte, 72h-Zeitreihe für Bremse + Motor, Alert-Verlauf, RUL
3. **Alert-Feed** – Chronologische Liste aller Warnungen, filterbar nach Schweregrad

Daten sind statisch und reproduzierbar (Seed 42). Keine echte ML-Pipeline – das ist das **Konzept**, das wir bis 19.06. als echtes MVP bauen.

---

## Projektstruktur

```text
fleetguard/
├── app.py                    # Streamlit-Hauptapp (alle drei Screens)
├── requirements.txt          # Python-Abhängigkeiten
├── runtime.txt               # Python-Version für Streamlit Cloud (3.12)
├── .streamlit/
│   └── config.toml           # Theme & Server-Config (Farben, headless)
└── data/
    ├── fleet.csv             # Aktueller Flottenstand (10 LKW)
    ├── timeseries.csv        # 72h-Zeitreihendaten (Bremse, Motor, Öl)
    ├── alerts.csv            # Alert-Feed (alle Meldungen)
    ├── truck_alerts.csv      # Alerts pro Fahrzeug (für Detailansicht)
    └── generate_data.py      # Datengenerator – einmalig ausführen
```

---

## Abhängigkeiten

```text
streamlit >= 1.36
pandas    >= 2.2
altair    >= 5.3
numpy     >= 2.0
```

Alle Pakete sind in `requirements.txt` gepinnt (Mindestversionen).

---

## Lokal laufen lassen

```bash
# Einmal: virtuelles Environment + Dependencies
python -m venv .venv

# Mac/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# App starten
streamlit run app.py
```

App läuft dann auf `http://localhost:8501`.

---

## Deploy auf Streamlit Community Cloud (kostenlos, online)

1. `runtime.txt` und `.streamlit/config.toml` im Repo lassen
2. Repo auf GitHub pushen (public oder privat)
3. Auf [share.streamlit.io](https://share.streamlit.io) einloggen mit GitHub
4. "New app" → Repo wählen → `app.py` als Main file → Deploy
5. Nach ~2 Minuten ist eine `https://xxx.streamlit.app` URL verfügbar

Diesen Link in das Slide-Deck einbinden. Lokal als Backup laufen lassen, falls die Cloud-Demo zickt.

---

## Demo-Skript für die Präsentation (8.5. · ~3 min)

1. **Flottenübersicht öffnen** – „Hier sieht Thomas, der Flottenmanager, alle 10 LKW auf einen Blick. LKW-01 ist rot, ganz oben sortiert. Die KPI-Cards zeigen: ein Fahrzeug kritisch, zwei gewarnt, sieben OK. Geschätzte verhinderte Kosten: 2.400 €."
2. **Auf „Details" bei LKW-01 klicken** – „Wir drillen runter. Das XGBoost-Modell stuft das Fahrzeug als kritisch ein. Bremsflüssigkeit auf 12 %. Restlebensdauer noch 48 Stunden. Empfehlung: sofort aus dem Verkehr ziehen."
3. **Auf den Zeitreihen-Chart zeigen** – „Hier sieht man die Degradation über 72 Stunden. Die rote gestrichelte Linie ist die kritische Schwelle. Das System hätte den Trend schon vor 2 Tagen erkannt – Isolation Forest hat den ersten INFO-Alert ausgelöst, bevor der Wert die Warnschwelle unterschritten hat."
4. **Zurück → Alert-Feed** – „Hier landen alle Alerts, filterbar nach Schweregrad. Jede Zeile zeigt: Quelle (welches Modell), Schweregrad, geschätzte Einsparung."
5. **Das war der Klick-Dummy.** Bis 19.06. ersetzen wir die statischen CSVs durch echten Simulator-Output, hängen die ML-Pipeline dahinter und stecken alles in Docker.

---

## Architektur (was hinter dem Klick-Dummy steckt im echten MVP)

```text
data/fleet.csv          ← jetzt static, bald: Python-Simulator
data/timeseries.csv     ← jetzt static, bald: TimescaleDB-Query
data/alerts.csv         ← jetzt static, bald: Alert-Engine-Output
data/truck_alerts.csv   ← jetzt static, bald: TimescaleDB-Query
```

Alle Screens lesen ausschließlich CSV. Sobald das Backend läuft, tauschen wir die Datenquelle aus – die UI bleibt 1:1 gleich. Das ist der Sinn dieses Prototypen.

### Testdaten neu generieren

```bash
python data/generate_data.py
```

---

## Team & Aufgaben

- **Ujjwal & Max** – Frontend, User Flows, Wireframes (dieser Repo)
- **Edel & Walter** – ML-Modelle, Architektur-Slides, Demo-Szenario

Slides für 08.05. liegen separat.
