# kemtam — Humanize AI Server

A Flask paraphrase server that rewrites text to sound human-written. Powered by the Hugging Face Inference API (`humarin/chatgpt_paraphraser_on_T5_base`). Deployed on Vercel.

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
echo "HF_TOKEN=your_key_here" > .env
python api/index.py
```

## Vercel deployment

1. Push this repo to GitHub
2. Import at vercel.com/new
3. Add `HF_TOKEN` in Settings → Environment Variables
4. Deploy

Get a free Hugging Face token at https://huggingface.co/settings/tokens.
