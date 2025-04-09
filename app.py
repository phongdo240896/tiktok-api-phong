from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def scrape_tiktok_videos(hashtag, limit=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.tiktok.com/tag/{hashtag}", timeout=60000)
        page.wait_for_timeout(5000)

        videos = []
        anchors = page.query_selector_all("a[href*='/video/']")
        links = list({a.get_attribute('href') for a in anchors if a.get_attribute('href')})[:limit]

        for link in links:
            page.goto(link, timeout=60000)
            page.wait_for_timeout(3000)

            video = {
                "caption": page.locator("h1").inner_text() or "",
                "video_url": link,
                "account": page.locator("a[href*='/@']").first.inner_text() or "",
                "like": int(page.locator("strong").nth(0).inner_text().replace(",", "") or "0"),
                "comment": int(page.locator("strong").nth(1).inner_text().replace(",", "") or "0"),
                "share": int(page.locator("strong").nth(2).inner_text().replace(",", "") or "0"),
                "hashtag": hashtag
            }
            videos.append(video)

        browser.close()
        return videos

@app.route("/scan", methods=["GET"])
def scan():
    hashtag = request.args.get("hashtag")
    if not hashtag:
        return jsonify({"error": "Thiếu hashtag"}), 400
    return jsonify(scrape_tiktok_videos(hashtag))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
