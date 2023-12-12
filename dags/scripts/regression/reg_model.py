# import os
import pickle
from sqlalchemy import create_engine
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error


def load_data_from_postgres():
    # Establish connection to the database
    # db_uri = os.environ['LOCAL_POSTGRES_URI']
    db_uri = "postgresql+psycopg2://myuser:mypassword@localhost:1234/mydatabase"
    engine = create_engine(db_uri)

    sql_query = """
    SELECT a.date, consumption, price FROM tr_electricity_consumption a
    INNER JOIN tr_electricity_price b ON a.date = b.date
    """

    # Execute the SQL query and save the result into a Pandas DataFrame
    df = pd.read_sql_query(sql_query, engine)

    df['date'] = pd.to_datetime(df['date'])

    # Lag variables for price and consumption based on hourly intervals
    for lag in [1, 6, 24, 48, 168]:  # Lag values in hours for 1 hour, 6 hours, 1 day, 2 days, and 7 days
        df[f'Price_Lag_{lag}_Hour'] = df['price'].shift(lag)
        df[f'Consumption_Lag_{lag}_Hour'] = df['consumption'].shift(lag)

    df.drop(['date', 'consumption'], axis=1, inplace=True)  # , 'price'
    return df


def train_random_forest_model(df):
    target_variable = 'price'  # Choose the target variable based on your lag values

    X = df.drop(target_variable, axis=1)  # Drop the target variable from the DataFrame to get the features
    y = df[target_variable]

    # Create a HistGradientBoostingRegressor model
    gradient_boosting = HistGradientBoostingRegressor(random_state=42)

    # Train the model
    gradient_boosting.fit(X, y)  # Use all data except the last row for training

    return gradient_boosting


def test_model_and_save(random_forest, df):
    target_variable = 'price'
    # Get the last 2 rows for testing
    y_test = df[target_variable].tail(2)
    X_test = df.drop(target_variable, axis=1).tail(2)

    # Make predictions
    y_pred = random_forest.predict(X_test)

    # Print predictions and actual values
    print(f"Predictions: {y_pred}")
    print(f"Actual: {y_test}")

    # Calculate error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Save the trained model
    pickle.dump(random_forest, open("model.pkl", "wb"))


# Main function performing the operations
def main():
    # Load data
    data = load_data_from_postgres()

    # Train model
    trained_model = train_random_forest_model(data)

    # Test and save the model
    test_model_and_save(trained_model, data)


if __name__ == "__main__":
    main()
