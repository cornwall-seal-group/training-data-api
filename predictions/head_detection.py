from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import azure_config

endpoint = azure_config.ENDPOINT
project_id = azure_config.PROJECT_ID
iteration_name = azure_config.ITERATION_NAME
prediction_key = azure_config.PREDICTION_KEY


def get_head_predictions(app, image_path):
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)

    # Open the image and get back the prediction results.
    with open(image_path, mode="rb") as test_data:
        results = predictor.detect_image(project_id, iteration_name, test_data)

    best_prediction = None

    # Find the best prediction
    for prediction in results.predictions:

        if best_prediction == None:
            best_prediction = prediction

        if best_prediction.probability < prediction.probability:
            best_prediction = prediction

    app.logger.info(results.predictions)
    app.logger.info(best_prediction)
    return {
        "predictions": results.predictions,
        "best_prediction": best_prediction
    }
