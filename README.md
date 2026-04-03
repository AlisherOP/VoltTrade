# ⚡ VoltTrade - High-Concurrency Crypto Trading Engine

![VoltTrade](https://img.shields.io/badge/Status-Active-brightgreen) ![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=flat&logo=django) ![DRF](https://img.shields.io/badge/DRF-3.17.0-red?style=flat&logo=django) ![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)

VoltTrade is a robust, high-performance web backend designed to simulate a real-world cryptocurrency trading platform. Built with **Django REST Framework**, the project prioritizes data integrity and high-concurrency safety, making it suitable for financial applications. 

## ✨ Key Features & Technical Highlights

- **Robust Financial Engine:** Guaranteed data consistency explicitly designed to ensure money is never lost during sudden network outages or concurrent trade executions.
- **Pessimistic Data Locking:** Prevents dangerous race conditions using strict database-level row locking with `select_for_update()`.
- **Deadlock Prevention Mechanisms:** Algorithmically prevents deadlocks during peer-to-peer transfers by implementing deterministic ID sorting prior to multi-row locking.
- **Data Normalization & Precision:** Adheres to strict data casing and relies on `Decimal` precision to avoid binary floating-point errors inherent to financial calculations.
- **Live Market Data:** Integrates directly with the **CoinGecko API** for real-time cryptocurrency pricing and exchange rates.

## 🏗️ Architecture & Stack

- **Backend Framework:** Django & Django REST Framework (DRF)
- **Database:** SQLite3 (Configurable for PostgreSQL)
- **External Services:** CoinGecko API integration for live crypto prices

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your local machine:
- Python 3.8+
- `pip` package manager
- `virtualenv` (recommended)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/VoltTrade.git
   cd VoltTrade
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   *Access the DRF browsable API at `http://127.0.0.1:8000/api/wallets/`.*

## 🔌 API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register/` | POST | Register a new user |
| `/api/wallets/` | GET | Retrieve wallets |
| `/api/wallets/transfer/` | POST | Transfer USD safely to another user |
| `/api/wallets/buy_coin/` | POST | Buy cryptocurrency (e.g., BTC, ETH) using USD balance |
| `/api/wallets/sell_coin/` | POST | Sell cryptocurrency to convert back to USD |

## 🔒 Concurrency Management

VoltTrade addresses the classic "double-spend" database problem frequently seen in naive trading applications. This is handled by wrapping potentially sensitive views in a `transaction.atomic()` block, and heavily utilizing Django's `select_for_update()` query method. By doing so, the database forces sequential execution of transactions touching the same wallet or asset ledger, practically eliminating race conditions while maintaining rapid transactional throughput.

## 🛡️ License

This project is open-source and available under the MIT License.
