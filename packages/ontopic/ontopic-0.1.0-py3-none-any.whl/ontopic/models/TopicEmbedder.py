from torch import nn, load
from transformers import AutoModel, AutoTokenizer
from typing import Iterable, Optional
import torch

from utils import create_data_loader


class TopicEmbedder(nn.Module):

    def __init__(self,
                 trained: Optional[bool]=True,
                 pre_trained_name: Optional[str] = 'allenai/scibert_scivocab_uncased',
                 device: Optional[str] = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                 ):

        super(TopicEmbedder, self).__init__()
        self.pre_trained_name = pre_trained_name
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(self.pre_trained_name)
        if trained:
            self.embedding_model = load("models/trained/embeddings/scibert_scivocab_1.pt")
            self.eval()
        else:
            self.embedding_model = AutoModel.from_pretrained(self.pre_trained_name)

        self.to(self.device)

    def forward(self, input_ids, attention_mask):
        model_output = self.embedding_model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        return model_output.last_hidden_state.mean(axis=1)

    def embed(self, data: Iterable[str], max_len=256, batch_size=16):
        embeddings = torch.empty(0, self.embedd.config.hidden_size).to(self.device)
        data_loader = create_data_loader(data, self.tokenizer, max_len, batch_size, targets=None)

        for d in data_loader:
            input_ids = d["input_ids"].to(self.device)
            attention_mask = d["attention_mask"].to(self.device)
            embeddings = torch.cat((embeddings, self.forward(input_ids, attention_mask)), 0)
        return embeddings

