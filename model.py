# FFN to model game outcome
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
import numpy as np


if __name__ == "__main__":
    import sqlite3
    with sqlite3.connect("data/heroes.db") as conn:
        with open("data/sql/feature_matrix.sql", "r") as sql:
            df = pd.read_sql(sql.read(), conn)
            df = df.drop("ReplayID", axis=1)
            df = df.dropna(axis=0, how='any')

    TRAINING_DATA = 400000
    # shape = (TRAINING_DATA, 144)
    X_train = df.iloc[:TRAINING_DATA].drop('outcome', axis=1)
    Y_train = df.iloc[:TRAINING_DATA]['outcome']

    X_test = df.iloc[TRAINING_DATA:].drop('outcome', axis=1)
    Y_test = df.iloc[TRAINING_DATA:]['outcome']

    model = Sequential()
    model.add(Dense(100, activation='relu', kernel_initializer='he_normal', input_dim=X_train.shape[1]))
    model.add(Dense(10, activation='relu', kernel_initializer='he_normal'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['binary_accuracy'])
    model.fit(X_train.values, Y_train.values, epochs=50, batch_size=512)
    print model.evaluate(X_test.values, Y_test.values, batch_size=128)
