# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import pandas as pd

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)

###### Training Test
# # Test
# num_classes = 26

# # Creates path to training data
# train_fp, test_fp = "Project/archive/sign_mnist_train.csv", "Project/archive/sign_mnist_test.csv"

# train_df, test_df = pd.read_csv(train_fp), pd.read_csv(test_fp)

# # Creates objects for inputs (x_train) and expected outputs (y_train)
# x_train, y_train = train_df.iloc[:, :0].values, train_df['label'].values

# x_test, y_test = test_df.iloc[:, :0].values, test_df['label'].values

# # PEEEEEEE
# print("hi")