import ee
import pickle 
import folium
import matplotlib.pyplot as plt
from IPython.display import Image

ee.Initialize()

def mapping():
    """ Plotting model results
    """

    # Folium Utilities 
    # Define a method for displaying Earth Engine image tiles to folium map.
    def add_ee_layer(self, ee_image_object, vis_params, name):
        map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
        folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = "Map Data © Google Earth Engine",
            name = name,
            overlay = True,
            control = True
        ).add_to(self)

    # Add Earth Engine drawing method to folium.
    folium.Map.add_ee_layer = add_ee_layer

def train_sentinel_model():
    """ Train a multi-label classification model on Sentinel2 images. 
    """

    image = ee.Image('users/danielhirst1998/liveEO/rasterize_on_sentinel_2_labelled_17SLD')
    imageCollection = ee.ImageCollection('users/danielhirst1998/liveEO/s2-images')

    image = image.select('b1')
    image = image.set('class',{ 0: 'urban', 1: 'treerow', 2: 'forest', 3: 'single tree', 4: 'agriculture', 5: 'grassland',6: 'water', 4294967295: 'nodata'})
    image = image.updateMask(image.neq(4294967295))

    # create a palette/legend so we can easily see the labels on the map
    palette = [
    'FF0000', # urban // red
    '00FF00', # treerow // green
    '0000FF', # forest //blue
    'FFFF00', # single tree //yellow
    'FF00FF', # agriculture //magenta
    '00FFFF', # grassland // cyan
    'FFFFFF', # water //white
    ]

    model_input = imageCollection.toBands()

    #Change names of bands to be more understandable
    model_input = model_input.select(
    ['T17SLD_20190922T203454_AOT_10m_b1',
        'T17SLD_20190922T203454_B01_60m_b1',
        'T17SLD_20190922T203454_B02_10m_b1',
        'T17SLD_20190922T203454_B03_10m_b1',
        'T17SLD_20190922T203454_B04_10m_b1',
        'T17SLD_20190922T203454_B05_20m_b1',
        'T17SLD_20190922T203454_B06_20m_b1',
        'T17SLD_20190922T203454_B07_20m_b1',
        'T17SLD_20190922T203454_B08_10m_b1',
        'T17SLD_20190922T203454_B09_60m_b1',
        'T17SLD_20190922T203454_B11_20m_b1',
        'T17SLD_20190922T203454_B12_20m_b1',
        'T17SLD_20190922T203454_B8A_20m_b1',
        'T17SLD_20190922T203454_SCL_20m_b1',
        'T17SLD_20190922T203454_WVP_10m_b1'],
        ['AOT','B01','B02','B03','B04','B05','B06','B07','B08','B09','B11','B12','B8A','SCL','WVP'] 
    )

    #Combine the unlabelled images with the labels from the labelled image
    model_input = model_input.addBands(image.select(["b1"],["label"]))

    #//---------------------Supervised Classification--------------------------//

    # Use these bands for prediction.
    # All bands used to have most data possible, doing a combination of bands could help to increase accuracy in the future 
    bands =  ['AOT','B01','B02','B03','B04','B05','B06','B07','B08','B09','B11','B12','B8A','SCL','WVP','label'] 

    #//Set scale and numPoint parameters so we can quickly change them for both the training and validation model
    scale = 10 #// highest resolution of the s2 bands is 10m, so scale=10 preserves all data for all bands
    numPoints = 100000

    #Sample the input imagery using a stratified sample
    training = model_input.select(bands).stratifiedSample(
        classBand='label',
        scale=scale,
        numPoints=numPoints,
        seed=0,
        region=model_input.geometry())

    # Train classifier
    classifier = ee.Classifier.cart().train(
        features=training,
        classProperty='label',
        inputProperties=bands)

    # .pkl model results
    pickle.dump(classifier, open('models/s2-classifier.pkl','wb'))

    # TODO: Pickle modle_input as well?

def predict_land_type():
    """
    """
    
    #Classify the image with the same bands used for training.
    classified = model_input.select(bands).classify(classifier)

    # Get a confusion matrix representing resubstitution accuracy.
    trainAccuracy = classifier.confusionMatrix()

    print('Resubstitution error matrix: '+ str(trainAccuracy.getInfo()))
    print('Training Accuracy: ' + str(trainAccuracy.accuracy().getInfo()))

    # Sample the input with a different seed so we can compare the classifier and validate the model.
    validation = model_input.select(bands).stratifiedSample(
        classBand='label',
        scale=scale,
        numPoints=numPoints,
        seed=1,
        region=model_input.geometry())

    #Classify the validation data.
    validated = validation.classify(classifier)

    #// Get a confusion matrix representing expected accuracy.
    testAccuracy = validated.errorMatrix('label', 'classification')

    print('Validation error matrix: ', testAccuracy.getInfo())
    print('Validation overall accuracy: ', testAccuracy.accuracy().getInfo())