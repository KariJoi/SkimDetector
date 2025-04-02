# CardGuardian

A web application by [PerryDynamic.com](https://perrydynamic.com) to help users detect illegal card skimming devices using image recognition.

## Features

- **Skimmer Detection**: Use your device's camera to scan and analyze card readers for potential skimming devices
- **Educational Resources**: Learn about different types of skimming devices and how to identify them
- **Reporting System**: Report suspicious devices to help protect others in the community
- **Community Reports**: View skimming devices reported by other users

## Technology Stack

- Flask web framework
- OpenCV for image processing and analysis
- PostgreSQL database for report storage
- Bootstrap for responsive UI design

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - DATABASE_URL - PostgreSQL connection string
   - FLASK_SECRET_KEY - Secret key for Flask session management

4. Run the application:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Development

- The application uses the Model-View-Controller (MVC) pattern
- PostgreSQL database is used for storing report data
- Image processing and skimmer detection algorithms are in the utils directory

## Contact

For questions or support, contact [zakari.perry@perrydynamic.com](mailto:zakari.perry@perrydynamic.com)