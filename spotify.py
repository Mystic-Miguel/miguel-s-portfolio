import requests
link = "https://open.spotify.com/track/2vtmY2mSccRzKGjtcHSzI3?si=1c1207faf9b64de4"

req = requests.post(
    "https://api.spotify-downloader.com/",
    data={
        "link": link
    },
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
)
print(req.json())