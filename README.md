# kemtam — Humanize AI Server

A Flask paraphrase server that rewrites text to sound human-written. Powered by Groq (llama-3.3-70b-versatile). Deployed on Vercel.

## Endpoint

**POST /paraphrase**

Request:
```json
{ "text": "Your text here." }
```

Response:
```json
{ "paraphrased": "Rewritten text.", "success": true }
```

## Local setup

```bash
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
python api/index.py
```

## Vercel deployment

1. Push this repo to GitHub
2. Import at vercel.com/new
3. Add GROQ_API_KEY in Settings → Environment Variables
4. Deploy

Get a free Groq API key at https://console.groq.com.