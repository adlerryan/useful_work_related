# Template to Run Scripts

This repository contains a collection of useful Python scripts designed to assist with common work-related tasks. These scripts leverage Flask to create a simple web interface for user interaction. The project is built with modularity in mind, making it easy to extend and build on top of the existing functionalities. Whether you're looking to add new features or adapt the current ones to suit your specific needs, this repository provides a straightforward and clean template to follow. The current functionalities include:

## Features

- **Zip Converter**: Allows users to select files or directories, and zip them into separate `.zip` files.
- **Data Profiling**: Upload `.csv`, `.xlsx`, or `.xls` files to generate a data profiling report that includes column names, fill percentages, unique counts, and data types.
- **Reporting**: Facilitates processing files to extract and interact with unique values from specified columns, allowing for custom reporting.
- **File Renaming and Ordering**: Provides a user interface for listing, renaming, and ordering files in a selected directory.

## Web Interface

The web interface is built using Flask, Bootstrap, and custom CSS, providing a clean and user-friendly environment for running these scripts. Users can select a script from a dropdown menu, and based on the selection, the relevant options and inputs are displayed.

## Setup Instructions

1. Clone this repository.
2. Install the required Python packages.
3. Run the Flask application using the command: `python app.py`.
4. Access the web interface via `http://127.0.0.1:5000` in your browser.

## Folder Structure

- **`app.py`**: The main Flask application that handles routing and script execution.
- **`static/`**: Contains the CSS files used for styling the web interface.
- **`templates/`**: HTML files for the web interface.
- **`uploads/`**: Directory where uploaded files are temporarily stored for processing.
