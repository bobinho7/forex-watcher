# 💱 UGX/USD Forex Watcher System

A web-based Forex monitoring and analytics system that tracks and visualizes UGX/USD exchange rates across multiple forex bureaus. The system provides role-based access control (RBAC), real-time data visualization, and bureau-level performance insights.

---

## 📌 Problem Statement

Foreign exchange rates in Uganda vary across different bureaus, and users often lack a centralized platform to compare rates, track trends, and analyze market movements.

This system solves that problem by providing:
- Centralized exchange rate tracking
- Bureau comparison
- Trend visualization
- Role-based data entry and viewing

---

## 🚀 Features

### 👤 Authentication & Security
- User login system
- Role-Based Access Control (RBAC)
  - Admin
  - Analyst
  - Viewer

### 🏦 Bureau Management
- Add forex bureaus (Admin only)
- View registered bureaus
- Track number of rates per bureau

### 💱 Exchange Rate Management
- Add buy/sell rates
- Filter rates by bureau
- Automatic timestamp tracking

### 📊 Data Visualization
- Interactive Chart.js line charts
- Buy vs Sell rate trend analysis
- Bureau-specific filtering

### 📈 Dashboard Analytics
- Average buy rate
- Average sell rate
- Best performing bureaus
- Real-time summary cards

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Vanilla JavaScript
- Chart.js

### Backend
- Python (Flask)
- Flask-SQLAlchemy ORM
- Flask-Login (authentication)

### Database
- SQLite (development)

---

## 🧱 System Architecture

---

## 🗄️ Database Schema

### User
- id
- username
- password
- role

### Bureau
- id
- name
- location

### ExchangeRate
- id
- bureau_id (FK)
- buy_rate
- sell_rate
- recorded_at

---

## 🔐 RBAC Model

| Role    | Permissions |
|----------|-------------|
| Admin    | Manage bureaus, add rates, full access |
| Analyst  | Add exchange rates, view dashboard |
| Viewer   | View dashboard only |

---

## 📊 Data Visualization Pipeline

1. Exchange rates are stored in SQLite
2. Flask retrieves and aggregates data
3. Data is passed to frontend via Jinja2
4. Chart.js renders interactive graphs
5. Users can filter data by bureau

---

## ⚙️ Installation & Setup

### 1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/forex-watcher.git
cd forex-watcher
