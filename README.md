# Ops Support Analytics

End-to-end operations analytics project using Python, SQL, and SQLite to analyze 5,000+ simulated support orders and identify delivery delays, accuracy trends, and support rep performance.

## Business Problem
Operations teams need visibility into:
- Order accuracy
- Late deliveries
- Support response times
- Individual rep performance

This project simulates a real-world ops support environment and answers key performance questions using SQL analytics.

## Tech Stack
- Python (data generation & loading)
- SQLite (database)
- SQL (analysis queries)
- VS Code
- GitHub

## Dataset
Synthetic data generated via Python:
- Clients
- Orders
- Communications
- Support reps

## Key Metrics
- Total Orders: 5,000
- Accuracy Rate: ~97%
- Late Delivery Rate: ~66%
- Avg First Response Time: ~3.7 hours

## SQL Analysis
- **KPIs**: Overall accuracy, lateness, response time
- **Rep Performance**: Orders handled, accuracy %, late %, avg response time
- **Trend Analysis**: Volume and delay trends over time

SQL queries available in `/sql`:
- `01_kpis.sql`
- `02_rep_performance.sql`
- `03_trendanalysis.sql`

## Project Structure
data/
raw/
processed/
db/
scripts/
sql/
docs/

## How to Run
1. Create virtual environment
2. Install dependencies
3. Run `generate_data.py`
4. Query SQLite database using SQL files

## Key Takeaways
- High accuracy does not guarantee on-time delivery
- Certain reps handle significantly higher volume
- Response time correlates with late deliveries

---
*Built as a portfolio project for operations & data analytics roles.*

