# ASL Buddy
A game developed for Hack the Northeast 2020 that challenges you to beat your high score while learning the ASL alphabet. Awarded Most Viable Startup at HTNE.

# Requirements
This project uses Python3, OpenCV, Tensorflow 2 Pygame, as well as other libraries outlined in the requirements.txt.

# Before running this project
Before running the application, train the model using 
```
python3 train.py \
  --bottleneck_dir=logs/bottlenecks \
  --how_many_training_steps=2000 \
  --model_dir=inception \
  --summaries_dir=logs/training_summaries/basic \
  --output_graph=logs/trained_graph.pb \
  --output_labels=logs/trained_labels.txt \
  --image_dir=./dataset
```
This will build Inception and train a model inside of a directory called logs. The logs directory is essential for running the actual game application. Training the model may take up to an hour (training_steps parameter is adjustable).

More options outlined in [Inception](https://github.com/tensorflow/models/blob/master/research/inception/README.md).



# Run ASL Buddy
```
python3 game.py
```



