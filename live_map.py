import streamlit as st
import pandas as pd
import plotly.express as px

from opensky_client import get_live_aircraft


st.set_page_config(
    page_title="AeroGuardian AI - Live Aviation",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ AeroGuardian AI")
st.subheader("Real-Time Aircraft Monitoring")

st.info(
    "🛰️ Live aircraft data is retrieved from the OpenSky Network. "
    "This is a research and educational decision-support dashboard."
)

# -----------------------------
# Refresh
# -----------------------------

if st.button("🔄 Refresh Live Aircraft Data", width="stretch"):

    try:
        aircraft = get_live_aircraft()

        st.success(
            f"✅ Live data received — {len(aircraft)} aircraft detected"
        )

        # Remove aircraft without coordinates
        aircraft_with_position = [
            plane
            for plane in aircraft
            if plane["latitude"] is not None
            and plane["longitude"] is not None
        ]

        if not aircraft_with_position:
            st.warning("No aircraft with valid positions found.")
            st.stop()

        df = pd.DataFrame(aircraft_with_position)

        # -----------------------------
        # Statistics
        # -----------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "✈️ Aircraft",
            len(df)
        )

        airborne = len(
            df[df["on_ground"] == False]
        )

        col2.metric(
            "🛫 Airborne",
            airborne
        )

        countries = df["country"].nunique()

        col3.metric(
            "🌍 Countries",
            countries
        )

        avg_altitude = df["baro_altitude"].dropna().mean()

        if pd.notna(avg_altitude):
            avg_altitude_km = avg_altitude / 1000
            altitude_text = f"{avg_altitude_km:.1f} km"
        else:
            altitude_text = "N/A"

        col4.metric(
            "📏 Avg Altitude",
            altitude_text
        )

        st.divider()

        # -----------------------------
        # Live Map
        # -----------------------------

        st.subheader("🌍 Live Aircraft Map")

        fig = px.scatter_geo(
            df,
            lat="latitude",
            lon="longitude",
            hover_name="callsign",
            hover_data={
                "country": True,
                "baro_altitude": True,
                "velocity": True,
                "heading": True,
                "latitude": False,
                "longitude": False,
            },
            projection="natural earth",
            title="Real-Time Aircraft Positions",
        )

        fig.update_traces(
            marker=dict(
                size=7,
                opacity=0.85,
            )
        )

        fig.update_layout(
            height=650,
            margin=dict(
                l=0,
                r=0,
                t=50,
                b=0,
            ),
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        # -----------------------------
        # Aircraft Table
        # -----------------------------

        st.subheader("📡 Live Aircraft Data")

        display_df = df[
            [
                "callsign",
                "country",
                "latitude",
                "longitude",
                "baro_altitude",
                "velocity",
                "heading",
                "on_ground",
            ]
        ].copy()

        display_df.columns = [
            "Callsign",
            "Country",
            "Latitude",
            "Longitude",
            "Altitude (m)",
            "Speed (m/s)",
            "Heading (°)",
            "On Ground",
        ]

        st.dataframe(
            display_df,
            width="stretch",
            height=400,
        )

    except Exception as e:

        st.error(
            f"❌ Unable to retrieve live aviation data: {e}"
        )

else:

    st.warning(
        "Click **Refresh Live Aircraft Data** to load real aircraft positions."
    )


st.divider()

st.caption(
    "AeroGuardian AI • Research & Educational Decision Support • "
    "Not for flight control or operational use."
)