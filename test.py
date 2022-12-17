import cloudscraper
scraper = cloudscraper.create_scraper()
i = scraper.get("https://streamtape.com/get_video?id=xPgbO0OVVYIkkqx&expires=1671302502&ip=F0ySKRWSFS9XKxR&token=jxAO0udPsmKG&stream=1")
print(i)