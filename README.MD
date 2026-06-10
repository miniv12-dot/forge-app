# 🦅 Forge | Mental Operating System for Men

Forge is a full-stack, data-driven web application designed to help men track physical habits, identify silent burnout, and access science-backed mental health protocols. 

Unlike traditional journaling apps, Forge utilizes a correlation engine to map physical exertion against mental clarity and features a fully anonymous, server-randomized community hub.

## 🚀 The Tech Stack
* **Backend:** Python, Django, Django REST Framework
* **Database:** PostgreSQL / SQLite
* **Authentication:** JWT (JSON Web Tokens)
* **Frontend:** HTML5, Modern CSS3 (Glassmorphism UI), Vanilla JavaScript
* **Architecture:** REST API decoupled from a dynamic Single Page Application (SPA) interface.

## 🧠 Core System Architecture

### 1. The Action Calendar (Heatmap Engine)
A dynamic JavaScript frontend that fetches JSON data from the Django REST API to render a predictive heatmap. It cross-references hours of sleep, training completion, and cortisol/stress levels to flag high-risk burnout days with UI indicators.

### 2. The Personalization Engine
A lightweight client-side algorithm that evaluates the user's daily telemetry (Sleep, Stress, Energy). Based on specific thresholds, the engine dynamically injects personalized, highly tactical "Protocols" (e.g., Deep Sleep Rescue, Cortisol Flush) directly into the user's dashboard.

### 3. The Anonymity Engine (Secure Feed)
A secure community feed where users can share strategies without stigma. The backend strips personal identifiers and assigns randomized, encrypted aliases to foster a zero-judgment environment.

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/forge-app.git](https://github.com/YOUR_USERNAME/forge-app.git)
   cd forge-app

2. Install dependencies:

Bash
pip install -r requirements.txt

3. Run database migrations:

Bash
python manage.py migrate

4. Start the Forge Server:

Bash
python manage.py runserver

5. Navigate to http://127.0.0.1:8000/ in your browser.

