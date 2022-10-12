import os
import torch

from flask import Flask
from app.settings import (
    UPLOAD_FOLDER, MODEL_CONFIG
)
from app.models.model import Im2LatexModel
from app.models.decoder import LatexProducer
from app.models.text import Vocab, build_vocab

# create flask instance
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

seed = MODEL_CONFIG["seed"]
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)

# config model im2latex
use_cuda = MODEL_CONFIG["use_cuda"]
device = torch.device("cuda" if use_cuda else "cpu")

vocab = build_vocab(MODEL_CONFIG["data_path"])

checkpoint = torch.load(os.path.join(MODEL_CONFIG["weights_path"]), map_location=torch.device(device))
model_args = checkpoint["args"]

model = Im2LatexModel(
    out_size=len(vocab),
    emb_size=model_args.emb_dim,
    dec_rnn_h=model_args.dec_rnn_h,
    add_pos_feat=model_args.add_position_features,
    dropout=model_args.dropout
)
model.to(device)
model.load_state_dict(checkpoint["model_state_dict"])

# model decoder
latex_producer = LatexProducer(
    model=model,
    vocab=vocab,
    use_cuda=use_cuda,
    max_len=MODEL_CONFIG["max_len"],
    beam_size=MODEL_CONFIG["beam_size"]
)

from app.views import *