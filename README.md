# Mfukoni Finance Tracker

<div align="center">
  <img src="https://via.placeholder.com/1200x600/0d6efd/ffffff?text=Mfukoni+Dashboard+Screenshot" alt="Mfukoni Dashboard" width="800"/>
  <br><br>
  <strong>A personal finance manager powered by a custom-built RDBMS engine — track income, expenses, budgets and generate reports with full SQL support.</strong>
  <br><br>
  <em>"Mfukoni" = Swahili for "in the pocket"</em>
</div>

<br>

[![Python](https://img.shields.io/badge/Python-3.7+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2+-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/BillyMwangiDev/MFUKONI?style=social)](https://github.com/BillyMwangiDev/MFUKONI)

<br>

## ✨ Features

- Custom RDBMS from scratch (no SQLite/PostgreSQL/Django ORM)
- Full SQL support: CREATE, INSERT, SELECT, UPDATE, DELETE, INNER JOIN
- PRIMARY KEY, UNIQUE constraints + hash-based indexing
- Modern Django web UI (Bootstrap 5) for transactions, categories & budgets
- Financial dashboard with summaries, trends and budget progress
- Monthly budgets with alerts and remaining balance tracking
- Reports: spending by category, monthly trends, CSV/PDF/Excel export
- Interactive SQL REPL for direct database exploration
- Fully containerized with Docker & docker-compose

<br>

<!-- ================== SCREENSHOTS GO HERE ================== -->

<div align="center">
  <h3>Dashboard Overview</h3>
  <!-- Replace with your real screenshot -->
  <img src="assets/dashboard.png" alt="Dashboard - Total income, expenses, balance, recent transactions" width="800"/>
  <p>Real-time financial summary, recent activity and category breakdown</p>

  <br>

  <h3>Transactions Management</h3>
  <!-- Replace -->
  <img src="assets/transactions.png" alt="Transactions list with filters and quick add" width="800"/>
  <p>Filter, search, add/edit/delete income & expense entries</p>

  <br>

  <h3>Budget Tracking</h3>
  <!-- Replace -->
  <img src="assets/budgets.png" alt="Monthly budgets with progress bars" width="800"/>
  <p>Set limits per category and monitor spending progress</p>

  <br>

  <h3>Reports & Analytics</h3>
  <!-- Replace -->
  <img src="assets/reports.png" alt="Monthly trends, category spending pie chart or bar" width="800"/>
  <p>Visual breakdowns, trends and export options</p>
</div>

<br>

## 🚀 Quick Start (Docker – Recommended)

```bash
 Table of ContentsFeatures (#-features)
Screenshots (#-screenshots--demo) ← add your images here
Installation & Setup (#installation--setup)
Usage (#usage)
Custom RDBMS Highlights (#custom-rdbms-highlights)
Challenge Requirements (#challenge-requirements-summary)
Project Structure (#project-structure)
Contributing (#contributing)
License (#license)

Installation & SetupDocker (easiest)See Quick Start above. Full details → DOCKER.mdLocal DevelopmentClone & enter directory
Create & activate venv: python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
Copy .env.example → .env and edit (SECRET_KEY, DEBUG=True, etc.)
cd mfukoni_web && python manage.py runserver
Open http://localhost:8000

Database (custom RDBMS) auto-initializes — all data in data/mfukoni.db/.
UsageDashboard → / (summary + quick actions)
Transactions → /transactions/ (CRUD + filters)
Categories → /categories/ (manage income/expense types)
Budgets → /budgets/ (set monthly limits)
Reports → /reports/ (trends + exports)
SQL REPL → python -m my_rdbms.repl

Custom RDBMS HighlightsBuilt from scratch in my_rdbms/
Supports: INT, VARCHAR, FLOAT, BOOLEAN
Hash indexing → O(1) PK/UNIQUE lookups
JSON file persistence (human-readable)
No external DB libraries used

See my_rdbms/ for parser, executor, indexes, constraints.
Challenge Requirements SummaryAll Pesapal Developer Challenge 2026 requirements met:Custom RDBMS with full SQL CRUD + JOIN
Web app using custom DB (no Django ORM)
Comprehensive documentation & tests

Detailed fulfillment → see sections below or CHALLENGE_REQUIREMENTS_CONFIRMED.md

ContributingFork & clone
Create feature branch (git checkout -b feature/add-export-pdf)
Commit & push
Open Pull Request

Please follow PEP 8 + type hints. Run black . before committing.
LicenseMIT License — see LICENSEBuilt with   • Last updated February 2026Questions? → Open an issue or reach out on X @MwangiBillyG

# 1. Clone
git clone https://github.com/BillyMwangiDev/MFUKONI.git
cd MFUKONI

# 2. Start (builds & runs in background)
docker-compose up -d

# 3. Open in browser
# → http://localhost:8000
