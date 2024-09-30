import torch
import numpy as np
from typing import Tuple
from torch.utils.data import TensorDataset
from cifar import load_cifar
from mnist import load_mnist
from data_fashion import load_fashion
from synthetic import make_chebyshev_dataset, make_linear_dataset
# from wikitext import load_wikitext_2

DATASETS = [
    "cifar10", "cifar10-nonst", "cifar10-1k", "cifar10-2k", "cifar10-5k", "cifar10-5k-nonst", "cifar10-10k", "cifar10-20k",
    "mnist", "mnist-5k", "mnist-10k", "mnist-20k",
    "fashion", "fashion-5k", "fashion-10k"
    "chebyshev-3-20", "chebyshev-4-20", "chebyshev-5-20", "linear-50-50"
]

def flatten(arr: np.ndarray):
    return arr.reshape(arr.shape[0], -1)

def unflatten(arr: np.ndarray, shape: Tuple):
    return arr.reshape(arr.shape[0], *shape)

def num_input_channels(dataset_name: str) -> int:
    if dataset_name.startswith("cifar10"):
        return 3
    elif dataset_name == 'fashion' or dataset_name == "mnist":
        return 1

def image_size(dataset_name: str) -> int:
    if dataset_name.startswith("cifar10"):
        return 32
    elif dataset_name == 'fashion' or dataset_name == "mnist":
        return 28

def num_classes(dataset_name: str) -> int:
    if dataset_name.startswith('cifar10'):
        return 10
    elif dataset_name == 'fashion' or dataset_name == "mnist":
        return 10

def get_pooling(pooling: str):
    if pooling == 'max':
        return torch.nn.MaxPool2d((2, 2))
    elif pooling == 'average':
        return torch.nn.AvgPool2d((2, 2))
    else:
        raise NotImplementedError("unknown pooling: {}".format(pooling))

def num_pixels(dataset_name: str) -> int:
    return num_input_channels(dataset_name) * image_size(dataset_name)**2

def take_first(dataset: TensorDataset, num_to_keep: int):
    return TensorDataset(dataset.tensors[0][0:num_to_keep], dataset.tensors[1][0:num_to_keep])

def load_dataset(dataset_name: str, loss: str) -> (TensorDataset, TensorDataset):
    if dataset_name == "cifar10":
        return load_cifar(loss)
    elif dataset_name == "cifar10-nonst":
        return load_cifar(loss, standardize_data=False)
    elif dataset_name == "cifar10-1k":
        train, test = load_cifar(loss)
        return take_first(train, 1000), test
    elif dataset_name == "cifar10-2k":
        train, test = load_cifar(loss)
        return take_first(train, 2000), test
    elif dataset_name == "cifar10-5k":
        train, test = load_cifar(loss)
        return take_first(train, 5000), test
    elif dataset_name == "cifar10-5k-nonst":
        train, test = load_cifar(loss, standardize_data=False)
        return take_first(train, 5000), test
    elif dataset_name == "cifar10-10k":
        train, test = load_cifar(loss)
        return take_first(train, 10000), test
    elif dataset_name == "cifar10-20k":
        train, test = load_cifar(loss)
        return take_first(train, 20000), test
    elif dataset_name == 'mnist':
        return load_mnist(loss)
    elif dataset_name == "mnist-5k":
        train, test = load_mnist(loss)
        return take_first(train, 5000), test
    elif dataset_name == "mnist-10k":
        train, test = load_mnist(loss)
        return take_first(train, 10000), test
    elif dataset_name == "mnist-20k":
        train, test = load_mnist(loss)
        return take_first(train, 20000), test
    elif dataset_name == 'fashion':
        return load_fashion(loss)
    elif dataset_name == "fashion-5k":
        train, test = load_fashion(loss)
        return take_first(train, 5000), test
    elif dataset_name == "chebyshev-5-20":
        return make_chebyshev_dataset(k=5, n=20)
    elif dataset_name == "chebyshev-4-20":
        return make_chebyshev_dataset(k=4, n=20)
    elif dataset_name == "chebyshev-3-20":
        return make_chebyshev_dataset(k=3, n=20)
    elif dataset_name == 'linear-50-50':
        return make_linear_dataset(n=50, d=50)

