"""
DeskDetect — YOLOv8 Masaüstü Nesne Tespiti
Yerel Gradio uygulaması.

Çalıştırmak için:  python app.py
Tarayıcıda açılır: http://127.0.0.1:7860
"""

from collections import defaultdict
from pathlib import Path

import gradio as gr
import numpy as np
from PIL import Image
from ultralytics import YOLO

# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------

MODEL_PATH = Path(__file__).parent / "best.pt"
EXAMPLES_DIR = Path(__file__).parent / "ornekler"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model dosyası bulunamadı: {MODEL_PATH}\n"
        "best.pt dosyasını app.py ile aynı klasöre koyun."
    )

model = YOLO(str(MODEL_PATH))
CLASS_NAMES = list(model.names.values())

print(f"Model yüklendi: {MODEL_PATH.name}")
print(f"Sınıflar ({len(CLASS_NAMES)}): {', '.join(CLASS_NAMES)}")

# Eğitim sonuçları — ADIM 4 değerlendirme çıktısından
METRICS = {
    "precision": 0.525,
    "recall": 0.388,
    "map50": 0.402,
    "map50_95": 0.280,
}

# Sınıf bazında mAP50-95
PER_CLASS = [
    ("laptop", 0.589),
    ("mouse", 0.488),
    ("keyboard", 0.326),
    ("cup", 0.315),
    ("bottle", 0.255),
    ("cell phone", 0.202),
    ("backpack", 0.038),
    ("book", 0.031),
]


# --------------------------------------------------------------------------
# Tespit
# --------------------------------------------------------------------------

def detect(image, confidence, iou):
    """Görseli modele verir, kutulu görsel ve tespit özeti döndürür."""

    if image is None:
        return None, _empty_summary("Başlamak için bir fotoğraf yükleyin.")

    results = model.predict(
        source=image,
        conf=confidence,
        iou=iou,
        verbose=False,
    )
    result = results[0]

    # plot() BGR döndürür; ::-1 ile RGB'ye çevrilir. Oluşan dizi
    # C-contiguous olmadığı için Image.fromarray bazı Pillow sürümlerinde
    # hata verir — ascontiguousarray bunu garantiye alır.
    annotated = np.ascontiguousarray(result.plot()[:, :, ::-1])
    annotated = Image.fromarray(annotated)

    if result.boxes is None or len(result.boxes) == 0:
        return annotated, _empty_summary(
            "Hiçbir nesne tespit edilemedi. "
            "Güven eşiğini düşürmeyi deneyin."
        )

    # Aynı sınıftan birden fazla nesneyi tek satırda topla
    per_class = defaultdict(list)
    for box in result.boxes:
        per_class[model.names[int(box.cls[0])]].append(float(box.conf[0]))

    rows = []
    for name, confs in sorted(per_class.items(), key=lambda kv: -max(kv[1])):
        rows.append(
            f"| {name} | {len(confs)} | {max(confs):.1%} | "
            f"{sum(confs) / len(confs):.1%} |"
        )

    summary = (
        f"### {len(result.boxes)} nesne tespit edildi\n\n"
        "| Sınıf | Adet | En yüksek | Ortalama |\n"
        "|---|---:|---:|---:|\n" + "\n".join(rows)
    )

    return annotated, summary


def _empty_summary(message):
    return f"### Sonuç\n\n{message}"


def _collect_examples():
    """ornekler/ klasöründeki görselleri Gradio örnekleri olarak toplar."""
    if not EXAMPLES_DIR.is_dir():
        return []

    suffixes = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    files = sorted(
        path for path in EXAMPLES_DIR.iterdir()
        if path.suffix.lower() in suffixes
    )
    return [[str(path), 0.25, 0.45] for path in files]


# --------------------------------------------------------------------------
# Arayüz
# --------------------------------------------------------------------------

CSS = """
.gradio-container { max-width: 1200px !important; margin: 0 auto !important; }

#header {
    border: 1px solid var(--border-color-primary);
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 18px;
    background: var(--background-fill-secondary);
}
#header h1 {
    margin: 0 0 6px;
    font-size: 1.6rem;
    font-weight: 650;
    letter-spacing: -0.015em;
}
#header p { margin: 0; color: var(--body-text-color-subdued); font-size: 0.94rem; }

.chips { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 14px; }
.chip {
    font-size: 0.78rem;
    padding: 4px 11px;
    border-radius: 999px;
    border: 1px solid var(--border-color-primary);
    color: var(--body-text-color-subdued);
    font-variant-numeric: tabular-nums;
}

.panel {
    border: 1px solid var(--border-color-primary);
    border-radius: 12px;
    padding: 18px 20px;
    background: var(--background-fill-primary);
}
.panel h3 {
    margin: 0 0 12px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--body-text-color-subdued);
}
.panel table { font-size: 0.88rem; width: 100%; }
.panel td, .panel th { padding: 5px 8px; }

.metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.metric {
    border: 1px solid var(--border-color-primary);
    border-radius: 10px;
    padding: 12px 14px;
    text-align: center;
}
.metric .value {
    font-size: 1.32rem;
    font-weight: 650;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
}
.metric .label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--body-text-color-subdued);
    margin-top: 3px;
}

.bar-row {
    display: grid;
    grid-template-columns: 92px 1fr 46px;
    align-items: center;
    gap: 10px;
    margin-bottom: 7px;
    font-size: 0.84rem;
}
.bar-track {
    height: 7px;
    border-radius: 4px;
    background: var(--background-fill-secondary);
    overflow: hidden;
}
.bar-fill { height: 100%; border-radius: 4px; background: var(--color-accent); }
.bar-value {
    text-align: right;
    font-variant-numeric: tabular-nums;
    color: var(--body-text-color-subdued);
}
"""

