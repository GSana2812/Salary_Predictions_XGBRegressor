In this project, I have approached a Regression Task, predicting salaries of Data Professionals, based on some components, such as:

1. Company Size (Small/Medium/Large)
2. Experience Level (Entry/Mid/Senior/Executive)
3. Employment Type (Full Time/Part Time/Freelance/Contract)
4. Job Titles (AI Engineer/Data Scientist etc)
5. Company Location (US/UK/Canada etc) -> top 10 countries with most data taken

I have used XGBRegressor for making predictions, because in another alternate file, it yielded better results compared to Linear Regression, 
DecisionTreeRegressor and RandomForestRegressor. The training and test results were really similar, so fortunately we didn't encounter any overfitting and the results were
pleasible, so we did a good job with the data preprocessing. 

I decided to transfer this project interface, in a more dynamic way, so a web app using streamlit library. There are 2 sections, the <b>predict</b> and <b>explore</b> section.
In the predict, based on the components shown, you can play around with values and in the end you will get the predicted salary while on explore you have a representation of 
charts and trends. 

Feel free to experiment with the app: <b> streamlit run app.py </b>

At a second moment, this app can be easily deployed in streamlit cloud community or another platform like docker. But this will probably take place with upcoming projects. 

Libraries used: pandas, numpy, sklearn, warnings, streamlit, xgboost, matplotlib, plotly, seaborn
