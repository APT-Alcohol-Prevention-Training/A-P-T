# **Alcohol Prevention Training (APT) Chat Bot**

An interactive web application designed for alcohol awareness and prevention education, targeting young adults aged 18-20. This application combines AI-powered chatbots, interactive assessments, and scenario-based training to provide personalized guidance on responsible decision-making.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Installation & Setup](#installation--setup)
5. [Environment Variables](#environment-variables)
6. [API Endpoints](#api-endpoints)
7. [Session Management](#session-management)
8. [Security Features](#security-features)
9. [Development](#development)
10. [Deployment](#deployment)
11. [Contributors](#contributors)
12. [License](#license)

---

## **Overview**

The **APT Chat Bot** is an educational platform that helps young adults make informed decisions about alcohol consumption through:
- Interactive conversations with AI personas
- Risk assessment questionnaires
- Real-world scenario training
- Personalized feedback and guidance

**Tech Stack:**
- **Backend**: Python 3.11+ with Flask
- **Frontend**: Next.js 15.1.3 with React 19
- **AI**: OpenAI GPT-3.5/GPT-4
- **Database**: CSV-based session storage
- **Deployment**: Google Cloud Platform

---

## **Key Features**

### 1. **Multi-Persona AI Chatbots**
Three distinct chatbot personalities to engage different user preferences:
- **AI Assistant**: Informal, friendly, and approachable
- **Student Peer**: Inquisitive, energetic, relatable
- **Doctor/Professional**: Formal, knowledgeable, authoritative

### 2. **Interactive Assessment Flow**
- Age verification (18-20 target demographic)
- Drinking habit questionnaire
- Risk score calculation (0-20 scale)
- Personalized recommendations based on responses

### 3. **Scenario-Based Training**
Real-world situations with interactive feedback:
- **Party Scenario**: Handling peer pressure when offered drinks
- **Concert Pre-game**: Setting boundaries before events
- **Date Scenario**: Maintaining choices in social settings

### 4. **Session Management System**
- UUID-based session tracking
- Individual CSV logs per user session
- Conversation history with timestamps
- Risk scores and scenario responses tracking

### 5. **Admin Dashboard**
- Protected admin panel for session management
- Download individual or bulk session data
- Real-time session monitoring
- CSV export for analysis

---

## **Architecture**

```
research-chat-bot/
├── backend/
│   ├── app/
│   │   ├── __init__.py         # Flask app factory
│   │   └── routes.py           # API endpoints
│   ├── auth/
│   │   └── authmanager.py      # Authentication system
│   ├── chatbot/
│   │   └── chatbot.py          # OpenAI integration & scenarios
│   ├── logger/
│   │   ├── custom_logger.py    # Legacy logging system
│   │   ├── session_logger.py   # Session-based CSV logging
│   │   └── session_logs/       # CSV storage directory
│   ├── templates/
│   │   └── sessions.html       # Admin dashboard UI
│   ├── assessment_data.json    # Assessment questions
│   ├── validators.py           # Input validation & sanitization
│   ├── main.py                 # Application entry point
│   ├── .env                    # Environment variables
│   └── pyproject.toml          # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── [role]/page.js      # Dynamic chat interface
│   │   ├── api/chat/route.js   # API proxy
│   │   └── page.js             # Landing page
│   ├── components/
│   │   └── ChooseAvatar.js     # Avatar selection
│   ├── public/
│   │   └── training_data.json  # Scenario content
│   └── package.json            # Node dependencies
└── README.md
```

---

## **Installation & Setup**

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Poetry (Python package manager)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/APT-Alcohol-Prevention-Training/research-chat-bot.git
   cd research-chat-bot/backend
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Configure environment variables**
   ```bash
   # Edit .env with your configuration
   ```

4. **Run the Flask server**
   ```bash
   poetry run python main.py
   ```
   The backend will start on `http://localhost:8080`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   The frontend will start on `http://localhost:3000`

---

## **Environment Variables**

Create a `.env` file in the `backend/` directory:

```env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here

# Admin Authentication
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_DEFAULT_MODEL=gpt-3.5-turbo
```

---

## **API Endpoints**

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/` | Main chatbot interaction |
| POST | `/api/get_assessment_step` | Get assessment questions |

### Protected Endpoints (Require Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sessions` | List all sessions |
| GET | `/download_session/<session_id>` | Download specific session CSV |
| GET | `/download_all_sessions` | Export all sessions as CSV |
| GET | `/session_management` | Admin dashboard UI |
| GET | `/download_logs` | Download legacy logs |

### Request/Response Examples

**Chat Interaction**
```json
POST /
{
  "message": "Hello",
  "chatbot_type": "ai",
  "risk_score": 5,
  "conversation_context": {
    "party_scenario": 1
  }
}

Response:
{
  "bot_response": "Hey there! How can I help you today?",
  "session_id": "uuid-here"
}
```

---

## **Session Management**

### Session Data Structure

Each session CSV contains:
- `session_id`: Unique identifier
- `timestamp`: Conversation timestamp
- `conversation_number`: Sequential message count
- `chatbot_type`: Selected persona (ai/student/doctor)
- `user_message`: User input
- `bot_response`: AI response
- `user_ip`: Client IP address
- `risk_score`: Assessment score (0-20)
- `scenario`: Active scenario number

### Admin Dashboard

Access the session management dashboard at:
```
http://localhost:8080/session_management
```

Features:
- View active and completed sessions
- Download individual session CSVs
- Export all sessions for analysis
- Real-time session monitoring

---

## **Security Features**

### Input Validation
- HTML/script tag removal
- SQL injection prevention
- XSS protection
- Unicode security character filtering
- Length limitations on all inputs

### Authentication
- HTTP Basic Auth for admin routes
- Environment-based credentials
- Session-based user tracking

### CORS Configuration
```python
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://34.31.208.12:3000",
    "https://34.31.208.12:3000"
]
```

---

## **Development**

### Code Quality Tools

**Linting and Formatting**
```bash
poetry run ruff check .        # Lint code
poetry run ruff format .       # Format code
poetry run pyright            # Type checking
```

**Testing**
```bash
poetry run pytest             # Run tests
poetry run pytest -v          # Verbose output
```

### Project Structure Guidelines
- Follow Google Python Style Guide
- Use type hints where applicable
- Maintain comprehensive docstrings
- Keep functions focused and testable

---

## **Deployment**

### Production Considerations

1. **Environment Setup**
   - Set `FLASK_ENV=production`
   - Use strong secret keys
   - Enable HTTPS

2. **Server Configuration**
   ```bash
   # Using Gunicorn
   poetry run gunicorn -w 4 -b 0.0.0.0:8080 main:app
   ```

3. **Frontend Build**
   ```bash
   npm run build
   npm start
   ```

### Google Cloud Platform Deployment

The application is designed for GCP deployment with:
- Compute Engine for hosting
- Cloud Storage for logs
- Load Balancer for HTTPS
- Firewall rules for security

---

## **Contributors**

- **Grace Jeonghyun Kim, Ph.D** – [UMD Directory](https://communication.umd.edu/directory/grace-jeonghyun-kim)  
  *Role:* Project Manager & Research Lead

- **Somy Park (박소미)** – [LinkedIn](https://www.linkedin.com/in/somy-park-4a45b2226/)  
  *Role:* Backend Development & AI Integration

- **Sueun Cho (조수은)** – [LinkedIn](https://www.linkedin.com/in/sueun-cho-625262252/)  
  *Role:* DevOps & System Architecture

---

## **License**

This project is distributed under the [MIT License](LICENSE). See the `LICENSE` file for details.

---

> **Making responsible choices, one conversation at a time.**  
> For questions or support, please contact the development team or open an issue in the repository.