# General application settings
APP_NAME = "Impetus AI"
VERSION = "1.0.0"
DEBUG_MODE = True

# Networking settings
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 65432
CONNECTION_TIMEOUT = 30  # in seconds
MAX_CONNECTIONS = 100

# Logging settings
LOG_FILE = "logs/app.log"
LOG_LEVEL = "INFO"

# API settings
API_BASE_URL = "https://api.impetus.ai"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # in seconds

# Security settings
ENABLE_SSL = True
SSL_CERTIFICATE_PATH = "certs/server.crt"
SSL_KEY_PATH = "certs/server.key"

# Performance settings
MONITOR_INTERVAL = 10  # seconds between monitoring cycles
MAX_DATA_BUFFER = 4096  # bytes
