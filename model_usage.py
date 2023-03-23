# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Read in the CSV file
df = pd.read_csv('/Users/rishabhsolanki/Desktop/Github/electricity_usage/IntervalData.csv')

# convert the USAGE_DATE column to a datetime object
df['USAGE_DATE'] = pd.to_datetime(df['USAGE_DATE'])

# create new columns for the day, month, and hour
df['DAY'] = df['USAGE_DATE'].dt.day
df['MONTH'] = df['USAGE_DATE'].dt.month

# Extract the hour from the 'USAGE_START_TIME' column and convert it to an integer
df['HOUR'] = df['USAGE_START_TIME'].apply(lambda x: int(x.split(':')[0]))

# Drop rows containing NaN values
df = df.dropna(subset=['USAGE_KWH'])


# Prepare the data for training
features = ['DAY', 'MONTH', 'HOUR']
target = 'USAGE_KWH'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the random forest regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Predict the max electricity usage time for a given day and month
def predict_max_usage_time(day, month):
    # create a dataframe containing all hours of the day for the given day and month
    hours = list(range(0, 24))
    input_data = pd.DataFrame({'DAY': [day] * 24, 'MONTH': [month] * 24, 'HOUR': hours})

    # make predictions
    predictions = model.predict(input_data)

    # find the hour with the maximum predicted usage
    max_hour = hours[predictions.argmax()]

    return max_hour

# Example usage: predict the max usage time for day 23 and month 8
day = 2
month = 8
max_hour = predict_max_usage_time(day, month)
print(f"The predicted max electricity usage time for day {day} and month {month} is hour {max_hour}.")

# Scatter plot of actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Electricity Usage (kWh)')
plt.show()
