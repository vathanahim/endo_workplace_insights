# Endodontist Workplace Insights

A Streamlit web application that helps endodontists and endodontic residents find potential workplaces by providing location-based insights, including population data and average rental prices in specific cities.

🌐 [Live Demo](https://minty-endo-data.streamlit.app/)

## Features

- 🔍 Search for endodontists in any US city
- 📊 View population data for the selected city
- 🗺️ Interactive map visualization of endodontist locations
- 💰 Average rental market data by zip code
- 📱 Mobile-friendly interface

## Project Structure

```
endo_workplace_insights/
├── app.py              # Main Streamlit application
├── helper/             # Helper functions and utilities
│   └── get_data.py     # Data fetching and processing functions
├── data/               # Data files
│   └── uscities.csv.zip # Population data
├── requirements.txt    # Python dependencies
└── LICENSE            # Project license
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/endo_workplace_insights.git
   cd endo_workplace_insights
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter a city name and state abbreviation (e.g., "Greensboro", "NC")
2. Click "Submit" to search for endodontists in that area
3. View the results including:
   - Population data for the city
   - List of endodontists with their locations
   - Interactive map showing practice locations
   - Average rental prices by zip code

## Data Sources

- Endodontist data: [NPI Registry API](https://npiregistry.cms.hhs.gov/)
- Population data: US Census data
- Rental market data: Public rental market statistics

