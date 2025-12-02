# ✨ TrucoLab — Test Intelligence Dashboard  
Um laboratório digital para analisar, visualizar e compreender o comportamento dos testes do projeto de Truco.  
Aqui, código encontra ciência, e ciência encontra poesia — tudo em gráficos, cores e indicadores que contam histórias.  

---

## 🎯 Visão Geral

O **TrucoLab** é uma ferramenta que coleta, organiza e transforma resultados do **pytest** em um dashboard visual de altíssima clareza.  
Ele permite enxergar:

- ✔️ Status geral dos testes  
- 📊 Quantidade de testes por arquivo  
- ⚠️ Falhas por módulo  
- 🚀 Os testes mais lentos  
- ⏱️ Tempos e médias de execução  
- 📈 Histórico simbólico de performance  
- 🪄 E tudo isso reunido num PDF lindão para documentação  

O objetivo é simples:  
> **Transformar o caos dos testes em beleza, controle e visão.**

---

## 🌌 Características Principais

### 🥧 Dashboard Gráfico Completo  
Gera um painel visual com:

- Gráficos de pizza com status dos testes  
- Barras horizontais por arquivo  
- Falhas distribuídas por origem  
- Linha temporal para observar tendência  
- Lista elegante dos testes mais lentos  

Tudo isso com um tema escuro e vibes de “monitor futurista”.

---

## 📄 Exportação em PDF  
Além da imagem PNG, o projeto gera automaticamente um **PDF em página inteira**, perfeito para:

- Documentações  
- Relatórios internos  
- Entrega de sprints  
- Arquivos profissionais de auditoria  

---

## 🔧 Como Funciona

1. Rode o pytest com captura de resultados  
2. O script `run_tests_with_graph.py`:

   - Executa os testes  
   - Extrai estatísticas  
   - Gera gráficos  
   - Renderiza o dashboard  
   - Exporta PNG + PDF  

Simples, rápido e mágico.

---

## 🚀 Como Usar

### 1️⃣ Instalar dependências
```bash
pip install pytest matplotlib reportlab
```

## 2️⃣ Rodar o script de testes e gerar dashboard

```bash
python3 run_tests_with_graph.py
```

## 3️⃣ Resultado

🖼️ dashboard_testes_beautiful.png

📄 dashboard_testes.pdf
Aparecem automaticamente na pasta do projeto.

## 🗂 Estrutura do Projeto

```
/
├── src/                 # Código do jogo Truco e lógica
├── test/                # Testes unitários com pytest
├── run_tests_with_graph.py  # Script de geração do dashboard
├── dashboard_testes.png     # Painel visual (auto-gerado)
├── dashboard_testes.pdf     # Relatório final (auto-gerado)
└── README.md
```

## 💡 Por que TrucoLab?

- Porque testes não precisam ser cinzas.
- Eles podem ser poéticos, bonitos, visíveis.
- Podem contar a trajetória de um projeto — suas quedas, suas vitórias, sua evolução.

- O TrucoLab te permite enxergar a alma dos seus testes.

## 🛠 Tecnologias

- Python
- Pytest
- Matplotlib
- ReportLab
- Amor por dashboards bonitos ❤️

### 🤝 Contribuições

Pull Requests são super bem-vindos.
<br />
Aqui, cada insight vira melhoria e cada melhoria reflete diretamente na qualidade do projeto.

