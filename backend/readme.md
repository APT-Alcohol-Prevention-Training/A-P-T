# **Research Chat Bot**

A **simple research-oriented chatbot application** built with the **Flask** framework for the backend and **Next.js** for the frontend. This project includes interactive chat functionality, admin panel features, logging, and model fine-tuning capabilities using a chosen AI model (e.g., GPT-based). It is deployed on Google Cloud Platform (GCP).

---

## **Table of Contents**

1. [Introduction](#introduction)  
2. [Key Features](#key-features)  
3. [Installation & Setup](#installation--setup)  
4. [Environment Variables](#environment-variables)  
5. [Commands & Scripts](#commands--scripts)  
6. [Frontend & Backend Cycle](#frontend--backend-cycle)  
7. [Additional Notes](#additional-notes)  
8. [Contributors](#contributors)  
9. [License](#license)

---

## **Introduction**

**Research Chat Bot** is designed to offer a streamlined, research-focused conversational environment.  
- **Backend**: Python + Flask (with Gunicorn in production)  
- **Frontend**: Next.js (JavaScript/TypeScript)  
- **AI**: GPT-based capable of **fine-tuning**.  
- **Deployment**: Hosted on **Google Cloud Platform (GCP)**.  

**Project Link:** [http://34.68.0.228:3000/](http://34.68.0.228:3000/) (Example)

Date: *December 14, 2024 – January 29, 2025*

---

## **Key Features**

1. **Interactive Chat**  
   - User can type a query; A-P-T expert chatbot responds with AI-generated text.  
   - Real-time or near real-time updates.  

2. **Model Fine-Tuning**  
   - Scripts (`fineTring.py`, `testfineTring.py`) to customize and test GPT-based models with a given dataset (`training_data.jsonl`).  

3. **Admin Panel**  
   - Optional admin or management page (in the backend or a separate Next.js admin route) to view logs, manage configuration, etc.  

4. **Logging**  
   - Logs stored in `logs/` folder for error tracking and usage analytics.  

5. **Deployment on GCP**  
   - Flask server + Next.js frontend accessible at [http://34.68.0.228:3000/](http://34.68.0.228:3000/).  
   - Gunicorn or similar WSGI server recommended in production for Flask.  

---

## **Installation & Setup**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/Research-Chat-Bot.git
cd Research-Chat-Bot
```

### **2. Backend Setup (Flask)**

1. **Create and activate a virtual environment (venv):**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables** (see [Environment Variables](#environment-variables)).
4. **Run the Flask development server** (not for production):
   ```bash
   python main.py
   ```
   - Default: `http://127.0.0.1:8000`

### **3. Frontend Setup (Next.js)**

1. **Install dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```
2. **Run the Next.js development server**:
   ```bash
   npm run dev
   ```
   - Default: `http://localhost:3000`

### **4. Production Deployment**

1. **Use Gunicorn** (or another WSGI server) for Flask:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```
2. **Build Next.js** for production:
   ```bash
   npm run build
   npm start
   ```
3. **Configure GCP firewall** to allow incoming traffic on the ports used (e.g., 3000, 8080).

---

## **Environment Variables**

Create a `.env` file in the `backend/` folder to store secrets and configuration details:

```bash
API_KEY=your-secret-api-key
OPENAI_API_KEY=your-openai-key
DATABASE_URL=mysql://user:password@host:port/dbname
SECRET_KEY=supersecret
FLASK_ENV=production
```

**Note**: Update `app.py` or other scripts to read these variables using `os.getenv("API_KEY")` (and consider using `python-dotenv`).

---

## **Commands & Scripts**

| Command / Script        | Usage                          | Description                                                           |
|-------------------------|--------------------------------|-----------------------------------------------------------------------|
| **Run Application**     | `python app.py`                | Starts the Flask development server                                   |
| **Fine-Tuning**         | `python fineTring.py`          | Fine-tunes a model using `training_data.jsonl`                        |
| **Test Fine-Tuning**    | `python testfineTring.py`      | Tests or validates the fine-tuned model                               |
| **API Model Script**    | `python apimodel.py`           | Runs additional API-related logic (if applicable)                     |
| **Update Requirements** | `pip freeze > requirements.txt` | Updates `requirements.txt` based on current environment               |
| **Next.js Dev**         | `npm run dev`                   | Runs Next.js in development mode (localhost:3000 by default)          |
| **Next.js Build**       | `npm run build`                 | Builds Next.js for production                                        |
| **Next.js Start**       | `npm start`                     | Starts Next.js in production mode on the configured port (3000 by default) |

---

## **Frontend & Backend Cycle**

Below is a simple illustration of how data flows between the **Next.js** frontend and the **Flask** backend:

1. **Frontend** (Next.js) - user inputs text in the chat interface.  
2. That input is sent to the **Backend** (Flask) at `http://<SERVER_IP>:8000` or your chosen port.  
3. **`main.py`** receives the request, processes it (possibly calling GPT or a fine-tuned model).  
4. The **AI Model** returns a response to **`main.py`**, which in turn sends it back to the **Frontend**.  
5. **Frontend** displays the response to the user.

**One full cycle**:  
Frontend → Flask → GPT-based model → Flask → Frontend.

---

## **Additional Notes**

- **Production Deployment**  
  - Set `FLASK_ENV=production` in `.env`.  
  - Use a production server like Gunicorn or uWSGI for Flask.
- **HTTPS**  
  - Configure SSL certificates (e.g., via a load balancer or reverse proxy) for secure connections.
- **Database Integration**  
  - (Optional) If you need persistent data storage, integrate an ORM or direct DB calls.
- **Logging**  
  - Check logs in `logs/` folder for errors or usage stats.

---

## **Contributors**

- **Somy Park (박소미)** – [LinkedIn](https://www.linkedin.com/in/somy-park-4a45b2226/)  
  - **Role**: Backend organization & classification, AI model tuning
- **Sueun Cho (조수은)**  - [LinkedIn](https://www.linkedin.com/in/sueun-cho-625262252/)
  - **Role**: DevOps & AI model tuning
- **Grace Jeonghyun Kim (김정현) Ph.D** – [UMD Directory](https://communication.umd.edu/directory/grace-jeonghyun-kim)
  - **Role**: Project manager

---

## **License**

This project is distributed under the [MIT License](LICENSE). You are free to modify and distribute this software as per the terms detailed in the `LICENSE` file.

---

### **End of README**  
> **Enjoy building and customizing your Research Chat Bot!**  
> For questions or issues, please contact the contributors or open an issue on the repository.