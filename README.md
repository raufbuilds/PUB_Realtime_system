# 🔴 PUB Realtime System

A real-time data ingestion and visualization system for Ontario Public Utility Board (PUB) demand data using FastAPI, Streamlit, and Server-Sent Events (SSE).

## 📋 Project Structure

```
PUB_Realtime_system/
├── cleaner/              # CSV data cleaning
│   ├── CSV File Cleaner.ipynb
│   ├── input_.csv_file/  # Place raw CSV files here
│   └── processed_.csv_file/  # Cleaned CSV files
├── client/               # Data sender
│   ├── sender.py
│   └── start_laptop1.bat
├── dashboard/            # Streamlit dashboard
│   ├── dashboard.py
│   └── start_laptop2.bat
├── server/               # FastAPI backend
│   └── app.py
├── config.py             # Centralized configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── setup_env.bat         # Setup script (Windows)
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows (uses `.bat` files), or adapt commands for Linux/Mac

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/raufbuildsi/PUB_Realtime_system.git
   cd PUB_Realtime_system
   ```

2. **Run setup (Windows):**
   ```bash
   setup_env.bat
   ```
   
   Or manually:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment (optional):**
   ```bash
   copy .env.example .env
   # Edit .env with your settings
   ```

### Data Preparation

1. Place raw CSV files in `cleaner/input_.csv_file/`
2. Run the CSV cleaner notebook or script:
   - **Jupyter:** Open `cleaner/CSV File Cleaner.ipynb`
   - **Python:** `python cleaner/CSV_File_Cleaner.py`
3. Processed files will appear in `cleaner/processed_.csv_file/`

### Running the System

**Option 1: Windows Batch Scripts (Automatic)**

Terminal 1 - Start server and sender:
```bash
start_laptop1.bat
```

Terminal 2 - Start dashboard:
```bash
start_laptop2.bat
```

**Option 2: Manual (All Platforms)**

Terminal 1 - Start FastAPI server:
```bash
venv\Scripts\activate
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

Terminal 2 - Send data:
```bash
venv\Scripts\activate
python client/sender.py
```

Terminal 3 - Start Streamlit dashboard:
```bash
venv\Scripts\activate
streamlit run dashboard/dashboard.py
```

## 📊 Features

- **Real-time Data Ingestion:** Send CSV data via HTTP POST
- **Server-Sent Events (SSE):** Live streaming to dashboard
- **Interactive Dashboard:** Multiple visualization modes:
  - Today's demand
  - All dates (multi-line chart)
  - Average profile
  - Today vs Average
  - Last 7 days
  - Latest records table
- **CORS Enabled:** Cross-origin requests supported
- **Environment Configuration:** Easy setup via `.env`

## 🔧 API Endpoints

### Server (`http://localhost:8000`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ingest` | POST | Receive data records |
| `/stream` | GET | SSE stream for real-time data |
| `/health` | GET | Server health check |
| `/docs` | GET | Interactive API documentation |

## 📝 Environment Variables

```env
API_URL=http://127.0.0.1:8000          # API endpoint
SERVER_IP=127.0.0.1                    # Server IP for dashboard
SERVER_PORT=8000                       # Server port
REQUEST_DELAY=1                        # Seconds between sender requests
CORS_ORIGINS=*                         # Allowed origins
```

## 🛠️ Configuration

Edit `config.py` to customize:
- Directory paths
- API URLs and ports
- CSV column names
- Request delays

## 📦 Dependencies

See `requirements.txt`:
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Streamlit** - Dashboard framework
- **Pandas** - Data processing
- **Plotly** - Interactive charts
- **Requests** - HTTP client
- **SSE-Starlette** - Server-Sent Events

## 🐛 Troubleshooting

### CSV file not found
- Ensure raw CSV files are in `cleaner/input_.csv_file/`
- Run the CSV cleaner before sender

### Connection refused
- Verify server is running: `uvicorn server.app:app --host 0.0.0.0 --port 8000`
- Check `API_URL` and `SERVER_IP` in `.env`

### Dashboard not connecting
- Ensure server is running and accessible
- Check `STREAM_URL` in dashboard logs
- Verify firewall allows port 8000

## 📄 License

MIT License

## 👤 Author

Rauf Builds

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
