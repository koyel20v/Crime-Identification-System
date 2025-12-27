🚔 Crime Classification & Monitoring System

An integrated web-based system that allows police officers to register, log in, file crime reports, and automatically classify crimes using a hybrid AI model (FastAPI + BERT).
Admins and officers can monitor, update, and visualize crime data using an interactive dashboard connected to MySQL.

🧩 Project Architecture

Frontend (Live Server)
│
├── HTML / CSS / JS
│   ├── index.html       → Login / Signup
│   ├── report.html      → File new reports
│   ├── dashboard.html   → View stats, charts, reports
│
├── Backend - Node.js (Port 5000)
│   └── server.js        → API for auth, MySQL access, connects to FastAPI
│
└── ML API - FastAPI (Port 8000)
    └── app.py           → AI model (BERT) for automatic crime classification

 
 
 
⚙️ Features


👮 Officer Side

Officer registration and login

File a new crime report with AI-based classification

View and update case status (Pending / Investigating / Resolved)

View personal reports and history


🧠 Machine Learning Integration

Uses a hybrid approach:

Keyword-based detection for speed

BERT model for NLP-based crime classification

Returns predicted crime type and IPC section


📊 Dashboard Features

Total, Pending, Resolved Cases

Top Crimes by City

Crime Types Distribution

Recent Reports

Monthly Trends

Cases grouped by status and severity   


🛠️ Tech Stack

Layer	Technology
Frontend	HTML5, CSS3, JavaScript
Backend API	Node.js + Express
AI/ML API	FastAPI (Python), Transformers (BERT), Pydantic
Database	MySQL
Authentication	JWT (JSON Web Token)
Styling	Vanilla CSS or Bootstrap
Data Visualization	Chart.js (on dashboard.html)

⚡ Installation Guide
1️⃣ Clone the repository

git clone https://github.com/your-username/crime-system.git
cd crime-system

2️⃣ Setup MySQL Database

3️⃣ Setup Backend (Node.js)

cd backend
npm install express cors mysql2 dotenv bcryptjs jsonwebtoken axios

Create a .env file:
PORT=5000
JWT_SECRET=your_secret_key
DB_HOST=localhost
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=crime_system
ML_API_URL=http://127.0.0.1:8000/predict


Start the backend:

**node server.js
**
4️⃣ Setup Machine Learning API (FastAPI)

cd ml-api
pip install fastapi uvicorn transformers torch joblib mysql-connector-python

Run the FastAPI server:

**uvicorn app:app --reload --port 8000
**

5️⃣ Run the Frontend

Open index.html using Live Server in VS Code.

Make sure ports align:

Frontend: 5500 (Live Server)

Node.js Backend: 5000

FastAPI: 8000

🔐 Authentication Flow

Officer signs up → saved to officers table.

Officer logs in → JWT token returned and stored in localStorage.

Token used for authenticated operations (reporting, viewing dashboard).

Logout clears session and redirects to login page.


// try these

💰 Theft (IPC 378)

Someone broke into a parked car and stole a laptop bag and some cash while the owner was shopping in a mall.

🏦 Robbery (IPC 392)

Three masked men robbed a jewelry store at gunpoint and escaped with gold ornaments worth ₹20 lakh.

👊 Assault (IPC 351)

During a dispute over a parking space, a man attacked another person with a stick causing minor injuries.

🏠 House Trespass (IPC 442)

A stranger was caught entering a house compound late at night without permission and was found trying to open the back door.

💳 Fraud (IPC 323)

(Note: This IPC might actually be “Voluntarily Causing Hurt”, but following your mapping:)

The accused promised to double people’s money through an investment scheme but later disappeared with all the deposits.

🚗 Accident Causing Death by Negligence (IPC 304A)

A speeding car hit a pedestrian at a zebra crossing, resulting in the victim’s death on the spot.

⚖️ Rape (IPC 376)

A young woman filed a complaint against her colleague alleging sexual assault inside an office premises after office hours.

🧾 Cheating (IPC 420)

The suspect sold a fake gold chain to the victim claiming it was real gold and took ₹15,000.

👶 Kidnapping (IPC 363)

A 10-year-old child was kidnapped from a playground; the family later received a ransom call.

🧠 Criminal Breach of Trust (IPC 406)

The employee took company funds to deposit in the bank but used the money for personal expenses instead.

💣 Extortion (IPC 384)

The accused threatened a shopkeeper with harm if he did not pay ₹5,000 every week as “protection money”.

🗣️ Defamation (IPC 499)

A businessman filed a case after false allegations were made against him in a local newspaper article.

💍 Dowry Death (IPC 304B)

A newly married woman died under suspicious circumstances at her in-laws’ house. Her family claimed she was harassed for dowry.

🔫 Attempt to Murder (IPC 307)

The suspect fired a gunshot at a local trader during an argument but missed; the trader survived with minor injuries.

🩸 Grievous Hurt (IPC 325)

A man attacked his neighbor with a sharp weapon causing a fracture in his arm during a property dispute.

🏚️ Dacoity (IPC 395)

A group of six men broke into a farmhouse at midnight, tied up the occupants, and looted valuables and cash.

✍️ Forgery (IPC 465)

The accused prepared a fake land ownership document to sell property that did not belong to him.

⚔️ Rioting (IPC 147)

During a protest march, several people vandalized public buses and attacked police vehicles.

👥 Unlawful Assembly (IPC 141)
