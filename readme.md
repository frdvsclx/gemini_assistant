# Gemini Assistant

A Python-based AI assistant application that integrates Google's Gemini AI model with a local SQLite database for note-taking and event management. The application features a modern GUI built with Tkinter and provides intelligent responses through natural language processing.

## Features

- **AI Chat Interface**: Interactive chat with Google Gemini 2.0 Flash model
- **Note Management**: Create, store, and retrieve notes with timestamps
- **Event Calendar**: Schedule and manage events with dates
- **Smart Summarization**: AI-powered summaries of notes and events
- **Modern GUI**: Clean and intuitive user interface built with Tkinter
- **Local Database**: SQLite database for data persistence
- **Async Processing**: Non-blocking AI responses for better user experience

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key
- Internet connection for AI model access

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gemini_assistant
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - Open `code/assistant.py`
   - Add your Google Gemini API key to the `api_key` variable
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

5. **Run the application**
   ```bash
   python code/main.py
   ```

##  Project Structure

```
gemini_assistant/
├── code/
│   ├── main.py           # Main GUI application
│   ├── assistant.py      # Gemini AI integration
│   ├── dataset.py        # Database operations
│   └── test_api.py       # API testing utility
├── data/
│   └── assistant.db      # SQLite database
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

##  Usage Examples

### Chat Commands
- **Natural Language**: Ask questions directly to Gemini AI
- **Note Management**: 
  - `not ekle: Remember to buy groceries`
  - `notları göster` (Show notes)
- **Event Management**:
  - `etkinlik ekle: Team Meeting - 2024-01-15 14:00`
  - `etkinlikleri göster` (Show events)

##  Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

### Database Configuration
- Database file: `data/assistant.db`
- Tables: `notes`, `calendar`
- Automatic initialization on first run

### Testing API Connection
Run the test script to verify API connectivity:
```bash
python code/test_api.py
```
## 🙏 Acknowledgments

- **Google Gemini**: AI model and API
- **Tkinter**: GUI framework
- **SQLite**: Database engine
- **Python Community**: Open source libraries
