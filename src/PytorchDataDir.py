from utils import *
import hydra
from omegaconf import DictConfig
import os
import wget

def my_app(cfg: DictConfig) -> None:
    pytorch_data_dir = cfg.pytorch_data_dir
    print(pytorch_data_dir)

if __name__ == "__main__":
    prep_args()
    my_app()