# 🧪 API Test Automation Suite

Automated functional test suite for the [DummyJSON](https://dummyjson.com) REST API, built using Python. Covers authentication, products, users, carts, schema validation, and performance checks.

![Tests](https://github.com/DivyanshCh39/api-test-automation-suite/actions/workflows/test.yml/badge.svg)

---

## 📋 Test Coverage

| Module | Test Cases |
|---|---|
| Authentication — Register & Login | TC-001 → TC-006 |
| Products — GET, Search, Filter, Limit | TC-007 → TC-013 |
| Users — GET, Schema Validation | TC-014 → TC-016 |
| Performance, Headers & Cart Schema | TC-017 → TC-020 |
| **Total** | **20 Test Cases** |

---

## 📁 Project Structure

```
api-test-automation-suite/
├── test_suite.py                  # Main test file — 20 test cases
├── requirements.txt               # Python dependencies
├── .gitignore
├── config/
│   └── config.py                  # Base URL, thresholds, report path
├── reports/
│   └── test_report.json           # Auto-generated after each run
└── .github/
    └── workflows/
        └── test.yml               # GitHub Actions CI/CD pipeline
```

---

## 🚀 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/api-test-automation-suite.git
cd api-test-automation-suite
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the test suite
```bash
python test_suite.py
```

---

## ⚙️ CI/CD — GitHub Actions

Tests run automatically on every push and pull request, and daily at 9AM UTC. The `test_report.json` is uploaded as a build artifact after each run.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core language |
| `requests` | HTTP API calls |
| GitHub Actions | CI/CD automation |
| DummyJSON API | API under test |
| JSON | Report format |

---

## 💡 What This Tests

- ✅ Valid & invalid authentication (register / login)
- ✅ Product listing, search, filter by category, pagination
- ✅ HTTP status codes (200, 201, 400, 401, 404)
- ✅ Response body schema validation
- ✅ API response time threshold (< 3000ms)
- ✅ Content-Type header validation
- ✅ Edge cases — missing fields, wrong credentials, nonexistent IDs

## 📸 Sample Output

![Test Output](assets/test-output.png)

