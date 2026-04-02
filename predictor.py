import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def run_predictions():

    try:
        df = pd.read_csv("academic_data.csv")
    except FileNotFoundError:
        print("Run fetch_data before running predictor.py.")
        return
    courses = df['course'].unique()

    weights_map = {    #A list of weights for each assignment. Higher number means the model places more emphasis, lower means less.
        "test": 0.50,
        "exam": 0.50,
        "interpretive": 0.5,
        "presentational":0.5,
        "interpersonal":0.5,
        "quiz": 0.20,
        "homework":0.10,
        "webassign": 0.05,
        "warmup":0.05,

    }

    for course in courses:
        
        c_data=df[df['course']==course].copy()
        row_weights = []
        for assignment_name in c_data['name']:
            assigned_weight = 0.1
            for keyword, value in weights_map.items():
                if keyword in assignment_name.lower():
                    assigned_weight = value
                    break
            row_weights.append(assigned_weight)
        if len(c_data)<3:
            print(f"Course has less than 3 assignments, mean is {c_data['percent'].mean()}")
            continue
        X=np.array(range(len(c_data))).reshape(-1,1)
        y=c_data['percent'].values

        model = LinearRegression()
        model.fit(X,y,sample_weight=row_weights)

        prediction=model.predict([[len(c_data)+5]])[0]
        prediction=max(0,min(prediction,100))
        print(f"The model predicts a {prediction:.2f}% in {course}")
        
if __name__ == "__main__":
    run_predictions()