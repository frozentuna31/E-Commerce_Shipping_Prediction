from flask import Flask, request, render_template
import requests
from flask_cors import cross_origin
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("e_commerce_shipment.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        
        #Numerical Columns

        # ID
        ID = request.form["ID"]

        # Customer Calls
        Customer_care_calls = float(request.form["Customer_Calls"])
        
        # Customer Rating
        Customer_rating = float(request.form["Customer_Rating"])

        # Purchase Priority
        Prior_purchases = float(request.form["Purchase_Priority"])

        # Cost Product
        Cost_of_the_Product = float(request.form["Cost_product"])
        
        # Discount Offered
        Discount_offered = float(request.form["Discount_offered"])

        # Weight
        Weight_in_gms = float(request.form["Weight"])

        #Categorical Columns
        
        # Warehouse_block
        Warehouse_block=request.form['Warehouse_block']
        if(Warehouse_block=='A'):
            B = 0
            C = 0
            D = 0
            F = 0

        elif(Warehouse_block=='B'):
            B = 1
            C = 0
            D = 0
            F = 0

        elif(Warehouse_block=='C'):
            B = 0
            C = 1
            D = 0
            F = 0
            
        elif(Warehouse_block=='D'):
            B = 0
            C = 0
            D = 1
            F = 0
            
        elif(Warehouse_block=='F'):
            B = 0
            C = 0
            D = 0
            F = 1
            
        #Mode_of_Shipment
        Mode_of_Shipment=request.form['Mode_of_Shipment']
        if(Mode_of_Shipment=='Flight'):
            Road = 0
            Ship = 0
            
        elif(Mode_of_Shipment=='Road'):
            Road = 1
            Ship = 0
            
        elif(Mode_of_Shipment=='Ship'):
            Road = 0
            Ship = 1
        
        #Product_Importance
        Product_importance=request.form['Product_Importance']
        if Product_importance == "Low":
            Product_importance = 1

        elif Product_importance == "Medium":
            Product_importance = 2

        elif Product_importance == "High":
            Product_importance = 3
            

        #Gender
        Gender=request.form['Gender']
        if Gender == "Male":
            M = 1

        elif Gender == "Female":
            M = 0

        #Data scaling in Continous Numerical Data
        from sklearn.preprocessing import StandardScaler
        standardization = StandardScaler()
        continous_num = np.array([Discount_offered,Weight_in_gms,Cost_of_the_Product])
        num_df= pd.DataFrame(data=continous_num)
        continous_std = standardization.fit_transform(num_df)

        #Standardized Data
        Discount_offered = float(continous_std[0])
        Weight_in_gms = float(continous_std[1])
        Cost_of_the_Product = float(continous_std[2])


        prediction=model.predict([[
            Customer_care_calls,
            Customer_rating,
            Cost_of_the_Product,
            Prior_purchases,
            Discount_offered,
            Weight_in_gms,
            B,
            C,
            D,
            F,
            Road,
            Ship,
            Product_importance,
            M
            ]])

        output=round(prediction[0],2)
        if prediction == 0:
            return render_template('home.html',prediction_text="Your package with ID {} will arrive on time!!".format(ID))
        elif prediction == 1:
            return render_template('home.html',prediction_text="Your package with ID {} will arrive late!!".format(ID))

    
    return render_template("home.html")




if __name__ == "__main__":
    app.run(debug=False)