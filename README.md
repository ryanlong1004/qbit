# Python Script Overview

## Description

This script is a CLI application for managing API connections and performing various operations like searching, purging data, and managing torrents.
The application utilizes the `typer` package to handle CLI commands, along with other libraries for logging, API interactions, and data formatting.

## Features

- **Search**: Search for a given term and display the results in CSV format.
- **Add Torrent**: Add a torrent by providing its URL.
- **List Plugins**: Retrieve and display available plugins from the client.
- **Purge Items**: Purge items older than a specified number of days.

## Dependencies

- Python 3.8 or higher
- Libraries:
  - `os`
  - `dotenv`
  - `pandas`
  - `loguru`
  - `qbittorrentapi`
  - `typer`
  - `api_connection` (Custom module)

## Installation

1. Clone the repository containing this script.
2. Install the required Python libraries by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file with the following variables:
   ```
   HOST=your_host
   PORT=your_port
   USERNAME=your_username
   PASSWORD=your_password
   ```

## Usage

### Commands

1. **Search**:

   ```bash
   python script_name.py search "<term>"
   ```

   - Searches for the specified term and displays the results.

2. **Add Torrent**:

   ```bash
   python script_name.py grab "<term>"
   ```

   - Searches for a term and adds the first result as a torrent.

3. **List Plugins**:

   ```bash
   python script_name.py plugins-list
   ```

   - Lists available plugins from the client.

4. **Purge Items**:

   ```bash
   python script_name.py purge <days>
   ```

   - Purges items older than the specified number of days.

5. **Add Torrent by URL**:
   ```bash
   python script_name.py add-torrent "<url>"
   ```
   - Adds a torrent using the given URL.

## Logging

The script uses `loguru` for enhanced logging. Logs provide information about operations, errors, and formatted results.

## Development

Ensure all required dependencies are installed and that you have an operational API to test against.

## License

This project is released under the MIT License.
