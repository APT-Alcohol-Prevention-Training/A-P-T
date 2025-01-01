# Research Chat Bot

A simple research-oriented chatbot application built with the Flask framework. This project includes interactive chat functionality, admin panel features, logging, and model fine-tuning capabilities.

---

## Table of Contents

1. [Project Structure](#project-structure)  
2. [Key Features](#key-features)  
3. [Installation & Setup](#installation--setup)  
4. [Environment Variables](#environment-variables)  
5. [Commands & Scripts](#commands--scripts)  
6. [Additional Notes](#additional-notes)  
7. [License](#license)

---

## Project Structure

```bash
RESEARCH-CHAT-BOT/
├── .git/                 # Git repository folder
├── logs/                 # Folder to store log files
├── static/               # Static files (CSS, JS, images, etc.)
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   └── bot_face.png
│   └── js/
│       └── scripts.js
├── templates/            # Flask templates (HTML files)
│   ├── admin.html
│   ├── chat.html
│   └── home.html
├── uploads/              # Folder for uploaded files
├── .env                  # Environment variable settings (e.g., API keys)
├── .gitignore
├── apimodel.py           # API logic for model interaction
├── app.log               # Application log file
├── app.py                # Main Flask application entry point
├── config.json           # Configuration file (optional)
├── fine-tuning.txt       # Notes for fine-tuning (optional)
├── fineTring.py          # Script to perform model fine-tuning
├── secretFlask.py        # Secret or private Flask settings (optional)
├── testfineTring.py      # Script to test the fine-tuned model
└── training_data.jsonl   # Dataset for model fine-tuning (JSONL format)

## Commands & Scripts

| Command / Script        | Usage                          | Description                                               |
|-------------------------|--------------------------------|-----------------------------------------------------------|
| **Run Application**     | `python app.py`               | Starts the Flask development server                       |
| **Fine-Tuning**         | `python fineTring.py`          | Fine-tunes a model using `training_data.jsonl`            |
| **Test Fine-Tuning**    | `python testfineTring.py`      | Tests or validates the fine-tuned model                   |
| **API Model Script**    | `python apimodel.py`           | Runs additional API-related logic (if applicable)         |
| **Update Requirements** | `pip freeze > requirements.txt`| Updates `requirements.txt` based on current environment   |

---

## Additional Notes

### Production Deployment
In production, set `FLASK_ENV` to `production` and consider using a production-grade WSGI server (e.g., Gunicorn, uWSGI).

### HTTPS
For secure connections, configure an SSL certificate and enable HTTPS redirection in your production environment.

### Template / Static File Customization
Edit the HTML files in `templates/` to modify the UI and layout.  
Adjust files in `static/css/`, `static/js/`, and `static/images/` for styling or branding.

### Database Integration
While this example does not require a database, you can incorporate one (e.g., SQLite, PostgreSQL, MySQL) for storing logs, sessions, or training data.

### Reporting Errors / Bugs
Check `logs/` for error and usage logs.  
Report bugs or submit feedback via the project’s Issue tracker.

---

## License

This project is distributed under the MIT License. See `LICENSE` for details (add or modify as you see fit).
