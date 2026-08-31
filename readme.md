# Modular Inventory Management System

A robust, relational-database-driven Inventory Management System built in Python. Designed to maintain product catalogs, track stock transactions with audit logging, and issue real-time reorder threshold alerts.

## Features
- **Relational Data Modeling:** Normalized SQLite schema with foreign key constraints and transaction logging.
- **Stock Audit Trail:** Tracks all `RESTOCK` and `DISPATCH` events with timestamps.
- **Automated Low-Stock Alerts:** Queries items falling below configurable reorder levels.
- **Data Integrity:** Enforces constraints on negative inventory and invalid price points.

## Tech Stack
- **Language:** Python 3.10+
- **Database:** SQLite3 / SQL
- **Architecture:** Modular separation of concerns (Storage Layer vs. Service Layer vs. Presentation CLI)

## Getting Started

1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/inventory-management-system.git
   cd inventory-management-system
