
# Real Time Emotion Recognition from text using Deep learning and Feedback Analysis





## Description

This project involves the development of an innovative system for emotion recognition from text using deep learning techniques, coupled with feedback analysis. It aims to offer organizations insights into customer sentiments expressed in feedback data, and  facilitates customers with quick issue resolution. It also provides better visualization of customer emotions for data analysis.
## Software Requirements

1. Editor for HTML, CSS, Python, Flask, Streamlit - VS Code
2. Google Chrome, Firefox, Microsoft Edge or Brave Browser
3. Google collab and kaggle notebooks for training.
4. Python(Version 3.0 or Greater)
5. Flask Library
6. Keras/TensorFlow Library
7. Pandas
8. NLTK Library
9. smtp Library
10. Streamlit Library
11. Glove Word Embeddings
12. XAMPP - MYSQL Database
13. Flask-MySQLdb
14. Autocorrect
## Installations

1. Clone or download the project repository from GitHub.
2. Install the required software dependencies listed in the "Software Requirements" section.
3. Open the MySQL server in XAMPP and create a database named *customer*. 
    
    * Create a *customer_info* table with fields name, email, age, gender, location, order_id(primary key), product_name, feedback and emotion.

    * Create a *orders_table* table with fields order_id(primary key), product_name, cust_name.
3. Set up the development environment on your development machine.
## Usage

1. Start the **Apache** and **MySQL** server in XAMPP.
2. Navigate to the project directory on your development machine.
3. To start the **Feedback Form** in the live server:

    * Run the *App_new.py* script using the command ***python App_new.py***
    
    * This will start the server and you can access the feedback form through the provided URL at localhost:5000.
4. To access the **Owner's Dashboard** open a new terminal:

    * Change the directory using the command [cd Dashboard](https://github.com/aTul-07kn/Real-Time-Emotion-Detection-from-Text/tree/master/Dashboard)
    
    * Run the *dashboard.py* script using the command ***streamlit run dashboard.py***

    * This will start the Streamlit server in your default web browser at localhost:8501.
5. To access the **Manager's Portal** open a new terminal:

    * Change the directory using the command [cd emaildashboard](https://github.com/aTul-07kn/Real-Time-Emotion-Detection-from-Text/tree/master/emaildashboard)

    * Run the *email_dashboard.py* script using the command ***python email_dashboard.py***

    * This will open the managers portal on a live server at localhost:3000.

6. To close the servers press ***ctrl+c*** in each terminal.

## Screenshots
1. Feedback Form

[![Feedback-form.jpg](https://i.postimg.cc/TPT4DSJX/Feedback-form.jpg)](https://postimg.cc/QFnmLfz6)

2. Managers Portal

[![Managers-Portal.jpg](https://i.postimg.cc/HxhZFLDp/Managers-Portal.jpg)](https://postimg.cc/sQ54hsg8)

3. Owner's Dashboard

[![Owners-Dashboard.png](https://i.postimg.cc/FRf0tkXZ/Owners-Dashboard.png)](https://postimg.cc/1nQ8wttn)

4. Mail to Customer

[![Email-to-customer-for-negative-feedback.jpg](https://i.postimg.cc/d0tKYDXd/Email-to-customer-for-negative-feedback.jpg)](https://postimg.cc/4YM0v4XN)

5. Mail to Customer Executive

[![Email-to-customer-executive.jpg](https://i.postimg.cc/t4kL2pTg/Email-to-customer-executive.jpg)](https://postimg.cc/PCL3qG1G)

*To see all the execution photos open [Project Execution Photos](https://github.com/aTul-07kn/Real-Time-Emotion-Detection-from-Text/tree/master/Project%20Execution%20Photos) directory*

## Credits

* Atul Kumar Nayak [GitHub](https://github.com/aTul-07kn)
* A. Rohan [GitHub](https://github.com/rohu2504)
* G. Kausthub Rao [GitHub](https://github.com/KausthubProjectSpace)
* K. Midhilesh [GitHub](https://github.com/Midhilesh13)