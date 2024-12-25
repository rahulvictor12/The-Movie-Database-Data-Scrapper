# The Movie DataBase Movie Data Scraper

## Description
This project is a Python-based web scraper designed to extract movie-related information from [The Movie Database (TMDB)](https://www.themoviedb.org). Using libraries like `requests` and `BeautifulSoup`, it collects data such as movie titles, ratings, genres, and cast details. The extracted data is organized into structured formats using Pandas and exported to a CSV file for further analysis.

## Features
- **Web Scraping**: Extracts movie details from multiple pages of the TMDB website.
- **Data Storage**: Combines data into Pandas DataFrames and exports as CSV.
- **Error Handling**: Implements robust mechanisms for handling request failures.
- **Reusable Functions**: Includes modular user-defined functions for easy extensibility.

## Prerequisites
Ensure you have the following installed:
- Python 3.7+
- Pip (Python package manager)

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd tmdb-movie-data-scraper
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Usage

### 1. Scrape Data
The script fetches data from the first 6 pages of TMDB and combines the results into a single CSV file.

### 2. Modify Parameters
You can customize the number of pages to scrape or adjust headers by editing the `main.py` script.

### 3. Output
The combined movie data is saved as `Combined_Data.csv` in the project directory.

## Outputs
- **CSV File**: Contains the following columns:
  - Title
  - Rating
  - Genre(s)
  - Cast

Example output:
| Title              | Rating | Genres         | Cast              |
|--------------------|--------|----------------|-------------------|
| The Shawshank...  | 9.3    | Drama, Crime   | Tim Robbins, ...  |
| The Godfather      | 9.2    | Drama, Crime   | Marlon Brando,... |

## Built With
- Python
- Requests
- BeautifulSoup
- Pandas

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [The Movie Database (TMDB)](https://www.themoviedb.org) for providing the data.

