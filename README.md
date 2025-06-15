# Food-Recognition-and-Calories-Estimation
0.	Title :- 
	Project Title: Food Recognization and Calories Estimation
	Student Name: Kanchan Kad, Vishakha More
	Guide Name: Dr.Abuzar sir Department of Data Science
	Department: Data Science
	Institution: SIES College of Arts, Science, and Commerce
	Academic Year: 2024-25
	Date of Submission: 21/10/2024
1.	Acknowledgments:- 
I would like to express my sincere gratitude to my project supervisor, Dr. Abuzar Ansari, for their invaluable support and guidance throughout this project. I also appreciate my peers for their constructive feedback and encouragement.
2.	Abstract:- 
The growing focus on health and nutrition has increased the demand for effective methods to recognize fruits and vegetables and estimate their calorie content. This paper introduces an innovative application that uses deep learning and image processing to identify different fruits and vegetables and predict their calorie values. It integrates a pre-trained convolutional neural network (CNN) model with web scraping to retrieve calorie information, offering users real-time nutritional insights. The system supports both live camera input and image uploads, making it versatile for dietary management and health monitoring.
3.	Acronyms and Abbreviations:- 
st – Streamlit (a Python library for building web apps)
PIL – Python Imaging Library (part of the Pillow package used for image processing)
Keras – (not an acronym but a deep learning library in Python)
cv2 – OpenCV (Open Source Computer Vision Library)
np – NumPy (a package for numerical computations in Python)
h5 – HDF5 (Hierarchical Data Format version 5, a file format to store large datasets)
________________________________________

Chapter 1: Introduction
As awareness of healthy eating grows, there's a rising need for tools that provide real-time nutritional analysis. While many apps offer manual calorie tracking, automating food recognition and calorie estimation through image processing is less explored. This research develops an automated system that uses deep learning to identify fruits and vegetables and estimate their calorie content. A pre-trained CNN classifies various produce, integrated with web scraping for real-time calorie data retrieval. The application supports two modes: live camera input for scanning food directly and image uploads for analyzing existing photos. This dual functionality enhances user experience and adaptability across environments.

Chapter 2: Literature Review
•  Bossard et al. (2014): Introduced the Food-101 dataset, advancing food image classification benchmarks.
•  Meyers et al. (2015): Developed deep learning methods for estimating food portion sizes and recognition, aiding calorie estimation.
•  Ege et al. (2019): Explored regression models with CNNs to predict nutritional content, informing calorie estimation.

Chapter 3: Research Methodology
Research Design:
This study employs a design-oriented methodology for developing, implementing, and evaluating a CNN-based food recognition and calorie estimation system via a web application. The approach includes:
•	Model Development: Designing and training a CNN to classify fruit and vegetable images.
•	Web Application Development: Creating a user interface using Streamlit for data-driven applications.
•	System Integration: Merging image classification and web scraping for calorie estimation into a platform that accepts both uploaded images and live camera input. This iterative process refines accuracy and functionality through testing and user feedback.

Data Collection Methods:
The project utilizes the “Fruit and Vegetable Image Recognition” dataset, consisting of 36 classes with approximately 100 images per class, totaling over 3600 training images. Each category includes 10 images for training and validation.
Caloric Data Collection:
The calorie estimation feature uses web scraping to gather caloric content for identified fruits and vegetables, involving:
•	Data Source: Google Search results.
•	Search Query: Queries such as "calories in [food item]" are formulated to extract data.
•	Extraction Method: HTML parsing with BeautifulSoup is used to identify and extract caloric values (per 100 grams) from the search results.
Ethical Considerations:
The study ensures all data sources for training and calorie estimation are publicly available. Users are informed that calorie values are estimates and may vary.


Chapter 4: Discussion
The effectiveness of the CNN model demonstrates the potential of AI-based tools in automating dietary monitoring. The integration of web scraping for calorie estimation, while innovative, requires careful handling to ensure data accuracy. The findings suggest that such tools can be valuable for dietitians, fitness enthusiasts, and the general public, offering a convenient way to track dietary intake. Future improvements could include portion size estimation and a broader range of food categories.
Chapter 6: Conclusion 
The study successfully developed an AI-based web application capable of recognizing fruits and vegetables and estimating their calorie content. The tool demonstrated good accuracy and user satisfaction. The results highlight the potential of using AI and web scraping to simplify dietary tracking. However, accuracy in calorie estimation remains dependent on the quality of online sources
________________________________________
References
Dataset:“https://www.kaggle.com/datasets/kriti kseth/fruit-and-vegetable-image-recognition”
