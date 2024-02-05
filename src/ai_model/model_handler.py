"""
ModelHandler class is responsible for handling AI model.
"""

import os
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageFile
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import requests

from ai_model.neural_network_model import NeuralNetworkModel
from predicted_class import PredictedClass
from label_class_mapper import LabelClassMapper
from date_to_str import DateToStr, DateNameType
from commandline_args_parser import CommandLineArgsParser

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ModelHandler:
    """
    Class representing a AI model, responsible for creating dataset of .jpg files
    collected by robotic car, training neural networks and classyfing images.
    """

    def __init__(self, commandline_args_parser: CommandLineArgsParser):
        self._set_workspace()
        self._select_device()
        self._create_paths_to_datasets()

        self._path_to_models_directory = "trained_models/"

        self._define_transform()
        self._load_datasets()
        self._classes_amount = len(self._train_dataset.classes)
        if commandline_args_parser.get_mode() == "train":
            self._epochs_amount = commandline_args_parser.get_epochs()
            self._batch_size = commandline_args_parser.get_batch()

            self._create_data_loaders()
            self._init_model()
        if commandline_args_parser.get_mode() == "run":
            model_name = commandline_args_parser.get_model()
            try:
                self._load_model(model_name)
            except FileNotFoundError as ex:
                raise ex


    def _set_workspace(self):
        current_workspace = str(Path(__file__).parent)
        os.chdir(current_workspace)


    def _select_device(self):
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


    def _create_paths_to_datasets(self):
        path_to_datasets = "../../dataset/"
        train_dataset_subdirectory = "train"
        test_dataset_subdirectory = "test"

        self._train_dataset_directory = f"{path_to_datasets}{train_dataset_subdirectory}"
        self._test_dataset_directory = f"{path_to_datasets}{test_dataset_subdirectory}"


    def _define_transform(self):
        self._transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])


    def _load_datasets(self):
        self._train_dataset = ImageFolder(
            root=self._train_dataset_directory,
            transform=self._transform
        )
        self._test_dataset = ImageFolder(
            root=self._test_dataset_directory,
            transform=self._transform
        )


    def _create_data_loaders(self):
        self._train_loader = DataLoader(
            dataset=self._train_dataset,
            batch_size=self._batch_size,
            shuffle=True,
            num_workers=8,
            pin_memory=True
        )
        self._test_loader = DataLoader(
            dataset=self._test_dataset,
            batch_size=self._batch_size,
            shuffle=False,
            num_workers=8,
            pin_memory=True
        )


    def _init_model(self):
        self._model = NeuralNetworkModel(self._classes_amount).to(self._device)
        self._criterion = nn.CrossEntropyLoss()
        self._optimizer = optim.Adam(self._model.parameters(), lr=0.001)


    def train_model(self):
        """Method to run training the AI model"""
        print(f"Device: {self._device}\n")

        print("Test before training")
        self._test()

        print("Start training...")
        self._train()

        print("Test after training")
        self._test()

        self._save_model()


    def _train(self):
        """Model training"""
        for epoch in range(self._epochs_amount):
            print(f"Epoch {epoch + 1} starts")

            train_accuracy, avg_train_loss = self._epoch_train()

            print(f"Epoch [{epoch + 1}/{self._epochs_amount}] stats:")
            print(f"    Train accuracy: {train_accuracy:.4f}")
            print(f"    Avg train loss: {avg_train_loss:.4f}")


    def _epoch_train(self):
        self._model.train()
        train_loss = 0
        correct_samples = 0
        total_samples = 0

        for images, labels in self._train_loader:
            images, labels = images.to(self._device), labels.to(self._device)

            self._optimizer.zero_grad()
            outputs = self._model(images)
            loss = self._criterion(outputs, labels)
            loss.backward()
            self._optimizer.step()
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            total_samples += labels.size(0)
            correct_samples += predicted.eq(labels).sum().item()

        train_accuracy = correct_samples / total_samples
        avg_train_loss = train_loss/len(self._train_loader)

        return (train_accuracy, avg_train_loss)


    def _test(self):
        """Model testing"""
        self._model.eval()
        test_loss = 0
        test_correct = 0
        test_samples = 0

        for images, labels in self._test_loader:
            images, labels = images.to(self._device), labels.to(self._device)

            outputs = self._model(images)
            loss = self._criterion(outputs, labels)
            loss.backward()
            test_loss += loss.item()
            _, predicted_class = torch.max(outputs, 1)
            test_correct += (predicted_class == labels).sum().item()
            test_samples += labels.size(0)

        test_accuracy = test_correct / test_samples
        avg_test_loss = test_loss/len(self._test_loader)

        print("Test stats:")
        print(f"    Test accuracy: {test_accuracy:.4f}")
        print(f"    Avg test loss: {avg_test_loss:.4f}")


    def classify_image(self, response: requests.models.Response) -> PredictedClass:
        """Image classification based on trained model."""
        image = Image.open(BytesIO(response.content)).convert('RGB')
        image = self._transform(image).unsqueeze(0).to(self._device)

        self._model.eval()

        with torch.no_grad():
            output = self._model(image)

        _, predicted_class = torch.max(output, 1)
        predicted_class = predicted_class.item()

        predicted_label = self._train_dataset.classes[predicted_class]
        predicted = LabelClassMapper.map_label_to_class(predicted_label)

        return predicted


    def _save_model(self):
        name_based_on_time = DateToStr.parse_date(DateNameType.DATE_HOUR_MINUTE)
        filename = f"epochs_{self._epochs_amount}_batch_{self._batch_size}_{name_based_on_time}.pt"
        model_path = self._path_to_models_directory + filename

        self._set_workspace()
        torch.save(self._model, model_path)
        print(f"Model saved in {model_path}")


    def _load_model(self, model_name: str="") -> bool:
        self._set_workspace()
        path = self._path_to_models_directory + model_name
        try:
            self._model = torch.load(path)
        except FileNotFoundError as ex:
            raise ex

        self._model.eval()


if __name__ == "__main__":
    command_line_parser = CommandLineArgsParser()
    model = ModelHandler(command_line_parser)
