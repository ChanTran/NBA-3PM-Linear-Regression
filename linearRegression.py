import pandas as pd
import playerScraper as ps
import numpy as np  
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def main():
    dataFrame = ""
    try:
        choice = input("Would you like to enter a bbref url (Y) or player name (N)? (Y/N): ")
        if choice.lower() == "y":
            url = input("Enter a BBREF URL (ex. https://www.basketball-reference.com/players/h/hardeja01.html): ")
            dataFrame = ps.openURL(url)
        elif choice.lower() == "n":
            player = input("Enter a player name (First Last, ex: James Harden): ")
            dataFrame = ps.openURL(ps.createURL(player))
        else:
            print("Please enter a valid choice")
            exit()
        #Plot 3P vs PTS
        dataFrame.plot(x='PTS', y='3P', style='o')  
        plt.title('3P vs PTS Relation')  
        plt.xlabel('PTS')  
        plt.ylabel('3P')  
        plt.show()
        createXYset(dataFrame)
    except IndexError:
        print("Please enter a valid player name.")
    except ValueError:
        print("Player not found.")
    
def createXYset(df):
    X = df['PTS'].values.reshape(-1,1)
    y = df['3P'].values # we want to predict 3 points made based off of how many points scored in a season
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    #create the model and train it
    regressor = LinearRegression()  
    model = regressor.fit(X_train, y_train)
    #Now predict
    y_pred = regressor.predict(X_test)
    vals = np.array([])
    valsPoints = np.array([])
    #Print actual and predicted values
    for val in y_test:
        for i in range(df.shape[0]-1, -1, -1):
            if df['3P'][i] == val:
                vals = np.append(vals, df['Season'][i])
                valsPoints = np.append(valsPoints, df['PTS'][i])
                break
    data = pd.DataFrame({'Season': vals, 'Actual 3PM': y_test, 'Predicted 3PM': y_pred, 'Points': valsPoints})
    print(data)
    print("R^2 value (data follows linear model if it's closer to 1 than 0): " + str(model.score(X_test,y_test)))
    #print("MSE value (lower loss = better predictions): " + str(metrics.mean_squared_error(y_test, y_pred)))
    #Plot linear line
    plt.scatter(X_test, y_test,  color='blue')
    plt.plot(X_test, y_pred, color='black', linewidth=3)
    plt.title('3P vs PTS Relation')  
    plt.xlabel('PTS')  
    plt.ylabel('3PM')  
    plt.show()
    
    
def mse_loss(y_true, y_pred):
  return ((y_true - y_pred) ** 2).mean()

main()