# VictorTech
PentaCORE Hackathon

Overview -
This web application analyzes Croma's competitors, displaying graphs and tables based on real-time data scraping. It retrieves insights on stock trends, marketing strategies, site traffic, and demographics, leveraging FastAPI for the backend and HTML/CSS/JavaScript for the frontend.

Features -
Real-Time Web Scraping: Gathers competitor data dynamically.
Data Visualization: Presents information in graphs and tables.
NLP Integration: Uses Named Entity Recognition (NER) to validate company names.
API Data Fetching: Utilizes SimilarWeb, Alpha Vantage, and Gemini for additional insights.
AI-Generated Marketing Strategies: Offers insights based on scraped data.

How to Run
Server:
Ensure REALTIME.py and API.py are in the same directory.
Run the following command:
"uvicorn API:app --host 0.0.0.0 --port 8000 --reload"

Client
Connect to the same network as the server.
Open the corresponding "helloworld" HTML file in a web browser.

Future Improvements
Faster Scraping: Optimize data retrieval speed.
Better Language Models: Fine-tune models for identifying Indian companies.
