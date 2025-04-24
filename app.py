import streamlit as st
import helper as hp
import pydeck as pdk

st.title("Endodontist Finder for Minty")

with st.form("key='input_city_state'"):
    city = st.text_input("Enter city")
    state = st.text_input("Enter state")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if not city or not state:
        st.error("Please enter both city and state")
    else:
        df = hp.fetch_endodontists_by_city_state(city.lower(), state.lower())
        if df is None or df.empty:
            st.warning(f"No endodontists found in {city.title()}, {state.upper()}")
        else:
            st.success(f"Found {len(df)+1} endodontists in {city.title()}, {state.upper()}")
            st.dataframe(df)
            # Clean and process the data
            df_clean = hp.aggregate_location_data(df)
            df_clean = df_clean[df_clean['latitude'].notna() & df_clean['longitude'].notna()]
            
            if df_clean.empty:
                st.warning("No valid locations found after cleaning the data")
            else:
                # Display the cleaned data
                st.write("Endodontist Locations:")
                # Create and display the map
                layer = pdk.Layer(
                    'ScatterplotLayer',
                    data=df_clean,
                    get_position='[longitude, latitude]',
                    get_radius=1000,
                    get_fill_color=[255, 0, 0, 160],
                    pickable=True
                )

                view_state = pdk.ViewState(
                    latitude=df_clean['latitude'].mean(),
                    longitude=df_clean['longitude'].mean(),
                    zoom=11,
                    pitch=0
                )

                tooltip = {"text": "{name}"}

                st.pydeck_chart(pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    tooltip=tooltip,
                    map_style='mapbox://styles/mapbox/light-v9'
                ))
                
                # Show rent data
                zipcode_list = df_clean['zip_code'].unique().tolist()
                rent_data = hp.get_rent_data(zipcode_list)
                if rent_data is not None and not rent_data.empty:
                    st.write("Average Rental Market Data by Zip Code:")
                    st.dataframe(rent_data, hide_index=True)
                else:
                    st.info("No rent data available for the selected area")


# def main():



# if __name__ == "__main__":
#     main()