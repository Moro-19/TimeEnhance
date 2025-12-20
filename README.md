# ⏰ Time Enhance

A gamified productivity and time-management web application that helps users organize tasks, track progress, and stay motivated through a built-in reward system.

## 📋 Project Information

**Course:** CSAI 203 - Introduction to Software Engineering  
**Team:** #40  
**Member:** Marwan Abdelhamid  ID: 202401466  
**Institution:** Zewail City of Science, Technology and Innovation  

## 🎯 Features

### Core Functionality
-  Task Management (Create, Edit, Delete, Complete)
-  Difficulty Levels (Easy, Medium, Hard)
-  XP & Leveling System
-  Virtual Currency (Time Coins)
-  Virtual Store (Purchase Cosmetics)
-  Inventory System (Equip/Unequip Items)
-  User Profile with Progress Tracking
-  Dashboard with Statistics

### Technical Features
-  MVC Architecture Pattern
-  Factory Pattern
-  Singleton Pattern
-  Repository Pattern
-  Automated Testing (42+ Unit Tests)
-  CI/CD Pipeline (GitHub Actions)
-  Docker Containerization
-  Responsive CSS Design

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/TimeEnhance.git
cd TimeEnhance
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python src/app.py
```

4. **Access the application:**
```
http://localhost:5000
```

### Default Login Credentials
- **Username:** `testuser`
- **Password:** `password`

##  Docker Deployment

### Build Docker Image
```bash
docker build -t timeenhance-app .
```

### Run Docker Container
```bash
docker run -p 5000:5000 timeenhance-app
```

### Access Application
```
http://localhost:5000
```

##  Testing

### Run All Tests
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_models.py -v
```

### Run with Coverage
```bash
pytest --cov=src tests/
```

##  Project Structure
```
TimeEnhance/
├── docs/                  # Documentation (SRS, Design)
├── src/                   # Source code
│   ├── Controllers/       # Flask route controllers
│   ├── models/           # Data models
│   ├── Repositories/     # Data access layer
│   ├── Core/             # Factory pattern
│   ├── Utils/            # Utilities (FileManager singleton)
│   ├── templates/        # HTML templates
│   └── static/           # CSS files
├── tests/                # Unit tests
├── Data/                 # CSV data storage
├── deployment/           # Deployment files
├── .github/workflows/    # CI/CD pipeline
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── pytest.ini          # Pytest configuration
```

##  Design Patterns

### MVC (Model-View-Controller)
- **Models:** User, Task, Reward, StoreItem, Inventory
- **Views:** HTML templates with Jinja2
- **Controllers:** Flask blueprints for routing

### Factory Pattern
- `RepositoryFactory` creates appropriate repository instances

### Singleton Pattern
- `FileManager` ensures single instance for file operations

### Repository Pattern
- Isolates data access logic from business logic

##  Bonus Features Implemented

-  Modularization across entire project 
-  Factory Pattern 
-  Repository Pattern 
-  Singleton Pattern 
-  CSS Styling 

##  Testing Coverage

- **Total Tests:** 42+ unit tests
- **Test Categories:**
  - Model Tests (15+)
  - Factory Tests (9)
  - Singleton Tests (4)
  - Repository Tests (10+)
  - Controller Tests (8+)

##  CI/CD Pipeline

Automated testing runs on every push via GitHub Actions:
- Checkout code
- Setup Python 3.10
- Install dependencies
- Run pytest

##  Documentation

- **SRS Document:** `docs/CSAI203_Design_Team40_202401466.pdf`
- **Design Document:** `docs/TimeEnhance.pdf`
- **Testing Guide:** See `tests/README.md`

##  Technology Stack

- **Backend:** Python Flask
- **Frontend:** HTML, CSS
- **Data Storage:** CSV files
- **Testing:** pytest, pytest-flask
- **CI/CD:** GitHub Actions
- **Containerization:** Docker

##  License

This project was developed as part of the CSAI 203 course requirements at Zewail City University.

##  Author

**Marwan Abdelhamid**  
Student ID: 202401466  
Email: s-marwan.abdel-hamid@zewailcity.edu.eg

---