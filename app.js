const express = require('express');
const puppeteer = require('puppeteer');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());

app.get('/scan', async (req, res) => {
  const hashtag = req.query.hashtag || 'tiktok';
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto(`https://www.tiktok.com/tag/${hashtag}`);

    // Lấy dữ liệu từ TikTok (có thể điều chỉnh theo nhu cầu)
    const result = await page.evaluate(() => {
      const videos = [];
      document.querySelectorAll('div[data-e2e="video-feed-item"]')
        .forEach((video) => {
          const title = video.querySelector('h3')?.innerText || 'No title';
          const link = video.querySelector('a')?.href || '';
          const likes = video.querySelector('strong')?.innerText || 'No likes';
          videos.push({ title, link, likes });
        });
      return videos;
    });

    await browser.close();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: 'Error scraping TikTok' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
