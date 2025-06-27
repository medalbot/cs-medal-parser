# CS:GO Medal Parser

A high-performance Python application for parsing and downloading CS:GO medals, coins, pins, and badges from the [ByMykel CSGO API](https://github.com/ByMykel/CSGO-API).

## Features

- **High-Performance Processing**: Concurrent downloads with configurable worker threads
- **Intelligent Caching**: Avoids redundant downloads and validates existing images
- **Automatic Image Processing**: Standardizes images to 256×192 resolution with aspect ratio preservation
- **Robust Network Handling**: Connection pooling, retry logic, and timeout management
- **Advanced Logging**: Beautiful structured logging with loguru for enhanced debugging and monitoring
- **Flexible Configuration**: Easily customizable settings via `config.py`

## Quick Start

### Installation

```bash
git clone https://github.com/tom-jm69/cs-medal-parser.git
cd cs-medal-parser
python -m pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

Output files:

- **Images**: `data/medals/*.png` (processed collectible images)
- **API Dumps**: `data/responses/*.json` (timestamped API responses)
- **Logs**: Beautiful console output with loguru (with optional file logging)

## Configuration

Customize behavior in `config.py`:

```python
# Performance settings
MAX_WORKERS = 10          # Concurrent download threads
REQUEST_TIMEOUT = 30      # Network timeout (seconds)
MAX_RETRIES = 3          # Retry attempts for failed requests

# Image processing
TARGET_WIDTH = 256       # Output image width
TARGET_HEIGHT = 192      # Output image height

# Filter types
COLLECTIBLE_TYPES = ["pick", "coin", "medal", "pin", "trophy", "badge", "pass", "stars"]
```

## Docker Deployment

### Pre-built Images (Recommended)

Pull the optimized multi-stage image from Docker Hub:

```bash
# Pull latest version
docker pull kway/cs-medal-parser:latest

# Run directly
docker run --rm -v $(pwd)/data:/app/data kway/cs-medal-parser:latest
```

### Build Locally

```bash
docker build -t cs-medal-parser .
docker run --rm -v $(pwd)/data:/app/data cs-medal-parser
```

### Docker Compose

```bash
docker compose up
```

### Automated Builds

🚀 **Automated Docker Hub builds** are configured via GitHub Actions:

- **Any push**: Builds and pushes branch-specific tags
- **Main branch**: Also gets the `latest` tag
- **Multi-platform**: Supports `linux/amd64` and `linux/arm64`
- **Optimized**: 60-70% smaller images using multi-stage builds

See [Docker Setup Guide](.github/DOCKER_SETUP.md) for configuration details.

### Automated Scheduling

Cron job for 15-minute updates:

```bash
*/15 * * * * docker compose -f /path/to/cs-medal-parser/docker-compose.yml run --rm cs2medalparser >> /var/log/medalparser.log 2>&1
```

## Testing

```bash
# Test regex filtering on cached data
python test-re.py
```

## Performance

- **Concurrent Processing**: ~10x faster image downloads vs sequential approach
- **Smart Resource Management**: Connection pooling and request optimization
- **Failure Resilience**: Automatic retries with exponential backoff
- **Progress Monitoring**: Real-time status updates and completion statistics

## API

This project uses the **ByMykel CSGO API** for collectible data.  
Documentation: [https://bymykel.github.io/CSGO-API/](https://bymykel.github.io/CSGO-API/)

## Requirements

- Python 3.12+
- loguru (for beautiful structured logging)
- Additional dependencies listed in `requirements.txt`

## License

GPL-3.0 License - see [LICENSE](LICENSE) file for details.
