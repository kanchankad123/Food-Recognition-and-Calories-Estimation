import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array 
import numpy as np
from keras.models import load_model 
import cv2
import tempfile
import requests
from bs4 import BeautifulSoup

model = load_model('FV.h5')

labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}


fruits = ['apple', 'banana', 'bell pepper', 'chilli pepper', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'mango', 'orange',
          'paprika', 'pear', 'pineapple', 'pomegranate', 'watermelon']
vegetables = ['beetroot', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'corn', 'cucumber', 'eggplant', 'ginger',
              'lettuce', 'onion', 'peas', 'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato',
              'tomato', 'turnip']


def fetch_calories(prediction):
    try:
        url = f'https://www.google.com/search?&q=calories in {prediction}'
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Cannot fetch calories at the moment.")
        print(e)
        return None


def processed_img(img):
    img = cv2.resize(img, (224, 224))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    y_class = prediction.argmax(axis=-1)[0]
    result = labels[y_class]
    return result.capitalize()


def processed_img_file(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, [0])
    prediction = model.predict(img)
    y_class = prediction.argmax(axis=-1)
    result = labels[int(y_class)]
    return result.capitalize()


def run():
    st.set_page_config(page_title="Food Recognition & Calorie Estimation", layout="wide")
    

    st.sidebar.title("Select Mode")
    mode = st.sidebar.selectbox("Choose", ["Upload Image","Live Camera"])
    

    st.title("Food Recognition & Calorie Estimation")
    st.write("This app allows you to recognize different fruits and vegetables and estimate their calories.")
    
    st.markdown(
        """
        <style>
        .stApp {background-color: #000080;}
        </style>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    if mode == "Live Camera":
        st.header("Live Camera Input")
        st.write("Use your camera to capture an image of fruits or vegetables for recognition.")
        
        capture = st.camera_input("Capture an Image")
        
        if capture is not None:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(capture.read())
            temp_file.close()

            img = cv2.imread(temp_file.name)
            st.image(img, channels="BGR", caption="Captured Image", width=600)

            result = processed_img(img)


            if result.lower() in vegetables:
                st.info(f"**Category: Vegetable**")
            else:
                st.info(f"**Category: Fruit**")
            st.success(f"**Predicted: {result}**")


            cal = fetch_calories(result)
            if cal:
                st.warning(f"**Calories: {cal} (per 100 grams)**")

    elif mode == "Upload Image":
        st.header("Upload Image")
        st.write("Upload an image of fruits or vegetables for recognition.")
        
        img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
        
        if img_file is not None:
            img = Image.open(img_file).resize((250, 250))
            st.image(img, caption="Uploaded Image", use_column_width=False)

            save_image_path = tempfile.NamedTemporaryFile(delete=False).name + img_file.name
            with open(save_image_path, "wb") as f:
                f.write(img_file.getbuffer())

            result = processed_img_file(save_image_path)

            if result.lower() in vegetables:
                st.info(f"**Category: Vegetable**")
            else:
                st.info(f"**Category: Fruit**")
            st.success(f"**Predicted: {result}**")

            cal = fetch_calories(result)
            if cal:
                st.warning(f"**Calories: {cal} (per 100 grams)**")

run()
