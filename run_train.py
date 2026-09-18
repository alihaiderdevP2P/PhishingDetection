"""Convenience launcher: python run_train.py"""

from src.dataset import write_dataset
from src.train import train_and_compare

if __name__ == "__main__":
    write_dataset()
    results = train_and_compare()
    print(f"Best model: {results['best_model']}")
