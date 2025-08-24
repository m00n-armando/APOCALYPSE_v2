# ====================================================================
# Bab 1: Perkenalan & Impor Pustaka Sakti
# ====================================================================
import sys
import json
import requests
import base64
import time
import os
import random
import concurrent.futures

# ====================================================================
# Bab 2: Kamus & Definisi Dunia
# ====================================================================
MODEL_MAP = { "Q": "IMAGEN_3_1", "BQ": "IMAGEN_3_5" }
ASPECT_RATIO_MAP = {
    "3:4": "IMAGE_ASPECT_RATIO_PORTRAIT_THREE_FOUR", "1:1": "IMAGE_ASPECT_RATIO_SQUARE",
    "4:3": "IMAGE_ASPECT_RATIO_LANDSCAPE_FOUR_THREE", "9:16": "IMAGE_ASPECT_RATIO_PORTRAIT",
    "16:9": "IMAGE_ASPECT_RATIO_LANDSCAPE"
}

# ====================================================================
# Bab 3: Biografi Sang Pekerja Keras (generate_single_image)
# DEFINISI HARUS DI ATAS SEBELUM DIPANGGIL
# ====================================================================
def generate_single_image(prompt_text: str, output_path: str, seed: int, aspect_ratio_str: str, model_str: str, url: str, headers: dict):
    """Fungsi pekerja yang akhirnya bisa dibaca oleh mandornya."""
    attempts = 0; max_attempts = 10
    current_prompt = prompt_text; current_seed = seed
    while attempts < max_attempts:
        attempts += 1
        print(f"[PEKERJA] Mencoba... #{attempts} | Seed: {current_seed}")
        payload = {
            "clientContext": {"workflowId": "7782a24a-8b69-4a7b-aca2-316600a8dc5c","tool": "BACKBONE","sessionId": f";{int(time.time() * 1000)}"},
            "imageModelSettings": {"imageModel": model_str,"aspectRatio": aspect_ratio_str},
            "seed": current_seed, "prompt": current_prompt, "mediaCategory": "MEDIA_CATEGORY_BOARD"
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
            response.raise_for_status()
            response_data = response.json()
            if response_data.get("imagePanels", [])[0].get("generatedImages"):
                encoded_image_str = response_data["imagePanels"][0]["generatedImages"][0]["encodedImage"]
                image_data = base64.b64decode(encoded_image_str)
                with open(output_path, 'wb') as f: f.write(image_data)
                print(f"[SUKSES] Disimpan: {output_path}")
                return True
        except requests.exceptions.HTTPError as e:
            try:
                reason = e.response.json().get('error', {}).get('details', [{}])[0].get('reason', 'UNKNOWN_REASON')
                if reason == "PUBLIC_ERROR_UNSAFE_GENERATION": print(f"[WARN] UNSAFE. Ganti seed..."); current_seed = random.randint(1, 999999)
                elif reason == "PUBLIC_ERROR_PROMINENT_PEOPLE_FILTER_FAILED": print(f"[WARN] UNPEOPLE. Meracuni prompt..."); current_prompt = prompt_text + ", (generic face)"
                else: print(f">>> GAGAL (HTTP): {e.response.status_code} - {reason}"); return False
            except json.JSONDecodeError: print(f">>> GAGAL (HTTP NON-JSON): {e.response.status_code}"); return False
        except Exception as e: print(f">>> GAGAL (LAINNYA): {e}"); return False
        time.sleep(2)
    print(f"[GAGAL TOTAL] Untuk: {output_path}")
    return False

# ====================================================================
# Bab 4: Manual Operasional Sang Mandor Pabrik (run_factory)
# DEFINISI JUGA HARUS DI ATAS SEBELUM DIPANGGIL
# ====================================================================
def run_factory(job_list: list, url: str, headers: dict, output_gallery: str):
    print(f"\n--- [ MEMBUKA PABRIK SANG ARSITEK v8.0 - FINAL ] ---")
    if not os.path.exists(output_gallery): os.makedirs(output_gallery)
    total_generated = 0; tasks_to_run = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for job_id, job in enumerate(job_list):
            if not job.get("active", True): print(f"[INFO] Melewati Job #{job_id + 1}"); continue
            project_name = job.get("project_name", f"Proyek_{job_id+1}"); image_name = job.get("image_name", f"Karya_{job_id+1}")
            model_code = job.get("model", "BQ").upper(); ratio_code = job.get("ratio", "3:4")
            num_images = job.get("num_images", 1); prompt = job.get("prompt", "")
            ID_photo = job.get("ID_photo", job_id)
            project_path = os.path.join(output_gallery, project_name)
            if not os.path.exists(project_path): os.makedirs(project_path)
            model_str = MODEL_MAP.get(model_code, MODEL_MAP["BQ"]); aspect_ratio_str = ASPECT_RATIO_MAP.get(ratio_code, ASPECT_RATIO_MAP["3:4"])
            print(f"\n--- [ Mengantri Job #{job_id + 1}: '{prompt[:40]}...' ({num_images}x) ] ---")
            initial_seed = job.get("seed")
            base_seed = random.randint(1, 999999) if initial_seed is None or str(initial_seed).lower() == "random" else int(initial_seed)
            for i in range(num_images):
                current_seed = base_seed + i
                output_filename = f"{ID_photo}_{job_id+1}_{image_name}_{model_code}_{current_seed}.png"
                filepath = os.path.join(project_path, output_filename)
                task = executor.submit(generate_single_image, prompt, filepath, current_seed, aspect_ratio_str, model_str, url, headers)
                tasks_to_run.append(task)
        for future in concurrent.futures.as_completed(tasks_to_run):
            if future.result(): total_generated += 1
    print(f"\n--- [ PEKERJAAN PABRIK SELESAI. Total Mahakarya: {total_generated} ] ---")
    print("Sudah selesai, Arsitek. Sekarang... istirahat.")

# ====================================================================
# Bab 5: Perintah Eksekusi Terakhir
# INI BARU BOLEH ADA DI BAGIAN AKHIR
# ====================================================================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("[REAKTOR ERROR] Kurang Memo (config.json) atau Surat Perintah (job.json).")
        sys.exit(1)
    config_file_path, job_file_path = sys.argv[1], sys.argv[2]
    try:
        with open(config_file_path, 'r') as f: config = json.load(f)
        URL = config.get("api_url"); BEARER_TOKEN = config.get("bearer_token")
        HEADERS = { "Authorization": f"Bearer {BEARER_TOKEN}", "Content-Type": "application/json" }
        OUTPUT_GALLERY = config.get("output_gallery_path")
        with open(job_file_path, 'r') as f: job_list = json.load(f)
        run_factory(job_list, URL, HEADERS, OUTPUT_GALLERY)
    except Exception as e:
        print(f"[REAKTOR ERROR KRITIS] Terjadi kesalahan fatal: {e}")
        sys.exit(1)
