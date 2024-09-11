
# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

## Project Overview
This project automates the collection, analysis, and visualization of bus travel data from Redbus, aiming to revolutionize the transportation industry. It uses Selenium for web scraping, SQL for data storage, and Streamlit for creating an interactive data filtering application.

## Features
- Automated data scraping from Redbus website
- Collection of bus routes, schedules, prices, and seat availability
- SQL database for efficient data storage
- Interactive Streamlit application for data visualization and filtering
- User-friendly interface for exploring bus travel options

## Technologies Used
- Python
- Selenium (for web scraping)
- MySQL (for data storage)
- Streamlit (for the web application)
- Pandas (for data manipulation)

## Project Structure
- `redbus_multiple_url.ipynb`: Python script for web scraping using Selenium
- `redbus_streamlit.py`: Streamlit application for data visualization and filtering
- `entire_transport_routes.csv`: CSV file containing scraped route data

## Installation and Setup
1. Clone the repository:
   ```
   git clone https://github.com/your-username/redbus-data-scraping.git
   ```
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up MySQL database and update connection details in `redbus_streamlit.py`

## Usage
1. Run the web scraping script:
   ```
   python redbus_multiple_url.ipynb
   ```
2. Launch the Streamlit application:
   ```
   streamlit run redbus_streamlit.py
   ```
3. Use the sidebar to select preferences and filter bus options

## Screenshots
![Redbus Streamlit Application](path/to/your/screenshot.png)

## Future Improvements
- Implement real-time data updates
- Expand to include more transportation providers
- Enhance data visualization with interactive charts and maps

## Contributing
Contributions to improve the project are welcome. Please fork the repository and submit a pull request with your changes.

## Acknowledgments
- Redbus for providing the data source
- Streamlit community for their excellent documentation and examples
          
