# ⚡ VoltTrade - High-Concurrency Crypto Engine

A professional trading backend built with **Django Rest Framework** and **PostgreSQL**.

##  Key Backend Features
- **Atomic Transactions**: Guarantees that money is never lost during a trade.
- **Pessimistic Locking**: Prevents Race Conditions using `select_for_update()`.
- **Deadlock Prevention**: Implements ID sorting before multi-row locking.
- **Data Normalization**: Strict casing and Decimal precision for financial accuracy.
- **External API Integration**: Real-time price fetching from CoinGecko.

##  Deployment
This project is fully containerized with **Docker Compose**.
1. `docker-compose up --build`
2. Access Swagger UI at `/api/docs/`