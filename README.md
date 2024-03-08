# sqlalchemy-challenge

# Module 10 challenge

## Overview
This project conducts analysis of climate data for Hawaii. The analysis includes precipitation analysis, station analysis, temperature observation analysis, and a temperature statistics API. The dataset includes measurements from various stations across Hawaii. There is also an interactive flask project for the seconf part of this project.

### Files
- `climate.ipynb`: Jupyter Notebook containing the climate data analysis including visualizations.
- `app.py`: Python Flask application providing an API for accessing the results of the climate data analysis.
- `hawaii_measurements.csv`: Temp, rain, and date data recorded by stations
- `hawaii_stations.csv`: General data about the weather stations in Hawaii. 

## Installation

### Requirements
- Python 3.7 or later
- Libraries: `numpy`, `pandas`, `datetime`, `sqlalchemy`, `matplotlib`, and `flask`. Installation commands are provided below.
- A SQLite database named `hawaii.sqlite` located in a `Resources` folder.

### Setup
1. Clone this repository to your local machine.
2. Ensure you have Python 3.7 or later installed.
3. Install required Python libraries by running: `pip install numpy pandas matplotlib flask sqlalchemy`.
4. Place your `hawaii.sqlite` database in the `Resources` folder relative to the `app.py` script.

## Usage

### Running the Analysis Notebook
1. Navigate to the directory containing `climate.ipynb`.
2. Start Jupyter Notebook or JupyterLab, and open `climate.ipynb`.
3. Execute the cells in sequence to perform the climate data analysis.

### Starting the Flask API
1. Navigate to the directory containing `app.py`.
2. Run the command: `python app.py` to start the Flask server.
3. Access the API at `http://127.0.0.1:5000/` in your web browser. Available routes will be listed on the homepage.

## Flask Route Endpoints
- `/`: Home page listing all available routes.
- `/api/v1.0/precipitation`: Returns JSON data about precipitation for the last 12 months.
- `/api/v1.0/stations`: Returns a JSON list of weather stations in the dataset.
- `/api/v1.0/tobs`: Returns JSON data about temperature observations for the most active station over the last year.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returns JSON data about the minimum, average, and maximum temperatures between the given start date or date range.
