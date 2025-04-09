
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import re

app = Flask(__name__)

def scrape_tiktok_videos(hashtag, limit=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"https://www.tiktok.com/tag/{hashtag}"
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # Đợi trang tải xong

        videos = []
        anchors = page.query_selector_all("a[href*='/video/']")
        unique_links = set()

        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href and "/video/" in href and href not in unique_links:
                unique_links.add(href)
                if len(unique_links) >= limit:
                    break

        for link in unique_links:
            page.goto(link, timeout=60000)
            page.wait_for_timeout(3000)

            try:
                caption = page.locator("h1").inner_text()
            except:
                caption = ""

            try:
                author = page.locator("a[href*='/@']").first.inner_text()
            except:
                author = ""

            try:
                stats = page.locator("strong").all_inner_texts()
                like = int(stats[0].replace(',', '')) if len(stats) > 0 else 0
                comment = int(stats[1].replace(',', '')) if len(stats) > 1 else 0
                share = int(stats[2].replace(',', '')) if len(stats) > 2 else 0
            except:
                like = comment = share = 0

            video = {
                "caption": caption,
                "video_url": link,
                "like": like,
                "comment": comment,
                "share": share,
                "account": author,
                "hashtag": hashtag
            }
            videos.append(video)

        browser.close()
        return videos

@app.route("/scan", methods=["GET"])
def scan():
    hashtag = request.args.get("hashtag", "")
    if not hashtag:
        return jsonify({"error": "Thiếu hashtag"}), 400

    data = scrape_tiktok_videos(hashtag)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
