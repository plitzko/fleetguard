"""
PREMA - Predictive Maintenance Dashboard (MVP Click-Demo)
Hochschule München | Big Data SS2026 | Team 1 (Predictive)

Run locally:
    streamlit run app.py

Deploy on Streamlit Community Cloud:
    https://share.streamlit.io
"""
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
from datetime import datetime

# ============================================================================
# Page config
# ============================================================================
st.set_page_config(
    page_title="PREMA – Predictive Maintenance",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# Custom CSS - industrial/refined aesthetic
# ============================================================================
st.markdown("""
<style>
    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Tighten top padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Custom header bar */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1.25rem;
        background: #1A1A1A;
        color: #FFFFFF;
        border-radius: 4px;
        margin-bottom: 1.5rem;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
    }
    .header-brand {
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }
    .header-brand-accent {
        color: #C8102E;
    }
    .header-user {
        font-size: 0.85rem;
        opacity: 0.8;
    }

    /* KPI cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E5E5E7;
        border-left: 4px solid #1A1A1A;
        padding: 1.1rem 1.25rem;
        border-radius: 4px;
    }
    .kpi-card.critical { border-left-color: #C8102E; }
    .kpi-card.warning  { border-left-color: #E89B00; }
    .kpi-card.ok       { border-left-color: #2E8B3D; }

    .kpi-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #6B6B6F;
        margin-bottom: 0.4rem;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 600;
        line-height: 1;
        color: #1A1A1A;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #6B6B6F;
        margin-top: 0.3rem;
    }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 3px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
    }
    .badge-critical { background: #C8102E; color: #FFF; }
    .badge-warning  { background: #E89B00; color: #FFF; }
    .badge-ok       { background: #2E8B3D; color: #FFF; }
    .badge-info     { background: #2B6CB0; color: #FFF; }

    /* Sensor strip */
    .sensor-row {
        display: grid;
        grid-template-columns: 160px 1fr 80px;
        gap: 1rem;
        align-items: center;
        padding: 0.6rem 0;
        border-bottom: 1px solid #F0F0F2;
    }
    .sensor-label {
        font-size: 0.85rem;
        color: #4A4A4F;
    }
    .sensor-bar-bg {
        height: 8px;
        background: #F0F0F2;
        border-radius: 4px;
        overflow: hidden;
    }
    .sensor-bar-fill {
        height: 100%;
        border-radius: 4px;
    }
    .sensor-value {
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: right;
    }

    /* Alert row */
    .alert-row {
        display: grid;
        grid-template-columns: 130px 90px 90px 1fr 130px;
        gap: 1rem;
        align-items: center;
        padding: 0.7rem 1rem;
        border-bottom: 1px solid #F0F0F2;
        font-size: 0.85rem;
    }
    .alert-row:hover { background: #FAFAFC; }
    .alert-time {
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        color: #6B6B6F;
        font-size: 0.78rem;
    }
    .alert-truck {
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        font-weight: 600;
    }
    .alert-savings {
        text-align: right;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        color: #2E8B3D;
        font-weight: 600;
    }
    .alert-meta {
        font-size: 0.72rem;
        color: #8A8A8F;
        margin-top: 0.15rem;
    }

    /* All buttons: never wrap text */
    .stButton > button {
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        white-space: nowrap;
    }

    /* Section title */
    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin: 1.5rem 0 0.6rem 0;
        color: #1A1A1A;
        letter-spacing: -0.01em;
    }
    .section-sub {
        font-size: 0.78rem;
        color: #6B6B6F;
        margin-bottom: 0.8rem;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
    }

    /* Recommendation banner */
    .reco-banner {
        background: linear-gradient(90deg, #FFF5F5 0%, #FFFFFF 100%);
        border-left: 4px solid #C8102E;
        padding: 1rem 1.25rem;
        border-radius: 4px;
        margin-bottom: 1.25rem;
    }
    .reco-banner.warning {
        background: linear-gradient(90deg, #FFF8EC 0%, #FFFFFF 100%);
        border-left-color: #E89B00;
    }
    .reco-banner.ok {
        background: linear-gradient(90deg, #F0F9F2 0%, #FFFFFF 100%);
        border-left-color: #2E8B3D;
    }
    .reco-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .reco-text {
        font-size: 0.85rem;
        color: #4A4A4F;
        line-height: 1.4;
    }
    .reco-rul {
        float: right;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        font-size: 0.85rem;
        color: #1A1A1A;
        background: #FFFFFF;
        padding: 0.2rem 0.6rem;
        border-radius: 3px;
        border: 1px solid #E5E5E7;
    }

    /* Truck table styling */
    .truck-table-header {
        display: grid;
        grid-template-columns: 100px 130px 120px 110px 130px 100px;
        gap: 1rem;
        padding: 0.6rem 1rem;
        background: #1A1A1A;
        color: #FFFFFF;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        border-radius: 4px 4px 0 0;
    }
    .truck-table-row {
        display: grid;
        grid-template-columns: 100px 130px 120px 110px 130px 100px;
        gap: 1rem;
        padding: 0.7rem 1rem;
        border-bottom: 1px solid #F0F0F2;
        background: #FFFFFF;
        font-size: 0.88rem;
        align-items: center;
    }
    .truck-table-row:hover { background: #FAFAFC; }
    .truck-table-row.critical { background: #FFF8F8; }
    .truck-id {
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        font-weight: 600;
    }
    .truck-detail-link {
        color: #C8102E;
        text-decoration: none;
        font-size: 0.8rem;
    }

    /* Nav tabs */
    [data-testid="stHorizontalBlock"] [data-testid="column"] button {
        width: 100%;
    }

    /* Hide default top padding from tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Mono', 'Courier New', monospace;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Data loading
# ============================================================================
@st.cache_data
def load_data():
    base = Path(__file__).parent / "data"
    fleet = pd.read_csv(base / "fleet.csv")
    timeseries = pd.read_csv(base / "timeseries.csv", parse_dates=["timestamp"])
    alerts = pd.read_csv(base / "alerts.csv", parse_dates=["timestamp"])
    truck_alerts = pd.read_csv(base / "truck_alerts.csv", parse_dates=["timestamp"])
    return fleet, timeseries, alerts, truck_alerts

fleet, timeseries, alerts, truck_alerts = load_data()

# ============================================================================
# Session state for navigation
# ============================================================================
if "view" not in st.session_state:
    st.session_state.view = "fleet"
if "selected_truck" not in st.session_state:
    st.session_state.selected_truck = None
if "alert_filter" not in st.session_state:
    st.session_state.alert_filter = "ALLE"

def go_to_detail(truck_id):
    st.session_state.view = "detail"
    st.session_state.selected_truck = truck_id

def go_to_fleet():
    st.session_state.view = "fleet"
    st.session_state.selected_truck = None

def go_to_alerts():
    st.session_state.view = "alerts"

# ============================================================================
# Helper functions
# ============================================================================
def status_badge(status):
    cls = {"KRITISCH": "badge-critical", "WARNUNG": "badge-warning",
           "OK": "badge-ok", "INFO": "badge-info"}.get(status, "badge-info")
    return f'<span class="badge {cls}">{status}</span>'

def severity_color(severity):
    return {"KRITISCH": "#C8102E", "WARNUNG": "#E89B00",
            "INFO": "#2B6CB0", "OK": "#2E8B3D"}.get(severity, "#6B6B6F")

# ============================================================================
# Header
# ============================================================================
st.markdown("""
<div class="header-bar">
    <div class="header-brand">PRE<span class="header-brand-accent">MA</span> · Predictive Maintenance</div>
    <div class="header-user">Thomas Müller · Spedition Müller GmbH</div>
</div>
""", unsafe_allow_html=True)

# Navigation
nav1, nav2, nav3, _ = st.columns([1.8, 1, 1.5, 3.7])
with nav1:
    if st.button("FLOTTENÜBERSICHT", use_container_width=True,
                 type="primary" if st.session_state.view == "fleet" else "secondary"):
        go_to_fleet()
        st.rerun()
with nav2:
    if st.button("ALERT-FEED", use_container_width=True,
                 type="primary" if st.session_state.view == "alerts" else "secondary"):
        go_to_alerts()
        st.rerun()
with nav3:
    if st.session_state.view == "detail" and st.session_state.selected_truck:
        st.button(f"DETAIL · {st.session_state.selected_truck}", use_container_width=True, type="primary", disabled=True)

# ============================================================================
# SCREEN 1: FLEET OVERVIEW
# ============================================================================
def render_fleet_overview():
    n_total = len(fleet)
    n_ok = (fleet["status"] == "OK").sum()
    n_warn = (fleet["status"] == "WARNUNG").sum()
    n_crit = (fleet["status"] == "KRITISCH").sum()
    avoided_eur = n_crit * 600 * 4  # 4h pro vermiedener Panne

    # KPI cards
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Fahrzeuge gesamt</div>
            <div class="kpi-value">{n_total}</div>
            <div class="kpi-sub">aktive Flotte</div>
        </div>
        <div class="kpi-card ok">
            <div class="kpi-label">Status OK</div>
            <div class="kpi-value">{n_ok}</div>
            <div class="kpi-sub">{n_ok/n_total*100:.0f}% der Flotte</div>
        </div>
        <div class="kpi-card warning">
            <div class="kpi-label">Warnung</div>
            <div class="kpi-value">{n_warn}</div>
            <div class="kpi-sub">Wartung in &lt; 14 Tagen</div>
        </div>
        <div class="kpi-card critical">
            <div class="kpi-label">Kritisch</div>
            <div class="kpi-value">{n_crit}</div>
            <div class="kpi-sub">~ {avoided_eur:,} € verhinderte Kosten</div>
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Flottenstatus</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">SORTIERT NACH PRIORITÄT · LIVE-DATEN AUS BATCH-PIPELINE · STAND {datetime.now().strftime("%H:%M")} UHR</div>', unsafe_allow_html=True)

    # Sort: critical first, then warning, then OK
    status_order = {"KRITISCH": 0, "WARNUNG": 1, "OK": 2}
    fleet_sorted = fleet.copy()
    fleet_sorted["sort_key"] = fleet_sorted["status"].map(status_order)
    fleet_sorted = fleet_sorted.sort_values(["sort_key", "rul_hours"]).drop(columns=["sort_key"])

    # Header – wrapped in same column structure as rows so columns align
    hcol, _ = st.columns([6, 1])
    with hcol:
        st.markdown("""
        <div class="truck-table-header">
            <div>LKW-ID</div>
            <div>Fahrer</div>
            <div>Motortemp.</div>
            <div>Bremse %</div>
            <div>RUL (Stunden)</div>
            <div>Status</div>
        </div>
        """, unsafe_allow_html=True)

    # Rows - using columns for click-through
    for _, truck in fleet_sorted.iterrows():
        row_class = "truck-table-row critical" if truck["status"] == "KRITISCH" else "truck-table-row"
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div class="{row_class}">
                <div class="truck-id">{truck['lkw_id']}</div>
                <div>{truck['driver']}</div>
                <div>{truck['motor_temp_c']:.0f} °C</div>
                <div>{truck['brake_fluid_pct']:.0f} %</div>
                <div>{truck['rul_hours']:,} h</div>
                <div>{status_badge(truck['status'])}</div>
            </div>
            """.replace(",", "."), unsafe_allow_html=True)
        with col2:
            if st.button("Details →", key=f"det_{truck['lkw_id']}", use_container_width=True):
                go_to_detail(truck["lkw_id"])
                st.rerun()

# ============================================================================
# SCREEN 2: TRUCK DETAIL
# ============================================================================
def render_truck_detail():
    truck_id = st.session_state.selected_truck
    truck = fleet[fleet["lkw_id"] == truck_id].iloc[0]

    # Back button
    back_col, _ = st.columns([1.5, 5.5])
    with back_col:
        if st.button("← Flottenübersicht", use_container_width=True):
            go_to_fleet()
            st.rerun()

    st.markdown(
        f'<div class="section-title" style="font-size:1.35rem; margin-top:0.5rem;">'
        f'{truck_id} &nbsp;·&nbsp; {truck["driver"]}</div>',
        unsafe_allow_html=True,
    )

    # Recommendation banner
    if truck["status"] == "KRITISCH":
        banner_cls = ""
        title = "SOFORTIGE WARTUNG EMPFOHLEN"
        issues = []
        if truck["brake_fluid_pct"] < 15:
            issues.append(f"Bremsflüssigkeit {truck['brake_fluid_pct']:.0f} %")
        if truck["motor_temp_c"] > 95:
            issues.append(f"Motortemperatur {truck['motor_temp_c']:.0f} °C")
        if truck["oil_pressure_bar"] < 2.5:
            issues.append(f"Öldruck {truck['oil_pressure_bar']:.1f} bar")
        issue_str = " · ".join(issues) if issues else "Kritische Sensorwerte"
        text = f"XGBoost-Modell stuft {truck_id} als kritisch ein. {issue_str} – Grenzwerte überschritten. Empfehlung: Fahrzeug aus dem Verkehr ziehen, Werkstattauftrag automatisch angelegt."
    elif truck["status"] == "WARNUNG":
        banner_cls = "warning"
        title = f"VERSCHLEIß ERHÖHT · Wartung innerhalb 14 Tagen"
        text = f"Verschleißmuster über Schwellwert. Wartung kann planbar in den nächsten 14 Tagen erfolgen."
    else:
        banner_cls = "ok"
        title = f"FAHRZEUG IM NORMALBETRIEB"
        text = f"Alle Sensorwerte im erwarteten Bereich. Nächste turnusgemäße Wartung in {truck['rul_hours']:,} h.".replace(",", ".")

    st.markdown(f"""
    <div class="reco-banner {banner_cls}">
        <div class="reco-rul">RUL: {truck['rul_hours']:,} h</div>
        <div class="reco-title">{status_badge(truck['status'])} &nbsp; {title}</div>
        <div class="reco-text">{text}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

    # Two columns: sensors left, chart right
    left, right = st.columns([1, 1.3])

    with left:
        st.markdown('<div class="section-title">Sensordaten · aktuell</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">LIVE-WERTE AUS LETZTER BATCH-INFERENZ</div>', unsafe_allow_html=True)

        sensors = [
            ("Motortemperatur", truck["motor_temp_c"], 110, "°C", "#C8102E" if truck["motor_temp_c"] > 95 else "#2E8B3D"),
            ("Öldruck",         truck["oil_pressure_bar"], 5.0, "bar", "#E89B00" if truck["oil_pressure_bar"] < 2.5 else "#2E8B3D"),
            ("Bremsflüssigkeit", truck["brake_fluid_pct"], 100, "%",
                "#C8102E" if truck["brake_fluid_pct"] < 15 else ("#E89B00" if truck["brake_fluid_pct"] < 35 else "#2E8B3D")),
            ("Reifendruck VL",  truck["tire_fl_bar"], 10, "bar", "#2E8B3D"),
            ("Reifendruck VR",  truck["tire_fr_bar"], 10, "bar", "#2E8B3D"),
        ]
        for label, val, max_val, unit, color in sensors:
            pct = min(100, val / max_val * 100)
            st.markdown(f"""
            <div class="sensor-row">
                <div class="sensor-label">{label}</div>
                <div class="sensor-bar-bg">
                    <div class="sensor-bar-fill" style="width: {pct}%; background: {color};"></div>
                </div>
                <div class="sensor-value">{val:.1f} {unit}</div>
            </div>
            """, unsafe_allow_html=True)

        # Vehicle metadata
        st.markdown('<div class="section-title">Fahrzeugdaten</div>', unsafe_allow_html=True)
        meta_col1, meta_col2 = st.columns(2)
        with meta_col1:
            st.metric("Kilometerstand", f"{truck['km_total']:,} km".replace(",", "."))
            st.metric("Fahrer", truck["driver"])
        with meta_col2:
            st.metric("Beladung", f"{truck['load_pct']} %")
            st.metric("RUL-Prognose", f"{truck['rul_hours']:,} h".replace(",", "."))

    with right:
        st.markdown('<div class="section-title">Bremsflüssigkeit · letzte 72 h</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">ZEITREIHEN-DEGRADATION · ISOLATION FOREST + XGBOOST</div>', unsafe_allow_html=True)

        ts_truck = timeseries[timeseries["lkw_id"] == truck_id].copy()

        # Threshold lines
        chart = alt.Chart(ts_truck).mark_line(
            color="#C8102E" if truck["status"] == "KRITISCH" else ("#E89B00" if truck["status"] == "WARNUNG" else "#2E8B3D"),
            strokeWidth=2.5
        ).encode(
            x=alt.X("timestamp:T", title=None, axis=alt.Axis(format="%d.%m %H:%M", labelFontSize=10)),
            y=alt.Y("brake_fluid_pct:Q", title="Bremsflüssigkeit (%)",
                    scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelFontSize=10, titleFontSize=11)),
            tooltip=[
                alt.Tooltip("timestamp:T", title="Zeit", format="%d.%m %H:%M"),
                alt.Tooltip("brake_fluid_pct:Q", title="Bremse %", format=".1f"),
            ]
        ).properties(height=280)

        # Threshold rules
        warn_line = alt.Chart(pd.DataFrame({"y": [30]})).mark_rule(
            color="#E89B00", strokeDash=[4, 4], strokeWidth=1.5
        ).encode(y="y:Q")
        crit_line = alt.Chart(pd.DataFrame({"y": [15]})).mark_rule(
            color="#C8102E", strokeDash=[4, 4], strokeWidth=1.5
        ).encode(y="y:Q")

        # Alert annotations as vertical rules
        ts_min, ts_max = ts_truck["timestamp"].min(), ts_truck["timestamp"].max()
        alert_markers = truck_alerts[
            (truck_alerts["lkw_id"] == truck_id) &
            (truck_alerts["timestamp"] >= ts_min) &
            (truck_alerts["timestamp"] <= ts_max)
        ].copy()
        sev_colors = {"KRITISCH": "#C8102E", "WARNUNG": "#E89B00", "INFO": "#2B6CB0"}
        alert_layers = [
            alt.Chart(alert_markers[alert_markers["severity"] == sev]).mark_rule(
                color=color, strokeWidth=1.5, strokeDash=[3, 3]
            ).encode(
                x="timestamp:T",
                tooltip=[
                    alt.Tooltip("timestamp:T", title="Alert", format="%d.%m %H:%M"),
                    alt.Tooltip("severity:N", title="Schweregrad"),
                    alt.Tooltip("message:N", title="Meldung"),
                ],
            )
            for sev, color in sev_colors.items()
            if not alert_markers[alert_markers["severity"] == sev].empty
        ]
        brake_chart = (
            alt.layer(chart, warn_line, crit_line, *alert_layers)
            if alert_layers else chart + warn_line + crit_line
        )
        st.altair_chart(brake_chart.configure_view(strokeWidth=0), use_container_width=True)

        cap = "⎯⎯ Warnschwelle 30 % · ⎯⎯ Kritische Schwelle 15 %"
        if not alert_markers.empty:
            cap += " · ╌╌ Alert-Zeitpunkte"
        st.caption(cap)

        # Motor temperature chart
        st.markdown('<div class="section-title">Motortemperatur · letzte 72 h</div>', unsafe_allow_html=True)
        chart2 = alt.Chart(ts_truck).mark_line(
            color="#1A1A1A", strokeWidth=2
        ).encode(
            x=alt.X("timestamp:T", title=None, axis=alt.Axis(format="%d.%m %H:%M", labelFontSize=10)),
            y=alt.Y("motor_temp_c:Q", title="Motortemp. (°C)",
                    scale=alt.Scale(domain=[60, 110]),
                    axis=alt.Axis(labelFontSize=10, titleFontSize=11)),
        ).properties(height=180)

        crit_temp = alt.Chart(pd.DataFrame({"y": [95]})).mark_rule(
            color="#C8102E", strokeDash=[4, 4], strokeWidth=1.5
        ).encode(y="y:Q")

        st.altair_chart((chart2 + crit_temp).configure_view(strokeWidth=0), use_container_width=True)

    # Alert history for this truck
    st.markdown('<div class="section-title">Alert-Verlauf · ' + truck_id + '</div>', unsafe_allow_html=True)
    truck_history = truck_alerts[truck_alerts["lkw_id"] == truck_id].sort_values("timestamp", ascending=False)

    if truck_history.empty:
        st.info("Keine Alerts für dieses Fahrzeug in den letzten 30 Tagen.")
    else:
        for _, alert in truck_history.iterrows():
            st.markdown(f"""
            <div class="alert-row" style="grid-template-columns: 130px 90px 1fr;">
                <div class="alert-time">{alert['timestamp'].strftime('%d.%m. %H:%M')}</div>
                <div>{status_badge(alert['severity'])}</div>
                <div>{alert['message']}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# SCREEN 3: ALERT FEED
# ============================================================================
def render_alert_feed():
    n_crit = (alerts["severity"] == "KRITISCH").sum()
    n_warn = (alerts["severity"] == "WARNUNG").sum()
    n_info = (alerts["severity"] == "INFO").sum()
    total_savings = alerts["savings_eur"].sum() * 4  # 4h pro Panne

    # KPIs for alert feed
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card critical">
            <div class="kpi-label">Kritisch (7 Tage)</div>
            <div class="kpi-value">{n_crit}</div>
            <div class="kpi-sub">Sofortmaßnahme</div>
        </div>
        <div class="kpi-card warning">
            <div class="kpi-label">Warnung (7 Tage)</div>
            <div class="kpi-value">{n_warn}</div>
            <div class="kpi-sub">Wartung &lt; 14 Tage</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Info (7 Tage)</div>
            <div class="kpi-value">{n_info}</div>
            <div class="kpi-sub">Anomalie erkannt</div>
        </div>
        <div class="kpi-card ok">
            <div class="kpi-label">Vermiedene Kosten</div>
            <div class="kpi-value">{total_savings:,} €</div>
            <div class="kpi-sub">letzte 7 Tage · geschätzt</div>
        </div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Alert-Feed</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">CHRONOLOGISCH · ALLE ML-AUSGABEN UND REGELBASIERTEN WARNUNGEN</div>', unsafe_allow_html=True)

    # Filter buttons
    f1, f2, f3, f4, _ = st.columns([1, 1, 1, 1, 3])
    filters = [("ALLE", f1), ("KRITISCH", f2), ("WARNUNG", f3), ("INFO", f4)]
    for label, col in filters:
        with col:
            is_active = st.session_state.alert_filter == label
            if st.button(label, key=f"f_{label}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.alert_filter = label
                st.rerun()

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Filtered alerts
    if st.session_state.alert_filter == "ALLE":
        filtered = alerts.copy()
    else:
        filtered = alerts[alerts["severity"] == st.session_state.alert_filter].copy()
    filtered = filtered.sort_values("timestamp", ascending=False)

    # Alert rows
    for idx, (_, alert) in enumerate(filtered.iterrows()):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div class="alert-row">
                <div class="alert-time">{alert['timestamp'].strftime('%d.%m. %H:%M')}</div>
                <div>{status_badge(alert['severity'])}</div>
                <div class="alert-truck">{alert['lkw_id']}</div>
                <div>
                    {alert['message']}
                    <div class="alert-meta">Quelle: {alert['source']} · Einsparung: ~ {alert['savings_eur']} €/h</div>
                </div>
                <div class="alert-savings">~ {alert['savings_eur']*4} €</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Details →", key=f"alert_det_{idx}", use_container_width=True):
                go_to_detail(alert["lkw_id"])
                st.rerun()

# ============================================================================
# Router
# ============================================================================
if st.session_state.view == "fleet":
    render_fleet_overview()
elif st.session_state.view == "detail":
    render_truck_detail()
elif st.session_state.view == "alerts":
    render_alert_feed()

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0; color: #B0B0B5;
           font-family: "IBM Plex Mono", "Courier New", monospace; font-size: 0.7rem;
           letter-spacing: 0.1em; border-top: 1px solid #F0F0F2; margin-top: 3rem;'>
    PREMA MVP · HM BIG DATA SS2026 · TEAM 1 · DATEN SIMULIERT · KEIN PRODUKTIVBETRIEB
</div>
""", unsafe_allow_html=True)
