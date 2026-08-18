from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import cv2
import numpy as np
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ============================================
# CARREGAR MODELO
# ============================================
MODEL_PATH = "best_roboflow.pt"

if os.path.exists(MODEL_PATH):
    print(f"✅ Modelo encontrado: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
else:
    print(f"❌ Modelo NÃO encontrado: {MODEL_PATH}")
    print("   Verifique se o arquivo está na pasta correta!")
    model = None

# ============================================
# NOVA ORDEM DAS CLASSES (ROBOFLOW)
# ============================================
CLASS_NAMES = [
    "Plastico_PEAD",             # ID 0
    "Plastico_PET_Colorido",     # ID 1
    "Plastico_PET_Transparente", # ID 2
    "Plastico_PET_Verde",        # ID 3
    "Vidro",                     # ID 4
    "metal",                     # ID 5
    "papel"                      # ID 6
]

# ============================================
# PASTA ONDE ESTÁ O INDEX.HTML
# ============================================
HTML_FOLDER = r"C:\Users\Eduardo\Desktop\ecoclassify-backand"

# ============================================
# ROTAS
# ============================================

@app.route("/")
def home():
    """Rota principal - verifica se API está online"""
    return jsonify({
        "status": "online",
        "modelo": "Roboflow YOLOv8",
        "classes": len(CLASS_NAMES),
        "classes_nomes": CLASS_NAMES,
        "endpoints": {
            "html": "/app",
            "deteccao": "/detect"
        }
    })

@app.route("/app")
def serve_app():
    """Serve o index.html"""
    try:
        return send_from_directory(HTML_FOLDER, 'index.html')
    except Exception as e:
        return jsonify({
            "erro": f"Não foi possível carregar o HTML: {str(e)}",
            "pasta_esperada": HTML_FOLDER
        }), 404

@app.route("/detect", methods=["POST"])
def detect():
    """Rota de detecção de objetos"""
    
    if model is None:
        return jsonify({
            "error": "Modelo não carregado. Verifique se best_roboflow.pt está na pasta.",
            "detections": []
        }), 500
    
    try:
        # Verificar tipo de conteúdo
        if request.content_type == 'application/octet-stream':
            # RAW data (enviado pelo HTML)
            npimg = np.frombuffer(request.data, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        else:
            # JPEG/PNG via FormData
            file = request.files["image"]
            npimg = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({
                "error": "Não foi possível decodificar a imagem",
                "detections": []
            }), 400

        # Fazer predição
        results = model(img, conf=0.5, verbose=False)

        detections = []
        for r in results:
            boxes = r.boxes
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    if len(box.xyxy) > 0:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        class_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else f"Classe_{class_id}"
                        
                        detections.append({
                            "class_name": class_name,
                            "class_id": class_id,
                            "confidence": round(confidence, 4),
                            "bbox": [int(x1), int(y1), int(x2), int(y2)]
                        })

        return jsonify({
            "detections": detections,
            "count": len(detections),
            "status": "success"
        })

    except Exception as e:
        print(f"❌ Erro na detecção: {str(e)}")
        return jsonify({
            "error": str(e),
            "detections": [],
            "status": "error"
        }), 500

# ============================================
# INICIAR SERVIDOR
# ============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("♻️  EcoClassify - API de Classificação de Resíduos")
    print("="*60)
    print(f"📦 Modelo: {MODEL_PATH}")
    print(f"🏷️  Classes: {len(CLASS_NAMES)}")
    print(f"📋 Classes: {', '.join(CLASS_NAMES)}")
    print("-"*60)
    print(f"🌐 Acesse o sistema: http://127.0.0.1:5000/app")
    print(f"🔍 Verificar API: http://127.0.0.1:5000/")
    print("-"*60)
    print("Pressione CTRL+C para encerrar")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)