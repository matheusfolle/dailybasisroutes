# 🚀 Deploy no Vercel - Guia Definitivo

## ⚠️ IMPORTANTE: Ordem correta!

**Faça EXATAMENTE nesta ordem:**

### ✅ **1. Preparar o Código**

**No seu repositório GitHub, certifique-se que tem TODOS estes arquivos:**

```
DailyBasisRoute/
├── app.py
├── vercel.json
├── requirements.txt
├── init_database.sql
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── analytics.html
│   └── historico.html
└── static/
    └── css/
        └── style.css
```

**Se falta algum arquivo, faça:**
```bash
git add .
git commit -m "Deploy para Vercel"
git push
```

---

### ✅ **2. Criar Tabelas no Supabase (SE AINDA NÃO FEZ)**

1. Acesse https://supabase.com
2. Seu projeto → **SQL Editor**
3. **New Query**
4. Cole TODO o conteúdo de `init_database.sql`
5. Clique em **RUN**
6. ✅ Deve aparecer: "Tabelas criadas com sucesso!"

---

### ✅ **3. Deploy no Vercel**

#### **A. Conectar GitHub**

1. Acesse https://vercel.com
2. Login com GitHub
3. **Add New...** → **Project**
4. Selecione o repositório **DailyBasisRoute**
5. Clique em **Import**

#### **B. ANTES DE FAZER DEPLOY - Configure Variáveis**

**🚨 CRÍTICO: Faça isso ANTES de clicar em Deploy!**

Na tela de configuração do projeto, procure por **"Environment Variables"** e adicione:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres.flzqqwelasfzipzahzqw:31528899japan@aws-1-us-east-1.pooler.supabase.com:5432/postgres` |
| `SECRET_KEY` | `dailybasisroute-secret-key-2025-production` |

**IMPORTANTE:** Cole EXATAMENTE a DATABASE_URL com sua senha!

#### **C. Configurar Build**

**Framework Preset:** Other (ou deixe auto-detect)

**Root Directory:** Deixe vazio

**Build Command:** Deixe vazio

**Output Directory:** Deixe vazio

**Install Command:** `pip install -r requirements.txt`

#### **D. Deploy!**

1. Clique em **Deploy**
2. Aguarde 2-3 minutos
3. ✅ Pronto!

---

### ✅ **4. Testar**

Vercel vai te dar uma URL tipo:
```
https://daily-basis-route.vercel.app
```

**Teste:**
1. Acesse a URL
2. Crie uma conta
3. Adicione tarefas
4. Veja se salva no banco

---

## 🐛 **Troubleshooting**

### **Erro: "Application Error"**

**Causa:** Variáveis de ambiente não configuradas

**Solução:**
1. Vercel Dashboard → Seu projeto → **Settings**
2. **Environment Variables**
3. Adicione `DATABASE_URL` e `SECRET_KEY`
4. **Deployments** → **Redeploy**

---

### **Erro: "Table doesn't exist"**

**Causa:** Não rodou o `init_database.sql` no Supabase

**Solução:**
1. Supabase → **SQL Editor**
2. Cole o conteúdo de `init_database.sql`
3. **RUN**

---

### **Erro: "Unable to connect to database"**

**Causa:** DATABASE_URL incorreta

**Solução:**
1. Supabase → **Project Settings** → **Database**
2. **Connection string** → Aba **URI**
3. Copie a URL **COMPLETA** (com senha)
4. Vercel → **Settings** → **Environment Variables**
5. Atualize `DATABASE_URL`
6. **Redeploy**

---

### **Erro: "Module not found"**

**Causa:** `requirements.txt` incompleto

**Solução:**
Certifique-se que `requirements.txt` tem:
```
Flask==3.0.0
psycopg2-binary==2.9.9
Werkzeug==3.0.0
```

---

## 📱 **Usar no Celular**

Depois do deploy funcionando:

### **iPhone:**
1. Safari → Acesse a URL do Vercel
2. Botão **Compartilhar** (quadrado com seta)
3. **"Adicionar à Tela Inicial"**
4. Pronto! Agora tem um ícone do app

### **Android:**
1. Chrome → Acesse a URL do Vercel
2. Menu (3 pontinhos)
3. **"Adicionar à tela inicial"**
4. Pronto! Ícone criado

---

## 🔄 **Atualizações Futuras**

Quando você atualizar o código:

1. **No GitHub:**
```bash
git add .
git commit -m "Nova feature"
git push
```

2. **Vercel rebuilda automaticamente!**
3. Aguarde 1-2min
4. ✅ Site atualizado

**Dados permanecem intactos no Supabase!**

---

## ✅ **Checklist Final**

Antes de começar, confirme:

- [ ] Código no GitHub com todos os arquivos
- [ ] `vercel.json` na raiz
- [ ] `requirements.txt` na raiz
- [ ] Tabelas criadas no Supabase
- [ ] DATABASE_URL copiada do Supabase

**Pronto? Bora fazer o deploy!** 🚀
