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

Date: *December 14, 2024 – Present*

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


## Installation & Setup

### Backend (Flask + Poetry)

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/Research-Chat-Bot.git
   cd Research-Chat-Bot/backend
   ```

2. **Install Poetry** (if not already installed)

   Follow the [Poetry installation guide](https://python-poetry.org/docs/#installation).

3. **Install Dependencies**

   Use Poetry to install all dependencies defined in `pyproject.toml`:

   ```bash
   poetry install
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the `backend/` folder (see [Environment Variables](#environment-variables)).

5. **Run the Flask Development Server**

   For development use:

   ```bash
   poetry run python main.py
   ```

   - Default URL: `http://127.0.0.1:8000`

### Frontend (Next.js)

1. **Navigate to the Frontend Folder**

   ```bash
   cd ../frontend
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Run the Next.js Development Server**

   ```bash
   npm run dev
   ```

   - Default URL: `http://localhost:3000`

---

## Environment Variables

In the `backend/` folder, create a `.env` file to store secrets and configuration details:

```ini
API_KEY=your-secret-api-key
OPENAI_API_KEY=your-openai-key
DATABASE_URL=mysql://user:password@host:port/dbname
SECRET_KEY=supersecret
FLASK_ENV=production
```

Your Flask application and related scripts will read these variables using `os.getenv("VARIABLE_NAME")` (with support from [python-dotenv](https://github.com/theskumar/python-dotenv)).

---

## Commands & Scripts

| **Command / Script**          | **Usage**                                           | **Description**                                                          |
|-------------------------------|-----------------------------------------------------|--------------------------------------------------------------------------|
| **Run Application**           | `poetry run python main.py`                         | Starts the Flask development server                                      |
| **Fine-Tuning**               | `poetry run python fineTring.py`                    | Fine-tunes a model using `training_data.jsonl`                           |
| **Test Fine-Tuning**          | `poetry run python testfineTring.py`                | Tests or validates the fine-tuned model                                  |
| **API Model Script**          | `poetry run python apimodel.py`                     | Runs additional API-related logic (if applicable)                        |
| **Update Poetry Dependencies**| `poetry update`                                     | Updates dependencies as per `pyproject.toml`                             |
| **Next.js Development**       | `npm run dev`                                       | Runs Next.js in development mode (localhost:3000 by default)             |
| **Next.js Build**             | `npm run build`                                     | Builds Next.js for production                                            |
| **Next.js Start**             | `npm start`                                         | Starts Next.js in production mode (default port: 3000)                   |

---

## Frontend & Backend Cycle

Data flows through the system as follows:

1. **User Input:** The user types a message in the Next.js chat interface.  
2. **Backend Request:** The frontend sends the input to the Flask backend (e.g., `http://<SERVER_IP>:8000`).  
3. **Processing:** The Flask app (via `main.py`) processes the request—calling the GPT-based model (or a fine-tuned variant) to generate a response.  
4. **Response:** The AI model returns a response to Flask, which then sends it back to the frontend.  
5. **Display:** The frontend displays the chatbot’s response to the user.

---

## Additional Notes

- **Production Deployment:**  
  - Set `FLASK_ENV=production` in your `.env` file.
  - Use a production server like Gunicorn:  
    ```bash
    gunicorn -w 4 -b 0.0.0.0:8080 main:app
    ```
- **HTTPS:**  
  Configure SSL certificates (using a load balancer or reverse proxy) for secure connections.
- **Database Integration:**  
  Integrate an ORM or direct database calls if persistent storage is required.
- **Logging:**  
  Check the `logs/` folder for error logs and usage statistics.
- **File Reorganization:**  
  The project is now organized into modular components for improved maintainability and scalability.

---

## Contributors

- **Somy Park (박소미)** – [LinkedIn](https://www.linkedin.com/in/somy-park-4a45b2226/)  
  *Role:* Backend organization & classification, AI model tuning
- **Sueun Cho (조수은)** – [LinkedIn](https://www.linkedin.com/in/sueun-cho-625262252/)  
  *Role:* DevOps & AI model tuning
- **Grace Jeonghyun Kim (김정현) Ph.D** – [UMD Directory](https://communication.umd.edu/directory/grace-jeonghyun-kim)  
  *Role:* Project Manager

---

## License

This project is distributed under the [MIT License](LICENSE). Feel free to modify and distribute the software as per the terms detailed in the `LICENSE` file.

---

> **Enjoy building and customizing your Research Chat Bot!**  
> For questions or issues, please contact the contributors or open an issue in the repository.
```

---

This revised README now clearly documents your project’s structure, setup (with Poetry for the backend), and overall workflow while ensuring that all instructions are detailed and concise.


---

## Quality Checks & Commands

To ensure the codebase adheres to formatting standards, passes linting, type checks, and other quality gates, use the following commands with Poetry.

### Automatic Formatting & Import Sorting

| **Command**                  | **Description**                                                                                 | **Usage**           |
|------------------------------|-------------------------------------------------------------------------------------------------|---------------------|
| **Format with Black**        | Automatically reformat your code to conform to [Black](https://black.readthedocs.io/).           | `poetry run black .` |
| **Sort Imports with isort**  | Automatically sort and format your imports using [isort](https://pycqa.github.io/isort/).         | `poetry run isort .` |

> **Note:** Running `poetry run black --check .` or `poetry run isort --check-only .` will only check for formatting issues without applying fixes. If files need reformatting, run the commands without the `--check` or `--check-only` flags.

### Testing

| **Command**             | **Description**                                                             | **Usage**             |
|-------------------------|-----------------------------------------------------------------------------|-----------------------|
| **Run Tests**           | Executes all unit tests using [pytest](https://docs.pytest.org/).            | `poetry run pytest`   |

> **Note:** If "no tests ran" appears, ensure your test files are named according to the pytest conventions (e.g., `test_*.py`).

### Linting & Type Checking

| **Command**                      | **Description**                                                                              | **Usage**              |
|----------------------------------|----------------------------------------------------------------------------------------------|------------------------|
| **Lint with Flake8**             | Checks code for linting errors using [Flake8](https://flake8.pycqa.org/en/latest/).           | `poetry run flake8`    |
| **Type Checking with mypy**      | Performs static type checking using [mypy](http://mypy-lang.org/).                           | `poetry run mypy .`    |

### Security Scanning

| **Command**                      | **Description**                                                                                          | **Usage**                  |
|----------------------------------|----------------------------------------------------------------------------------------------------------|----------------------------|
| **Security Scan with Bandit**    | Scans your project for common security issues using [Bandit](https://bandit.readthedocs.io/).             | `poetry run bandit -r .`    |

### Example Workflow

1. **Reformat Code & Sort Imports:**

   Run:
   
   ```
   poetry run black .
   poetry run isort .
   ```

2. **Run Linting & Type Checks:**

   Run:
   
   ```
   poetry run flake8
   poetry run mypy .
   ```

3. **Run Security Scan:**

   Run:
   
   ```
   poetry run bandit -r .
   ```

4. **Execute Tests:**

   Run:
   
   ```
   poetry run pytest
   ```

Following these commands ensures that your code remains consistently formatted, free of linting issues, type-safe, and secure.

