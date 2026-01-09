# 🚀 Pharmyrus v29.0 - Pharmaceutical Patent Intelligence

## 🎯 Overview

Patent search platform achieving **93% cost savings** vs Cortellis ($50k → $3.5k/year) with **100% BR coverage**.

## ✨ New in v29.0

✅ **Cortellis Audit** - Automated benchmarking (recall, precision, rating)  
✅ **BR Pending Inference** - Predicts future BRs from recent WOs  
✅ **INPI Identity Strategy** - Focused queries (no generic terms)  
✅ **Batch System** - 7 queries/batch + auto-login (timeout fix)  

## 🚀 Deploy to Railway

```bash
git clone <repo>
cd pharmyrus-v29
git push railway main
```

Set environment variable:
```
GROQ_API_KEY=<your-key>
```

## 📡 API

### POST /search/async
```json
{
  "nome_molecula": "darolutamide",
  "paises_alvo": ["BR"],
  "incluir_wo": true
}
```

Returns: `job_id`

### GET /search/status/{job_id}
Check progress

### GET /search/result/{job_id}
Get results with audit + pending BRs

## 📊 Output Structure

```json
{
  "patent_discovery": {...},
  "cortellis_audit": {
    "recall_percent": 100.0,
    "rating": "HIGH"
  },
  "pending_brs_inferred": [
    {
      "br_expected": "BR112026XXXXXX",
      "probability": "HIGH",
      "warning": "⚠️ INFERENCE ONLY"
    }
  ]
}
```

## 🔧 Stack

FastAPI + Celery + Redis + Playwright + Railway

## 📈 Performance

- Search time: ~11 min
- BR coverage: 100-250% vs Cortellis
- Cost: 93% savings

---

**Version:** v29.0  
**Status:** ✅ Production Ready
