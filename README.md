# 🚀 Pharmyrus v28.0 - INPI Multi-Strategy + Audit

## 📋 **VISÃO GERAL**

Sistema de busca de patentes farmacêuticas com 3 camadas:
- **Layer 1:** WIPO + EPO OPS (API oficial)
- **Layer 2:** Google Patents (crawler agressivo)
- **Layer 3:** INPI Multi-Strategy (6 estratégias paralelas)
- **Audit:** Comparação automática vs Cortellis

### **Novidades v28.0:**
✅ **6 estratégias INPI** executadas em paralelo
✅ **Auditoria Cortellis** integrada no JSON
✅ **Recall, Precision, F1-score** calculados automaticamente
✅ **Rating BAIXO/MÉDIO/ALTO** de performance
✅ **Campo `brand_name`** corrigido
✅ **Zero dependências externas** (tudo inline)

---

## 🎯 **ESTRATÉGIAS INPI**

### **1. Textual Multi-Term**
Busca por nome da molécula, nome comercial, dev codes e combinações.

### **2. Applicant/Titular**
Busca por depositante + molécula (quando depositantes conhecidos disponíveis).

### **3. IPC/CPC Pharmaceutical**
Busca usando classificações farmacêuticas: A61K, A61P, A61K9, A61K31, A61K47.

### **4. Temporal Recent (2023-2025)**
Foca em patentes depositadas após 2023 (gap do EPO de 6-18 meses).

### **5. Formulations**
Busca por termos de formulação farmacêutica (comprimido, cápsula, injetável, etc).

### **6. Polymorphs & Salts**
Busca por polimorfos, sais e formas cristalinas.

---

## 📊 **EXEMPLO DE AUDITORIA**

```json
{
  "cortellis_audit": {
    "comparison": {
      "expected_brs": 8,
      "found_brs": 28,
      "matched_brs": 8
    },
    "metrics": {
      "recall_percent": 100.0,
      "precision_percent": 28.57,
      "f1_score": 44.44
    },
    "vs_cortellis": {
      "status": "BETTER",
      "difference_percent": 250.0,
      "quality_rating": "ALTO"
    }
  }
}
```

---

## 🚀 **DEPLOY RAILWAY**

### **1. Criar novo repositório GitHub**
```bash
git init
git add .
git commit -m "Initial commit - Pharmyrus v28.0"
git remote add origin <seu-repo-git>
git push -u origin main
```

### **2. Deploy no Railway**
1. Acesse https://railway.app
2. New Project → Deploy from GitHub repo
3. Selecione o repositório criado
4. Railway detecta Dockerfile automaticamente
5. Aguarde build (~5 minutos)

### **3. Configurar Variáveis (Opcional)**
Railway não precisa de variáveis de ambiente para funcionar, mas você pode adicionar se necessário.

### **4. Testar**
```bash
curl -X POST https://<seu-app>.railway.app/search \
  -H "Content-Type: application/json" \
  -d '{
    "nome_molecula": "darolutamide",
    "nome_comercial": "Nubeqa",
    "paises_alvo": ["BR"],
    "incluir_wo": true
  }'
```

---

## 📂 **ESTRUTURA DO PROJETO**

```
pharmyrus-v28-complete/
├── main.py                      # Main com INPI inline (TUDO em 1 arquivo)
├── google_patents_crawler.py    # Crawler Google Patents
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Container config
├── railway.json                 # Railway config
├── .gitignore                   # Git ignore rules
└── README.md                    # Este arquivo
```

---

## 📦 **DEPENDÊNCIAS**

Todas listadas em `requirements.txt`:
- fastapi
- uvicorn[standard]
- httpx
- pydantic

**Nota:** Nenhuma dependência extra necessária para v28.0 (tudo inline).

---

## ✅ **VALIDAÇÃO**

### **Testar localmente:**
```bash
pip install -r requirements.txt
python main.py
```

### **Verificar health:**
```bash
curl http://localhost:8000/health
```

### **Fazer busca teste:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"nome_molecula": "darolutamide", "paises_alvo": ["BR"]}'
```

---

## 📈 **MÉTRICAS ESPERADAS**

| Métrica | v27.5 | v28.0 Target |
|---------|-------|--------------|
| **BRs (darolutamide)** | 8 | 15+ |
| **Recall** | 50% | 95%+ |
| **Rating** | BAIXO | ALTO |
| **Tempo** | 778s | <900s |

---

## 🐛 **TROUBLESHOOTING**

### **Erro: ModuleNotFoundError**
✅ **Resolvido!** v28.0 tem tudo inline, não precisa de módulos externos.

### **Healthcheck failed**
Verifique logs no Railway: Settings → Deployments → View Logs

### **Timeout**
INPI pode estar lento. Sistema tem fallback automático.

---

## 📞 **SUPORTE**

- Issues: GitHub Issues
- Logs: Railway Dashboard → Deployments → Logs
- Health: `/health` endpoint

---

**STATUS:** ✅ PRONTO PARA DEPLOY IMEDIATO
**Versão:** 28.0-INLINE
**Data:** 2026-01-09
