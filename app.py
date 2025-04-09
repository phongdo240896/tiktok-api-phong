const express = require('express');
const puppeteer = require('puppeteer');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());

app.get('/scan', async (req, res) => {
    const { hashtag } = req.query;
    if (!hashtag) {
        return res.status(400).json({ error: 'Thiếu hashtag' });
    }

    try {
        const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
        const page = await browser.newPage();
        await page.goto(`https://www.tiktok.com/tag/${hashtag}`, { waitUntil: 'networkidle2' });
        await page.waitForTimeout(5000);

        const videos = await page.evaluate(() => {
            const list = [];
            const items = document.querySelectorAll('a[href*="/video/"]');
            items.forEach((el) => {
                const caption = el.innerText;
                const link = el.href;
                list.push({ caption, link });
            });
            return list;
        });

        await browser.close();
        res.json(videos);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Đã xảy ra lỗi khi thu thập dữ liệu TikTok' });
    }
});

app.listen(PORT, () => {
    console.log(`TikTok API đang chạy tại http://localhost:${PORT}`);
});
