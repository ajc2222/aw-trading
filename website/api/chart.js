// GET /api/chart?symbol=MES=F&period1=1234567890&period2=1234567890
// Proxies Yahoo Finance v8 chart API (CORS-blocked from browser directly)

module.exports = async (req, res) => {
  const { symbol, period1, period2 } = req.query;
  if (!symbol || !period1 || !period2) {
    return res.status(400).json({ error: 'Missing params: symbol, period1, period2' });
  }

  const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}` +
    `?interval=1m&period1=${period1}&period2=${period2}&includePrePost=false`;

  try {
    const upstream = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
      },
    });

    if (!upstream.ok) {
      return res.status(upstream.status).json({ error: `Yahoo Finance: ${upstream.status}` });
    }

    const data = await upstream.json();
    res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate=600');
    return res.json(data);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
};
