import os # interact with operating system
import json # allows to encode and decode json objects
import datetime # to represent date and time
import csv # to handle csv file which store data in tabular format in a row, seperated by " , "
import nltk # Natural Language tool kit
import ssl # Secore Sockets Layer- provides encryption
import streamlit as st # to build user interfaces
import random 
from sklearn.feature_extraction.text import TfidfVectorizer 
# sklearn.feature_extraction.text - used to extract features in a format supported by machine learning algorythms forjm dateset consisting os format such as text and images 
# TfidfVectorizer- (Term Frequency Inverse Document Frequency); it converts text document into vectors based on the relevancy of words.
from sklearn.linear_model import LogisticRegression
# linear_model - used to predict new data points
# LogisticRegression- to solve classification problems

ssl._create_default_https_context = ssl._create_unverified_context

# Load intents form the JSON file
file_path=os.path.abspath("./pyintends.json")
# The abspath function takes a relative or absolute path as input and always returns the corresponding absolute path.
with open (file_path, "r") as file:
    intents=json.load(file)   
    #json.load is a function in Python's json module that is used to parse a JSON (JavaScript Object Notation) file and convert it into a Python object.

#crete the vectorizer and classifier
vectorizer= TfidfVectorizer(ngram_range=(1,4)) #Term Frequency-Inverse Document Frequency (TF-IDF) Vectorizer.
 #this is part of sklearn library. used in NLP to transform text data into numerical feature vectors, returns a sparse matrix where rows represent documents and columns represent n-grams, with values being the TF-IDF score

clf = LogisticRegression(random_state=0, max_iter=10000)
# creates an instance of the LogisticRegression class from the scikit-learn library in Python.
# It is a linear model, meaning it assumes a linear relationship between the input features and the log-odds of the output.
# It is essentially a "blueprint" or "empty shell" ready to be trained

# preprocess the data
tags=[]  # an empty list to store tags
patterns= [] #an empty list ot store patterns
for intent in intents:  #intent is a dict here.
    for pattern in intent['patterns']:  #intent['patterns'] is a list of patterns.
        tags.append(intent['tag'])
        patterns.append(pattern)

# training the model
x= vectorizer.fit_transform(patterns) 
y=tags 
clf.fit(x,y)
# Step 1: Convert the raw text data (patterns) into a numerical feature matrix (x) using the vectorizer.
# Step 2: Map the text data to corresponding labels (tags) as the target variable (y).
# Step 3: Train a classifier (clf) using the features (x) and labels (y)

def chatbot(input_text):
    input_text= vectorizer.transform([input_text]) # After transformation, input_text becomes a sparse matrix or a numerical array representing the text in the same feature space as the training data.
    tag= clf.predict(input_text)[0] #Output: clf.predict returns a list or an array of predicted labels. For instance, if the classifier is trained to classify input text into categories like ['greeting', 'farewell'], it might return something like ['greeting']
    for intent in intents:
        if intent['tag'] == tag:
            response= random.choice(intent['responses'])
            return str(response)

counter =0

def main():
    global counter
    st.title("PyBot")

    #Create a sidear menu with options
    menu=["Home","Chat History", "About"]
    choice= st.sidebar.selectbox("Menu", menu)
    # A dropdown menu appears in the sidebar labeled "Menu".
    # The user selects an option from the dropdown.
    # The selected option is saved in the choice variable, which can then be used elsewhere in the application

    #background image
    st.markdown(
        '''
        <style>
        .stApp {
            background-image: url("https://img.freepik.com/premium-photo/html5-editor-website-development-website-html-code-laptop-display-closeup-photo_372999-2161.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        ''',
        unsafe_allow_html=True
    
        # Risks of Using unsafe_allow_html:
        # Security Risks: If the HTML or CSS you include is malicious (e.g., injected through user input), it can lead to Cross-Site Scripting (XSS) vulnerabilities.
        # Maintenance: Custom styles may break when Streamlit updates its internal structure.
        # When to Use It:
        # When you need features that Streamlit doesn't natively support (e.g., background images, custom animations, or advanced layouts).
        # For internal or controlled environments where the risks of malicious input are minimal.
    )

    # home menu
    if choice=="Home":
        st.write("Welcome to The PyBot, you can ask any question releted python.")

        #check if the log file of chat exists if not then create it with column names
        if not os.path.exists('chat_history.csv'):
            with open('chat_history.csv', 'w', newline='', encoding='utf-8') as csvfile:
               csv_writer= csv.writer(csvfile) 
               #csv.writer: This is a method from Python's built-in csv module used to create a writer object for CSV files
               csv_writer.writerow(['User Input', 'chatbot response', 'timestamp'])
               # .writerow(): A method of the csv.writer object that writes a single row of data to the CSV file. The row is passed as a list or iterable
        
        counter += 1
        user_input= st.text_input("You: ",key=f"user_input_{counter}")
        # A text input field appears with the label "You:".
        # The user types something in the field.
        # The typed text is saved in user_input.
        # The key ensures the widget maintains state across app reruns. For example, if counter changes, a new input field is created

        if user_input :
            #convert the user input to a stirng
            user_input_str= str(user_input)

            response= chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=120, max_chars=None, key=f"chatbot_response_{counter}")

            # get the current timestap
            timestap= datetime.datetime.now().strftime(f"%y/%m/%d %H:%M:%S")

            #save the input and response to csv file
            with open('chat_history.csv','a', newline='', encoding='utf-8') as csvfile:
                csv_writer= csv.writer(csvfile)
                csv_writer.writerow([user_input_str,response, timestap])

            if response.lower() in ['goodbye','bye']:
                st.write("Feel free to ask your doubts, Happy Coding !")
                st.stop()
    elif choice=="Chat History":
        # display converstaion in acollapsible ecpander
        st.header("Chat History")

        with open('chat_history.csv','r', encoding='utf-8') as csvfile:
            csv_reader=csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                st.text(f"User: {row[0]}")
                st.text(f"Chatbot: {row[1]}")
                st.text(f"Timestap: {row[2]}")
                st.markdown("----")

    elif choice=="About":
        # st.header("About PyBot")
        st.write("""A Python-focused chatbot is being developed to help users with their programming questions. This chatbot is designed to provide quick, accurate, and clear answers, making it a valuable resource for anyone working with Python. Whether someone is a beginner learning the basics or an experienced developer tackling complex challenges, this tool aims to simplify problem-solving.\n \n The chatbot covers a wide range of Python-related topics, including syntax, libraries, debugging, and best practices. With natural language processing (NLP) integrated, it understands questions phrased in various ways. For example, asking “How do I create a list in Python?” or “What’s the syntax for defining a list?” will yield the same helpful response. The backend is powered by Python itself, ensuring efficiency and relevance. The chatbot is equipped with a knowledge base built from official documentation, tutorials, and community resources. Over time, it improves its performance using machine learning, enabling it to provide increasingly precise and useful answers.\n \n This chatbot isn’t just about answering questions; it’s also designed to support learning. By offering step-by-step explanations, code examples, and recommendations for further study, it serves as an educational companion. Its goal is to make Python approachable and engaging for all users. Once deployed, the chatbot will be accessible through platforms like websites and messaging apps, allowing users to get help anytime, anywhere. This project aims to bridge the gap between learning and real-time problem-solving, empowering Python enthusiasts to progress confidently in their coding journey.""")


if __name__ == '__main__':
    main()
