const express = require("express");
const puppeteer = require("puppeteer");
const app = express();
const port = process.env.PORT || 10000;

app.get("/scan", async (req, res) => {
  const hashtag = req.query.hashtag;
  if (!hashtag) return res.status(400).send("Missing hashtag");

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto(`https://www.tiktok.com/tag/${hashtag}`);

  const data = await page.evaluate(() => {
    const items = document.querySelectorAll("div[data-e2e='search_video_item']");
    return Array.from(items).slice(0, 10).map(item => ({
      title: item.innerText,
      link: item.querySelector("a")?.href
    }));
  });

  await browser.close();
  res.json(data);
});

app.get("/", (req, res) => {
  res.send("TikTok API Phong is live!");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
