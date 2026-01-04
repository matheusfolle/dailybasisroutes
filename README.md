# 🎯 DailyBasisRoute v2.0

Sistema completo de gerenciamento de rotina gamificado com analytics, notas diárias e integração com IA.

## ✨ Funcionalidades

### 🔐 Sistema de Autenticação
- Login e cadastro de usuários
- Sessões seguras com bcrypt
- Dados isolados por usuário

### 📊 Dashboard Principal
- Checklist de tarefas diárias com 3 categorias:
  - **Pilares Fixos** (40pts): Devocional, rotina de sono
  - **Cardápio de Estudos** (40pts): DS/Python, inglês, SQL, atividade física, leitura
  - **Bônus Extras** (20pts): Obsidian, treino eficiente, pedal extra
- **Tarefas do Dia:** Adicione tarefas pontuais (cortar grama, lavar carro, etc)
- Sistema de pontos (100pts/dia)
- Contador de streak (sequência de dias 60+pts)
- Progresso semanal em tempo real
- **Campo de notas diárias** com auto-save

### 📈 Analytics
- Gráfico semanal (últimos 7 dias)
- Gráfico mensal (últimos 30 dias)
- Estatísticas:
  - Média semanal/mensal
  - Taxa de sucesso (60+ pontos)
  - Melhor dia

### 📜 Histórico
- Últimos 30 dias com pontuação
- Notas de cada dia
- Badges de desempenho

### 🤖 Integração com IA
- Botão "Exportar Dados" copia JSON completo
- Cole no Claude para análises personalizadas
- Dados incluem: tarefas, pontos, notas, datas

## 🛠️ Tecnologias

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Banco de Dados:** SQLite
- **Gráficos:** Chart.js
- **Autenticação:** Werkzeug Security (bcrypt)

## 🚀 Como Usar

### 1. Instalação

```bash
# Clone ou baixe o projeto
cd dailybasisroute_v2

# Instale as dependências
pip install flask --break-system-packages

# Rode o servidor
python3 app.py
```

### 2. Acesso

Abra o navegador em: `http://localhost:5000`

### 3. Primeiro Uso

1. Clique em **"Cadastro"**
2. Preencha nome, email e senha
3. Tarefas padrão serão criadas automaticamente
4. Comece a marcar suas atividades!

### 4. Uso Diário

1. Acesse o **Dashboard**
2. Marque tarefas conforme completa
3. Escreva uma nota sobre o dia
4. Acompanhe sua pontuação e streak

### 5. Análise com IA

1. Clique em **"Exportar Dados"**
2. Cole no Claude (ou outro assistente)
3. Peça análises tipo:
   - "Analise meus padrões de produtividade"
   - "Quais dias tive melhor desempenho?"
   - "Identifique correlações entre tarefas"

## 📊 Sistema de Pontos

**Sistema realista e sustentável:**

- **Meta diária:** 60+ pontos = mantém streak ✨
- **Máximo possível:** 100 pontos/dia
- **Categorias:**
  - **Pilares (40pts):** Base essencial - devocional, sono, acordar
  - **Cardápio (40pts):** Estudos e desenvolvimento - escolha suas prioridades
  - **Bônus (20pts):** Extras e eficiência

### **Breakdown detalhado:**

**PILARES FIXOS (40pts):**
- 🙏 Devocional Diário: 20pts (manhã OU noite)
- 😴 Dormiu antes 23h: 10pts
- ⏰ Acordou cedo sem voltar: 10pts

**CARDÁPIO FLEXÍVEL (40pts):**
- 💪 Atividade Física: 15pts (qualquer tipo!)
- 📊 Estudo DS/Python: 15pts
- 🗣️ Inglês: 10pts
- 🗄️ SQL: 10pts
- 📖 Leitura: 10pts

**BÔNUS EXTRAS (20pts):**
- 📝 Obsidian: 5pts
- ⚡ Treino Focado: 5pts
- 🚴 Pedal Extra: 10pts

**Filosofia:** O sistema prioriza consistência sobre perfeição. A maioria dos dias deve atingir 60+ pontos naturalmente, sem exaustão.

## 🎯 Filosofia

Baseado em conceitos japoneses:

- **Kaizen:** Melhoria contínua (1% melhor por dia)
- **Ikigai:** Propósito diário
- **Wabi-sabi:** Aceitar imperfeições
- **Kintsugi:** Força nas quedas e recuperações

## 📁 Estrutura do Projeto

```
dailybasisroute_v2/
├── app.py                  # Backend Flask
├── dailybasisroute.db      # Banco SQLite (criado automaticamente)
├── templates/
│   ├── login.html          # Página de login/cadastro
│   ├── dashboard.html      # Dashboard principal
│   ├── analytics.html      # Gráficos e estatísticas
│   └── historico.html      # Histórico de 30 dias
└── static/
    └── css/
        └── style.css       # Estilos completos
```

## 🔧 Banco de Dados

**Tabelas:**
- `users` - Usuários do sistema
- `tasks` - Definições de tarefas
- `daily_logs` - Registros diários de conclusão
- `notes` - Notas diárias
- `streaks` - Controle de sequências

## 📱 Deploy (Opcional)

### Vercel/Railway

1. Substitua SQLite por PostgreSQL
2. Configure variáveis de ambiente
3. Deploy normal

### Render/Fly.io

1. Adicione `requirements.txt`:
```
Flask==3.0.0
```

2. Configure Procfile/Dockerfile
3. Deploy

## 💡 Ideias Futuras

- [ ] Timeline de aprendizado visual
- [ ] Seção Ikigai Lab
- [ ] Correlações automáticas (ML)
- [ ] Widget mobile
- [ ] Exportar PDF mensal
- [ ] Integração Google Calendar
- [ ] Modo multiplayer/competição

## 📝 Licença

MIT - Use à vontade!

---

**Desenvolvido com 💜 por Matheus (Folle)**

*"Sua rotina quantificada, sua evolução visualizada"*
