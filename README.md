# ♻️ EcoClassify - Sistema de Classificação de Resíduos Recicláveis

## 📋 Sobre o Projeto

Sistema web para classificação automatizada de resíduos recicláveis utilizando **Visão Computacional** e **YOLOv8**, com detecção em **tempo real** via webcam.

### 🎯 Funcionalidades
- ✅ Detecção em tempo real com caixas delimitadoras
- ✅ Classificação de 7 tipos de resíduos
- ✅ Interface web responsiva (Vue.js)
- ✅ API REST (Flask + Python)
- ✅ Suporte a múltiplos modelos YOLOv8

### 🏷️ Classes Detectadas
| ID | Classe | Descrição |
|:--:|--------|-----------|
| 0 | Plastico_PEAD | Frascos opacos (shampoo, detergente) |
| 1 | Plastico_PET_Colorido | Garrafas PET coloridas |
| 2 | Plastico_PET_Transparente | Garrafas PET cristalinas |
| 3 | Plastico_PET_Verde | Garrafas PET verdes |
| 4 | Vidro | Todos os tipos de vidro |
| 5 | Metal | Latas e objetos metálicos |
| 6 | Papel | Papéis e papelão |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python 3.10+** | Backend e treinamento |
| **Flask** | API REST |
| **YOLOv8 (Ultralytics)** | Modelo de detecção |
| **Vue.js 2** | Frontend reativo |
| **Axios** | Comunicação HTTP |
| **OpenCV** | Processamento de imagem |
| **Google Colab** | Treinamento com GPU T4 |
| **Roboflow** | Dataset e anotações |

---

## 📁 Estrutura do Projeto

ecoclassify-backand/
├── api.py # API Flask (backend)
├── index.html # Interface web (frontend)
├── requirements.txt # Dependências Python
├── .gitignore # Arquivos ignorados
├── README.md # Este arquivo
└── best_roboflow.pt # Modelo treinado (não incluso no GitHub)


---

## 🚀 Como Executar

### 1. Clonar o repositório

git clone https://github.com/EduardoSantos19/EcoClassify.git
cd EcoClassify

2.Instalar dependências

pip install -r requirements.txt

3. Baixar o modelo treinado

O modelo best_roboflow.pt está disponível na pasta do projeto.

4. Executar a API

python api.py


5. Acessar o sistema

Abra o navegador e acesse:

http://127.0.0.1:5000/app


📊 Dataset e Treinamento

O modelo foi treinado utilizando dataset do Roboflow com as seguintes configurações:
Parâmetro	Valor
Arquitetura	YOLOv8 Nano
Resolução	320x320
Batch Size	32
Épocas	50
Early Stopping	10 épocas

📄 Licença

Este projeto é parte do Trabalho de Conclusão de Curso de Ciência da Computação da UNIP - 2026.
🙏 Agradecimentos

Professor Orientador Lauro Tomiatti

Universidade Paulista (UNIP)

Comunidade Open Source (Ultralytics, Flask, Vue.js)
