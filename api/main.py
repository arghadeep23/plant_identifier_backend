from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from keras import layers
import os
from fastapi import FastAPI
from Uses1 import uses
app = FastAPI()

# Get the parent directory of the current working directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir = os.path.dirname(parent_dir)

# Define the path to the model directory
model_path = os.path.join(parent_parent_dir, "saved_models", "1")

MODEL = keras.models.load_model(model_path)
CLASS_NAMES = ['Alpinia Galanga (Rasna)', 'Amaranthus Viridis (Arive-Dantu)',
               'Artocarpus Heterophyllus (Jackfruit)', 'Azadirachta Indica (Neem)',
               'Basella Alba (Basale)', 'Brassica Juncea (Indian Mustard)',
               'Carissa Carandas (Karanda)', 'Citrus Limon (Lemon)',
               'Ficus Auriculata (Roxburgh fig)', 'Ficus Religiosa (Peepal Tree)',
               'Hibiscus Rosa-sinensis', 'Jasminum (Jasmine)',
               'Mangifera Indica (Mango)', 'Mentha (Mint)',
               'Moringa Oleifera (Drumstick)', 'Muntingia Calabura (Jamaica Cherry-Gasagase)',
               'Murraya Koenigii (Curry)', 'Nerium Oleander (Oleander)',
               'Nyctanthes Arbor-tristis (Parijata)', 'Ocimum Tenuiflorum (Tulsi)',
               'Piper Betle (Betel)', 'Plectranthus Amboinicus (Mexican Mint)',
               'Pongamia Pinnata (Indian Beech)', 'Psidium Guajava (Guava)',
               'Punica Granatum (Pomegranate)', 'Santalum Album (Sandalwood)',
               'Syzygium Cumini (Jamun)', 'Syzygium Jambos (Rose Apple)',
               'Tabernaemontana Divaricata (Crape Jasmine)', 'Trigonella Foenum-graecum (Fenugreek)',
               'arjun_diseased', 'arjun_healthy',
               'bael_diseased', 'basil_healthy',
               'chinar_diseased', 'chinar_healthy',
               'guava_diseased', 'guava_healthy',
               'jamun_diseased', 'jamun_healthy',
               'jatropha_diseased', 'jatropha_healthy',
               'lemon_diseased', 'lemon_healthy',
               'mango_diseased', 'mango_healthy',
               'pomegranate_diseased', 'pomegranate_healthy',
               'pongamia_pinnata_diseased', 'pongamia_pinnata_healthy']


@app.get("/ping")
async def ping():
    return "Hello, I am alive"


def read_file_as_image(data) -> np.ndarray:
    # image = BytesIO(data.resize(256, 256))
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
#                        data type     default value
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'uses': uses[predicted_class]
    }


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