chips = "".join(f'<span class="chip">{name}</span>' for name in CLASS_NAMES)

metric_cards = "".join(
    f'<div class="metric"><div class="value">{value:.3f}</div>'
    f'<div class="label">{label}</div></div>'
    for label, value in [
        ("mAP50", METRICS["map50"]),
        ("mAP50-95", METRICS["map50_95"]),
        ("Precision", METRICS["precision"]),
        ("Recall", METRICS["recall"]),
    ]
)

bars = "".join(
    f'<div class="bar-row"><span>{name}</span>'
    f'<span class="bar-track"><span class="bar-fill" style="width:{score / 0.6 * 100:.0f}%"></span></span>'
    f'<span class="bar-value">{score:.3f}</span></div>'
    for name, score in PER_CLASS
)

with gr.Blocks(theme=gr.themes.Soft(), css=CSS, title="DeskDetect") as demo:

    gr.HTML(
        f"""
        <div id="header">
            <h1>DeskDetect</h1>
            <p>YOLOv8 ile masaüstü nesne tespiti — 8 sınıf, COCO 2017 alt kümesi ile eğitildi.</p>
            <div class="chips">{chips}</div>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(
                type="pil",
                label="Fotoğraf",
                height=420,
                sources=["upload", "clipboard"],
            )
            confidence = gr.Slider(
                0.05, 0.95, value=0.25, step=0.05,
                label="Güven eşiği (conf)",
                info="Düşürürsen daha çok ama daha az güvenilir tespit görürsün.",
            )
            iou = gr.Slider(
                0.10, 0.90, value=0.45, step=0.05,
                label="Kutu birleştirme eşiği (IoU)",
                info="Aynı nesne için çakışan kutular bu eşiğe göre eleniyor.",
            )
            with gr.Row():
                run_button = gr.Button("Tespit Et", variant="primary", scale=3)
                clear_button = gr.ClearButton(value="Temizle", scale=1)

        with gr.Column(scale=1):
            output_image = gr.Image(
                type="pil",
                label="Sonuç",
                height=420,
                interactive=False,
            )
            summary = gr.Markdown(_empty_summary("Başlamak için bir fotoğraf yükleyin."))

    examples = _collect_examples()
    if examples:
        gr.Examples(
            examples=examples,
            inputs=[input_image, confidence, iou],
            label="Örnek fotoğraflar",
            examples_per_page=6,
        )
    else:
        gr.Markdown(
            "*Örnek fotoğraf eklemek için `ornekler/` klasörü oluşturup içine "
            "birkaç görsel koyun, uygulamayı yeniden başlatın.*"
        )

    with gr.Accordion("Model bilgisi", open=False):
        gr.HTML(
            f"""
            <div class="panel">
                <h3>Genel performans (doğrulama seti)</h3>
                <div class="metrics">{metric_cards}</div>
            </div>

            <div class="panel" style="margin-top:14px">
                <h3>Sınıf bazında mAP50-95</h3>
                {bars}
                <p style="font-size:0.82rem;color:var(--body-text-color-subdued);margin:12px 0 0">
                    <strong>book</strong> ve <strong>backpack</strong> belirgin şekilde düşük.
                    COCO'da kitaplar genelde raf veya yığın halinde, onlarca küçük nesne olarak
                    etiketleniyor; sırt çantaları da çoğunlukla kısmen görünür durumda.
                    Bu iki sınıf literatürde de COCO'nun en zorları arasında sayılıyor.
                </p>
            </div>

            <div class="panel" style="margin-top:14px">
                <h3>Eğitim yapılandırması</h3>
                <table>
                    <tr><td>Mimari</td><td><strong>YOLOv8n</strong> (nano)</td></tr>
                    <tr><td>Veri kaynağı</td><td>COCO 2017 — yalnızca hedef 8 sınıf</td></tr>
                    <tr><td>Eğitim / doğrulama</td><td>1200 / 250 görsel</td></tr>
                    <tr><td>Epoch</td><td>50 (patience 15)</td></tr>
                    <tr><td>Görüntü boyutu</td><td>640 × 640</td></tr>
                    <tr><td>Batch</td><td>16</td></tr>
                </table>
            </div>
            """
        )

    run_button.click(
        fn=detect,
        inputs=[input_image, confidence, iou],
        outputs=[output_image, summary],
    )
    clear_button.add([input_image, output_image, summary])


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        inbrowser=True,
    )
