const express = require("express");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const app = express();
const port = process.env.PORT || 10000;

app.get("/scan", async (req, res) => {
  const hashtag = req.query.hashtag;
  if (!hashtag) return res.status(400).send("Missing hashtag");

  try {
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();

    // Giả lập trình duyệt
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36");
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9'
    });

    await page.goto(`https://www.tiktok.com/tag/${hashtag}`, { waitUntil: "networkidle2", timeout: 60000 });

    const data = await page.evaluate(() => {
      const items = document.querySelectorAll("div[data-e2e='search_video_item']");
      return Array.from(items).slice(0, 10).map(item => ({
        title: item.innerText,
        link: item.querySelector("a")?.href
      }));
    });

    await browser.close();
    res.json(data);
  } catch (err) {
    console.error("Lỗi khi crawl:", err.message);
    res.status(500).send("Server error");
  }
});

app.get("/", (req, res) => {
  res.send("TikTok API Phong is live!");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
