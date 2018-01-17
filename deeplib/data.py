import math
import random
import numpy as np
import torch
import torch.utils.data
from torch.utils.data.sampler import SubsetRandomSampler
from deeplib.datasets import load_mnist
from torchvision.transforms import ToTensor, Compose

class SpiralDataset(torch.utils.data.Dataset):

    def __init__(self, n_points=500, noise=0.2):
        self.points = torch.Tensor(n_points, 7)
        self.labels = torch.IntTensor(n_points)

        n_positive = n_points // 2
        n_negative = n_points = n_positive

        for i, point in enumerate(self._gen_spiral_points(n_positive, 0, noise)):
            self.points[i], self.labels[i] = point, 1

        for i, point in enumerate(self._gen_spiral_points(n_negative, math.pi, noise)):
            self.points[i+n_positive] = point
            self.labels[i+n_positive] = -1


    def _gen_spiral_points(self, n_points, delta_t, noise):
        for i in range(n_points):
            r = i / n_points * 5
            t = 1.75 * i / n_points * 2 * math.pi + delta_t
            x = r * math.sin(t) + random.uniform(-1, 1) * noise
            y = r * math.cos(t) + random.uniform(-1, 1) * noise
            yield torch.Tensor([x, y, x**2, y**2, x*y, math.sin(x), math.sin(y)])


    def __len__(self):
        return len(self.labels)


    def __getitem__(self, i):
        return self.points[i], self.labels[i]


    def to_numpy(self):
        return self.points.numpy(), self.labels.numpy()


def train_valid_loaders(dataset, batch_size, train_split=0.8, shuffle=True):
    num_data = len(dataset)
    indices = np.arange(num_data)
    split = math.floor(train_split * num_data)

    if shuffle == True:
        np.random.shuffle(indices)

    train_idx, valid_idx = indices[split:], indices[:split]

    train_sampler = SubsetRandomSampler(train_idx)
    valid_sampler = SubsetRandomSampler(valid_idx)

    train_loader = torch.utils.data.DataLoader(dataset,
                    batch_size=batch_size, sampler=train_sampler)
    valid_loader = torch.utils.data.DataLoader(dataset,
                    batch_size=batch_size, sampler=valid_sampler)

    return train_loader, valid_loader

