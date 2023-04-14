import torch

class Negative_summary_dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Negative_summary_dataset(train_encodings, train_labels)
val_dataset = Negative_summary_dataset(val_encodings, val_labels)

test_dataset = Negative_summary_dataset(test_encodings, test_labels)