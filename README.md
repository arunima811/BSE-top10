# BSE Top 10
CherryPy app that shows the top 10 BSE stocks.

fetch_to_redis.py : Fetched the equity zip and extracts the data to appropriate data structures in Redis.

app.py: Handles the sorting and searching functionalities of the stocks and renders the front-end templates for the app.

# Run


```bash
pip install -r requirements.txt
python fetch_to_redis.py
python app.py

//(Optional) Automatically fetch the new file zip file every 24hours
sudo crontab -e
//insert
0 10 * * * python /path/to/file/fetch_to_redis.py
0 10 * * * python /path/to/file/app.py
```

# Live Demo

[Heroku App](https://boiling-sea-89162.herokuapp.com/)
