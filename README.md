# ollama-CLI-AIassistante - Intelligent Chatbot with Ollama Integration

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)

A sophisticated AI chatbot application that integrates with Ollama for local AI model inference, featuring user authentication, chat history management, and real-time system monitoring.

## 🚀 Features

- **🤖 AI Integration**: Powered by Ollama with DeepSeek-R1 7B model
- **🔐 User Authentication**: Secure login/signup system with password hashing
- **💾 Chat History**: Persistent conversation storage with SQLite database
- **📊 System Monitoring**: Real-time CPU, RAM, and performance metrics
- **🎨 Rich Terminal UI**: Beautiful console interface with Rich library
- **⚙️ Customizable Settings**: Adjustable AI parameters (temperature, token limits)
- **🔄 Streaming Responses**: Real-time AI response streaming
- **🛡️ Graceful Shutdown**: Proper cleanup and signal handling

## 📁 Project Structure

```
ai_talk/
├── main.py          # Entry point and application orchestrator
├── Artificial.py    # Core AI engine and chat management
├── login.py         # User authentication and database management
├── history.py       # Chat history operations and display
├── requirements.txt # Python dependencies
└── README.md       # Project documentation
```

## 📄 File Descriptions

### 🎯 `main.py`
**Purpose**: Application entry point and system initialization
- Initializes the AI chatbot instance
- Sets up signal handlers for graceful shutdown
- Manages admin privileges (Windows-specific)
- Configures system prompt and starts the main loop

### 🧠 `Artificial.py`
**Purpose**: Core AI engine and chat management system
- **AI Integration**: Manages Ollama server connection and model inference
- **Performance Monitoring**: Tracks CPU usage, memory consumption, and token generation rates
- **Chat Management**: Handles conversation flow and message processing
- **System Optimization**: CPU affinity settings and process priority management
- **User Interface**: Rich terminal formatting and interactive prompts
- **Configuration**: AI parameter adjustment (temperature, top_p, max_tokens)

### 🔐 `login.py`
**Purpose**: Secure user authentication and database management
- **User Registration**: Account creation with secure password hashing
- **Authentication**: Login verification using PBKDF2 with SHA-256
- **Database Schema**: SQLite tables for users and chat history
- **Security**: Salt generation and password protection
- **Session Management**: Current user state tracking

### 📚 `history.py`
**Purpose**: Chat history operations and display management
- **History Storage**: Save conversations to SQLite database
- **History Retrieval**: Load previous chat sessions
- **Interactive Display**: Rich table formatting for chat history
- **User Control**: Optional history saving with user confirmation
- **Data Persistence**: Link chat history to authenticated users

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and configured
- DeepSeek-R1 7B model downloaded in Ollama

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/PIRATE-E/ai_talk.git
   cd ai_talk
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   
   # Pull the DeepSeek model
   ollama pull deepseek-r1:7b
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 🎮 Usage

### First Time Setup
1. **Authentication**: Choose to login or create a new account
2. **AI Configuration**: Select output personality and response length
3. **History Review**: View previous conversations (if any)

### Chat Interface
- Enter your queries when prompted
- Type `exit(0)` to quit the application
- Choose whether to save chat history before exiting

### AI Configuration Options
- **Output Type**: 
  - `random` (temperature: 1.0) - Creative and varied responses
  - `strict` (temperature: 0.0) - Focused and deterministic responses
  - `intermediate` (temperature: 0.5) - Balanced responses
- **Response Length**:
  - `short` (200 tokens) - Concise answers
  - `long` (1500 tokens) - Detailed explanations
  - `extreme` (2000 tokens) - Comprehensive responses

## 🔧 Configuration

### AI Parameters
The application allows customization of various AI parameters:

```python
# Temperature: Controls randomness (0.0 - 1.0)
# Top-p: Nucleus sampling parameter (0.0 - 1.0)
# Max Tokens: Maximum response length
# Keep Alive: Model persistence setting
```

### System Optimization
- **CPU Affinity**: Binds Ollama process to all available cores
- **Process Priority**: Sets real-time priority for optimal performance
- **Memory Monitoring**: Tracks RAM usage of both Python and Ollama processes

## 📊 Performance Metrics

The application provides real-time performance information:
- **Response Time**: Time taken to generate each response
- **Memory Usage**: RAM consumption by the application and Ollama
- **Tokens Per Second**: AI model inference speed
- **System Resource Utilization**: CPU and memory monitoring

## 🔒 Security Features

- **Password Hashing**: PBKDF2 with SHA-256 and random salt
- **Secure Storage**: Encrypted password storage in SQLite
- **Session Management**: Secure user session handling
- **Input Validation**: Protected against common security vulnerabilities

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    hashed_password TEXT,
    salt TEXT
);
```

### Chat History Table
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    prompt TEXT,
    response TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
);
```

## 🚨 Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues with Ollama
- Database connection problems
- System resource constraints
- User input validation
- Graceful shutdown on interrupts

## 🛠️ Development

### Dependencies
- `ollama`: AI model integration
- `rich`: Terminal UI and formatting
- `psutil`: System monitoring and process management
- Standard library modules for core functionality

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support, please open an issue on the GitHub repository or contact the maintainer.

## 🔮 Future Enhancements

- [ ] Support for multiple AI models
- [ ] Web interface option
- [ ] Export chat history to various formats
- [ ] Plugin system for extensions
- [ ] Multi-language support
- [ ] Voice input/output capabilities

---

**Created by**: PIRATE-E  
**Last Updated**: June 23, 2025  
**Version**: 1.0.0
