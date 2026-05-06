# 🌿 Análise de Dados Ambientais – Pantanal

**Autora:** Mariana Sanchez Pedroni  
**Processo Seletivo:** Bolsista – Perfil 1: Desenvolvimento de Plataforma de Dados Ambientais  
**Instituição:** Instituto Nacional de Pesquisa do Pantanal (INPP) / MCTI

---

## 📋 Descrição

Script Python para leitura, tratamento e visualização dos dados ambientais do arquivo `dados_pantanal.csv`, contendo temperatura do ar (°C), nível do rio (m) e índice de vegetação NDVI ao longo de 10 dias em janeiro de 2025.

---

## 📁 Estrutura do Projeto

```
pantanal_analise/
├── analise_pantanal.py        # Script principal
├── dados_pantanal.csv         # Dados brutos originais
├── requirements.txt           # Dependências do projeto
├── README.md                  # Este arquivo
└── outputs/                   # Gerado automaticamente
    ├── grafico1_series_temporais.png
    ├── grafico2_correlacao_medias.png
    └── dados_pantanal_tratados.csv
```

---

## ⚙️ Requisitos

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`:

```
pandas>=2.0.0
matplotlib>=3.7.0
numpy>=1.24.0
```

---

## 🚀 Instruções de Execução

**1. Clone ou baixe o repositório:**
```bash
git clone <url-do-repositorio>
cd pantanal_analise
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

> Ou usando um ambiente virtual (recomendado):
> ```bash
> python -m venv venv
> source venv/bin/activate      # Linux/macOS
> venv\Scripts\activate         # Windows
> pip install -r requirements.txt
> ```

**3. Execute o script:**
```bash
python analise_pantanal.py
```

Os gráficos e o CSV tratado serão gerados automaticamente na pasta `outputs/`.

---

## 🔍 Decisões Técnicas

### 1. Linguagem e Bibliotecas
Escolhi **Python** por ser a linguagem padrão em análise de dados científicos e ambientais. As bibliotecas utilizadas (`pandas`, `matplotlib`, `numpy`) são amplamente adotadas, bem documentadas e de código aberto.

### 2. Tratamento de Valores Ausentes — Interpolação Linear
O dataset apresenta 4 valores ausentes distribuídos em `nivel_rio_m` (dias 03 e 07) e `ndvi` (dias 04 e 09).

**Abordagem escolhida:** interpolação linear temporal.

**Justificativa:** variáveis ambientais como nível de rio e NDVI variam de forma contínua e suave ao longo do tempo. A interpolação linear utiliza os valores adjacentes para estimar o ponto faltante, preservando a tendência real da série. Alternativas como preenchimento pela **média global** seriam inadequadas pois ignorariam a dinâmica temporal (ex.: um pico de temperatura não seria capturado).

Os pontos interpolados são sinalizados nos gráficos com marcadores em branco para rastreabilidade.

### 3. Gráfico 1 — Séries Temporais em Painéis Independentes
Optei por três subgráficos separados (temperatura, nível do rio, NDVI) em vez de um único gráfico de eixo duplo. **Motivo:** as unidades e escalas são completamente distintas (°C, metros, índice 0–1); sobrepor em um único eixo distorceria visualmente as magnitudes e dificultaria a leitura.

### 4. Gráfico 2 — Dispersão + Barras de Médias
O painel duplo combina:
- **Scatter Temperatura × NDVI** (com coloração pelo nível do rio e linha de tendência): permite verificar visualmente se temperaturas mais altas estão associadas a menor vigor vegetal — hipótese relevante para o Pantanal em períodos de seca.
- **Barras de médias:** oferecem um resumo estatístico rápido e comparativo das três variáveis para o período analisado.

---

## 📊 Resultados

| Variável          | Média   | Mínimo | Máximo | Desvio Padrão |
|-------------------|---------|--------|--------|---------------|
| Temperatura (°C)  | 33.95   | 31.80  | 36.00  | 1.41          |
| Nível do Rio (m)  | 4.49    | 4.20   | 4.80   | 0.20          |
| NDVI              | 0.6815  | 0.65   | 0.72   | 0.023         |

---

## 📌 Observações

- O script é modular: cada etapa (leitura, tratamento, estatísticas, visualização) está encapsulada em funções independentes, facilitando manutenção e expansão futura.
- A pasta `outputs/` é criada automaticamente caso não exista.
- O CSV com os dados tratados é exportado para permitir reuso em outras ferramentas (ex.: QGIS, Power BI, R).