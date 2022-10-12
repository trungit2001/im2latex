# config data upload
UPLOAD_FOLDER = "./app/static/images/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# config model
MODEL_CONFIG = {
    "use_cuda": False,
    "weights_path": "./app/data/weights/best_ckpt.pt",
    "data_path": "./app/data/",
    "max_len": 150,
    "beam_size": 5,
    "seed": 2022
}

BASE_URL = "https://im2latex.up.railway.app/"