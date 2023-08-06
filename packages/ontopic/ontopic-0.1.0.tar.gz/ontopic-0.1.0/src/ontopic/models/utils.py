import torch
from torch.utils.data import DataLoader, Dataset


class TopicDataset(Dataset):
    def __init__(self, abstracts, tokenizer, max_len, targets=None):
        self.abstracts = abstracts
        self.tokenizer = tokenizer
        self.max_len = max_len
        if targets is not None:
            self.targets = targets
        else:
            self.targets = [None] * len(abstracts)

    def __len__(self):
        return len(self.abstracts)

    def __getitem__(self, item):
        abstract = str(self.abstracts[item])
        target = self.targets[item]
        encoding = self.tokenizer.encode_plus(
            abstract,
            add_special_tokens=True,
            max_length=self.max_len,
            truncation=True,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'abstract_text': abstract,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'targets': torch.tensor(target, dtype=torch.long)
        }


def create_data_loader(abstracts, tokenizer, max_len, batch_size, targets=None):
    ds = TopicDataset(
        abstracts=abstracts,
        targets=targets,
        tokenizer=tokenizer,
        max_len=max_len
    )

    return DataLoader(
        ds,
        batch_size=batch_size,
        num_workers=0
    )
