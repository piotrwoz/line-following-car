# line-following-car

Software of line following robotic car made as an project for deep reinforcement learning course during 2nd semester of Master's studies at Gdansk University of Technology.

## Requirements

* Python 3.10

Python modules:

* pyTorch
* requests
* yaml

## Usage

To be able to connect with robotic car, you have to create Wi-Fi hotspot with proper netowork name and password. If done correctly, car should connect with hotsport automatically when turned on. Then put network name, IPv4 address and network password in [network.yaml](settings/network.yaml) settings file as a value for `network-name`, `ipv4` and `password` keys.

This software runs in 2 modes: `train` and `run`. `train` mode is responsible for training Convolutional Neural Network model for image classification which is used for self-steering of robotic car. You need to specify `epochs` and `batch` as command line arguments when starting application. Those arguments should be positive integers. When model is trained, you can run this software in `run` mode which will start car drive. You have to specify command line parameters as `time` of drive in seconds and `model` which is name of previously trained model, which should be placed in [trained_models](src/ai_model/trained_models) directory. `time` should be a positive integer and `model` is a string. Optionally, you can add `music` parameter, which will play music in the background when car is driving. It should be `true`, `on`, `false` or `off`.

### Train

To train CNN model, get into [src](src/) directory and run following command:

```bash
python3 main.py --mode train --epochs epochs_amount --batch batch_size
```

for example:

```bash
python3 main.py --mode train --epochs 10 --batch 16
```

### Run

To start car drive get into [src](src/) directory and run following command:

```bash
python3 main.py --mode run --time driving_times --model model_name.pt --music if_music
```

for example:

```bash
python3 main.py --mode run --time 20 --model my_model.pt --music on
```

## Results

Trained CNN model is stored in [trained_models](src/ai_model/trained_models) directory.

## License

[MIT](https://choosealicense.com/licenses/mit/)
