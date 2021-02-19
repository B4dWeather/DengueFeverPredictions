import numpy as np

from pandemicsprediction.functions.regression import initialize, fit, predict
from pandemicsprediction.functions.util import decode_city, table_to_matrix, serialize, deserialize
from pandemicsprediction.models import feature_names, WeatherRecord, TrainingOptions, TrainingRecord, ResultRecord

NO_LABELS_LOADED = 1
NO_FEATURES_LOADED = 2
NO_FEATURES_TO_PROCESS = 3
NO_LABELS_FOUND = 4
NO_MODEL_FOUND = 5

CITY_FEATURE_INDEX = 0
YEAR_FEATURE_INDEX = 1
WEEKOFYEAR_FEATURE_INDEX = 2


def abort(error_code):
    if error_code == NO_LABELS_LOADED:
        print("No labels have been loaded to start training")
    if error_code == NO_FEATURES_LOADED:
        print("No features have been loaded to start training")
    if error_code == NO_FEATURES_TO_PROCESS:
        print("No features to analyze")
    if error_code == NO_MODEL_FOUND:
        print("No model to process")
    else:
        print("Error somewhere")


def get_labels(data_set):
    labels = []
    for line in data_set:
        c = decode_city(int(line[0]))
        y = str(int(line[1]))
        w = str(int(line[2]))

        record = TrainingRecord.objects.filter(city=c, year=y, weekofyear=w)
        if record.exists():
            n = record.first().total_cases
            labels.append(n)
        else:
            labels.append("-1")
            print("MISSING LABEL: ")
            print(line)
    return labels


def save_prediction_model(model_name, blackbox, settings):
    wrapped = serialize(blackbox)
    featuresettings = ";".join(settings)
    item = TrainingOptions.objects.create(model_name=model_name, regressor=wrapped, settings=featuresettings)
    item.save()
    return item.id


def start_training(settings, method):
    print("training started")

    if TrainingRecord.objects.count() <= 0:
        abort(NO_LABELS_LOADED)
        return

    if WeatherRecord.objects.count() <= 0:
        abort(NO_FEATURES_LOADED)
        return

    features_dimension = settings.count('on')  # number of columns
    tuples_dimension = WeatherRecord.objects.count()  # number of rows

    # convert spreadsheet into matrix
    data_matrix = table_to_matrix(WeatherRecord.objects.all(), tuples_dimension, features_dimension, settings)

    np.random.shuffle(data_matrix)

    # get labels from the other table
    training_labels = get_labels(data_matrix)

    regressor = initialize(method)

    trained_model = fit(regressor, data_matrix, training_labels, tuples_dimension, features_dimension)

    print("training finished")

    return save_prediction_model(method, trained_model, settings)


def read_settings(raw_settings: str = ""):
    return raw_settings.split(";")


def start_prediction(trained_model_id):
    print("processing started")

    if WeatherRecord.objects.count() <= 0:
        abort(NO_FEATURES_LOADED)
        return

    model = None
    try:
        model = TrainingOptions.objects.get(id=trained_model_id)
    except TrainingOptions.DoesNotExist:
        abort(NO_MODEL_FOUND)
        return "Error: model saved incorrectly"

    ResultRecord.objects.all().delete()

    settings = read_settings(model.settings)

    tuples_dimension = WeatherRecord.objects.count()
    features_dimension = settings.count('on')

    # convert spreadsheet into matrix
    data_matrix = table_to_matrix(WeatherRecord.objects.all(), tuples_dimension, features_dimension, settings)

    regressor = deserialize(model.regressor)

    predictions = predict(regressor, data_matrix, tuples_dimension, features_dimension)

    print("prediction finished")

    export_result(zip(data_matrix, predictions))
    return "Results saved"


def export_result(dataset):
    output = []
    for features, label in dataset:
        c = decode_city(int(features[0]))
        y = str(int(features[1]))
        w = str(int(features[2]))
        r = ResultRecord(city=c, year=y, weekofyear=w, total_cases=label)
        output.append(r)
    ResultRecord.objects.bulk_create(output)
