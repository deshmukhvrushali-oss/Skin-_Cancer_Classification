import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load trained model
model = load_model("skin_cancer_model.h5")

# Class labels (dataset ke according order same hona chahiye)
class_names = ["bkl", "melanoma", "nevus"]

def predict_image(img_path):

    # Load image
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Prediction
    predictions = model.predict(img_array)[0]

    # Get highest probability index
    predicted_index = np.argmax(predictions)
    predicted_class = class_names[predicted_index]
    confidence = float(predictions[predicted_index])

    return predicted_class, confidence