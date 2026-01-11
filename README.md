# QR Generator Web App

A web application that generates QR codes and saves them as PNG files to the local filesystem.

## Features

- Generate QR codes from text or URLs
- Download generated QR codes as PNG files
- Delete generated QR codes
- List all generated QR codes

## Architecture

The application consists of:
1. **Backend**: Python Flask web server
2. **Frontend**: HTML, CSS with Bootstrap 5
3. **Storage**: QR codes are saved to `/data` directory

## Requirements

- Python 3.11+
- Docker (optional, for containerized deployment)

## Installation

### Using Docker (Recommended)

```bash
# Build the image
docker build -t qr-generator:latest .

# Run the container
docker run -p 5000:5000 -v /data:/data qr-generator:latest
```

### Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

1. Access the web interface at `http://localhost:5000`
2. Enter text or URL in the input field
3. Click "Generate QR Code"
4. Download or delete generated QR codes as needed

## Directory Structure

```
/data/           # QR code storage directory
app.py          # Main Flask application
templates/      # HTML templates
Dockerfile      # Docker configuration
.github/workflows/build-and-push.yml  # GitHub Actions workflow
```

## GitHub Actions

The project includes a GitHub Actions workflow that:
- Builds the Docker image
- Tags it as `qr-generator:latest`
- Pushes to GitHub Container Registry (GHCR)

## Security Notes

The application stores generated QR codes in `/data` directory. Make sure this directory has appropriate permissions for your deployment environment.

## License

MIT