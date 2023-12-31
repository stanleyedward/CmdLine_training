"""
trains a model
"""

import os
import torch
from torchvision import transforms
from pytorch_modules.modules import data_preprocess, train_engine, build_model, utils

import argparse

#create a parser
parser = argparse.ArgumentParser(description="Hyperparamter tuning for model training.")

#get an arg for epochs
parser.add_argument("--epochs",
                    default=10,
                    type=int,
                    help="number of epochs to train the model")
#get an arf ffor abtchsize
parser.add_argument("--batch_size",
                    default=32,
                    type=int,
                    help="batch size of the dataloader")
#get an arg for hidden units
parser.add_argument("--hidden_units",
                    type=int,
                    default=10,
                    help="no of hidden units in the model architecture")
#get an arg for learning rate
parser.add_argument("--lr",
                    default=0.001,
                    type=float,
                    help="set learning rate of the optimizer")
#gettingargs from the parser
args = parser.parse_args()

# setup hyperparameters
NUM_EPOCHS = args.epochs
BATCH_SIZE = args.batch_size
HIDDEN_UNITS = args.hidden_units
LEARNING_RATE = args.lr

print(f"training a model with: \nepochs {NUM_EPOCHS} \nbatch_size {BATCH_SIZE} \nhidden_units {HIDDEN_UNITS}\n learning_rate {LEARNING_RATE}")

# setup directories
train_dir = "data/pizza_steak_sushi/train"
test_dir = "data/pizza_steak_sushi/test"

# Ssetup target device
device = "cuda" if torch.cuda.is_available() else "cpu"

# create transforms
data_transform = transforms.Compose([
  transforms.Resize((64, 64)),
  transforms.ToTensor()
])

# create DataLoaders with help from data_setup.py
train_dataloader, test_dataloader, class_names = data_preprocess.create_dataloaders(
    train_dir=train_dir,
    test_dir=test_dir,
    transform=data_transform,
    batch_size=BATCH_SIZE
)

# create model with help from model_builder.py
model = build_model.TinyVGG(
    input_shape=3,
    hidden_units=HIDDEN_UNITS,
    output_shape=len(class_names)
).to(device)

# set loss and optimizer
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),
                             lr=LEARNING_RATE)

# Start training with help from engine.py
train_engine.train(model=model,
             train_dataloader=train_dataloader,
             test_dataloader=test_dataloader,
             loss_fn=loss_fn,
             optimizer=optimizer,
             epochs=NUM_EPOCHS,
             device=device)

# Save the model with help from utils.py
utils.save_model(model=model,
                 target_dir="models",
                 model_name="dummy_model.pth")
