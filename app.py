import streamlit as st
import helper as hp
import pydeck as pdk

st.title("Endodontist Finder for Minty")

with st.form("key='input_city_state'"):
    city = st.text_input("Enter city")
    state = st.text_input("Enter state")
    submit_button = st.form_submit_button("Submit")

col1, col2 = st.columns(2)

if submit_button:
    df = hp.fetch_endodontists_by_city_state(city.lower(), state.lower())
    if df is not None:
        df_clean = hp.aggregate_location_data(df)
        df_clean = df_clean[df_clean['latitude'].notna() & df_clean['longitude'].notna()]
        st.write(df)
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=df_clean,
            get_position='[longitude, latitude]',
            get_radius=1000,  # Size in meters
            get_fill_color=[255, 0, 0, 160],
            pickable=True
        )

        # Define view
        view_state = pdk.ViewState(
            latitude=df_clean['latitude'].mean(),
            longitude=df_clean['longitude'].mean(),
            zoom=11,
            pitch=0
        )

        # Tooltip on hover
        tooltip = {"text": "{name}"}

        # Render map
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style='mapbox://styles/mapbox/light-v9'
        ))
    zipcode_list = df_clean['zip_code'].unique().tolist()
    rent_data = hp.get_rent_data(zipcode_list)
    st.write(rent_data)


# def main():



# if __name__ == "__main__":
#     main()