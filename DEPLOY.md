# 🚀 Deploy no Vercel - Guia Completo

## 📋 Pré-requisitos

1. ✅ Conta no [Supabase](https://supabase.com) (gratuita)
2. ✅ Conta no [Vercel](https://vercel.com) (gratuita)
3. ✅ Código no GitHub

---

## 1️⃣ Configurar Banco de Dados (Supabase)

### **A. Criar Projeto**
1. Acesse https://supabase.com
2. Clique em **"New Project"**
3. Preencha:
   - **Name:** `dailybasisroute`
   - **Database Password:** Crie uma senha forte e **ANOTE**
   - **Region:** South America (São Paulo)
4. Aguarde ~2min

### **B. Criar Tabelas**
1. No Supabase, vá em **SQL Editor** (menu lateral)
2. Clique em **"New Query"**
3. **Cole todo o conteúdo** do arquivo `init_database.sql`
4. Clique em **"Run"**
5. Você verá: ✅ "Tabelas criadas com sucesso!"

### **C. Pegar Connection String**
1. Clique em **"Connect"** (botão verde no topo)
2. Escolha **"ORMs"**
3. Selecione **"URI"**
4. **Copie a string** (algo como):
```
postgresql://postgres.xxxxx:SUA_SENHA@db.xxxxx.supabase.co:5432/postgres
```
5. **IMPORTANTE:** Troque `[YOUR-PASSWORD]` pela senha que você criou no passo A3

---

## 2️⃣ Deploy no Vercel

### **A. Conectar Repositório**
1. Acesse https://vercel.com
2. Clique em **"Add New..."** → **"Project"**
3. **Import** seu repositório GitHub
4. Vercel vai detectar automaticamente

### **B. Configurar Variáveis de Ambiente**
**ANTES** de fazer deploy, configure:

1. Na tela de configuração do projeto, procure por **"Environment Variables"**
2. Adicione estas variáveis:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres.xxxxx:SUA_SENHA@db.xxxxx.supabase.co:5432/postgres` |
| `SECRET_KEY` | Qualquer string longa e aleatória (ex: `minha-chave-super-secreta-2025`) |

### **C. Deploy!**
1. Clique em **"Deploy"**
2. Aguarde ~2-3min
3. ✅ Pronto! Seu site estará no ar!

---

## 3️⃣ Acessar o Site

Após o deploy, Vercel vai te dar uma URL tipo:
```
https://dailybasisroute.vercel.app
```

**Teste:**
1. Acesse a URL
2. Crie sua conta
3. Comece a usar! 🎉

---

## 🔧 Troubleshooting

### **Erro: "Unable to connect to database"**
- ✅ Verifique se a `DATABASE_URL` está correta
- ✅ Confirme que substituiu `[YOUR-PASSWORD]` pela senha real
- ✅ Teste a conexão no Supabase SQL Editor

### **Erro: "Table doesn't exist"**
- ✅ Execute o `init_database.sql` no Supabase
- ✅ Verifique no Supabase **Table Editor** se as tabelas foram criadas

### **Erro 500 no Vercel**
- ✅ Vá em **Deployments** → **Functions** → Veja os logs
- ✅ Procure por erros de import ou conexão

---

## 📱 Usando no Celular

Depois do deploy:
1. Abra a URL no navegador do celular
2. **Adicione à tela inicial:**
   - **iPhone:** Safari → Compartilhar → "Adicionar à Tela Inicial"
   - **Android:** Chrome → Menu → "Adicionar à tela inicial"
3. Agora você tem um "app" no celular! 📲

---

## 🔄 Atualizações Futuras

Quando você fizer mudanças no código:
1. **Push pro GitHub**
2. Vercel **rebuilda automaticamente**
3. Pronto! Site atualizado.

---

## 💾 Backup de Dados

**Importante:** Seus dados estão no Supabase (não no Vercel).

Para fazer backup:
1. Supabase → **Database** → **Backups**
2. Ou exporte via SQL:
```sql
-- No SQL Editor do Supabase
COPY (SELECT * FROM users) TO STDOUT WITH CSV HEADER;
```

---

## 📞 Suporte

Problemas? Verifique:
1. ✅ Variáveis de ambiente corretas no Vercel
2. ✅ Tabelas criadas no Supabase
3. ✅ Connection string válida
4. ✅ Logs do Vercel (Deployments → Functions)

---

**Feito com 💜 - DailyBasisRoute v2.0**
