import csv
import io
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from pandemicsprediction.functions.ml import start_training, start_prediction
from .functions.regression import REGRESSORS
from .models import WeatherRecord, ResultRecord, TrainingRecord, TrainingOptions, feature_names


def index_from_url(request):
    return render(request, "index.html")


def csv_uploader_data_from_url(request):
    template = "dataupload.html"
    return upload_page(request, template)


def csv_uploader_labels_from_url(request):
    template = "resultsupload.html"
    return upload_page(request, template)


def dataset_upload_from_url(request):
    template = "index.html"
    prompt = {'order': 'First row of the .CSV should be column names'}
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == "POST":
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Uploaded file is not .csv as expected')

        csv_decode_weather(csv_file)

        content = "uploading a test dataset"
        result = "Dataset csv Uploaded"
        context = {"page": content, "result": result}
        return render(request, template, context)


def training_label_upload_from_url(request):
    template = "index.html"
    prompt = {'order': 'First row of the .CSV should be column names'}
    if request.method == "GET":
        return render(request, template, prompt)
    if request.method == "POST":
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Uploaded file is not .csv as expected')

        print("csv reading Started")
        dzero = Decimal(0)

        TrainingRecord.objects.all().delete()

        data_set = csv_file.read().decode("UTF-8")
        io_string = io.StringIO(data_set)
        next(io_string)

        for column in csv.reader(io_string, delimiter=",", quotechar="|"):
            _, created = TrainingRecord.objects.update_or_create(
                city=column[0],
                year=column[1],
                weekofyear=column[2],
                total_cases=column[3] if column[3] else dzero
            )

        print("csv reading complete")

        content = "uploading a training dataset"
        result = "Training Labels Uploaded"
        context = {"page": content, "result": result}
        return render(request, template, context)


def upload_page(request, template):
    content = "uploader"
    context = {"page": content}
    return render(request, template, context)


def training_page_from_url(request):
    return open_training_page(request, -1)


def open_training_page(request, set_id):
    content = "training_settings"
    features = feature_names()
    context = {"page": content, "features": features, "regressor_names" : REGRESSORS}
    return render(request, "training.html", context)


def csv_decode_weather(csv_file):
    WeatherRecord.objects.all().delete()
    print("csv reading started")
    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    dzero = Decimal(0)
    dmissing = Decimal(-1)
    for line in csv.reader(io_string, delimiter=",", quotechar="|"):
        if len(line) < 24:
            continue
        _, created = WeatherRecord.objects.update_or_create(
            city=line[0],
            year=line[1],
            weekofyear=line[2],
            week_start_date=line[3],
            ndvi_ne=line[4] if line[4] else dmissing,
            ndvi_nw=line[5] if line[5] else dmissing,
            ndvi_se=line[6] if line[6] else dmissing,
            ndvi_sw=line[7] if line[7] else dmissing,
            precipitation_amt_mm=line[8] if line[8] else dzero,
            reanalysis_air_temp_k=line[9] if line[9] else dzero,
            reanalysis_avg_temp_k=line[10] if line[10] else dzero,
            reanalysis_dew_point_temp_k=line[11] if line[11] else dzero,
            reanalysis_max_air_temp_k=line[12] if line[12] else dzero,
            reanalysis_min_air_temp_k=line[13] if line[13] else dzero,
            reanalysis_precip_amt_kg_per_m2=line[14] if line[14] else dzero,
            reanalysis_relative_humidity_percent=line[15] if line[15] else dzero,
            reanalysis_sat_precip_amt_mm=line[16] if line[16] else dzero,
            reanalysis_specific_humidity_g_per_kg=line[17] if line[17] else dzero,
            reanalysis_tdtr_k=line[18] if line[18] else dzero,
            station_avg_temp_c=line[19] if line[19] else dzero,
            station_diur_temp_rng_c=line[20] if line[20] else dzero,
            station_max_temp_c=line[21] if line[21] else dzero,
            station_min_temp_c=line[22] if line[22] else dzero,
            station_precip_mm=line[23] if line[23] else dzero
        )
    print("csv reading complete")


def csv_download_from_url(request, trainset_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'
    writer = csv.writer(response)
    writer.writerow(['city', 'year', 'weekofyear', 'total_cases'])
    data = ResultRecord.objects.all()
    for r in data:
        writer.writerow(r.as_array())
    return response


def training_start_from_url(request):
    global feature_names
    set = -1
    if request.method == 'POST':
        features = feature_names()
        settings = []
        selected_features = []
        features_ids = []
        for feature in request.POST.keys():
            if feature.startswith("csrf"):
                continue
            trimmed_feature = feature.split("\t")[0]
            if (any(trimmed_feature in feature_names for feature_names in features)):
                selected_features.append(trimmed_feature)
                features_ids.append(feature)
        for feature in features:
            id = feature
            try:
                id_index = selected_features.index(feature)
                id = features_ids[id_index]
            except:
                id = feature
            finally:
                flag = request.POST.get(id)
                if flag is None:
                    flag = 'off'
                settings.append(flag)

        method = request.POST["regchoice"]
        set = start_training(settings, method)

    return open_training_page(request, set)


def browse_trained_models_from_url(request):
    content = "browse_models"
    context = {"page": content, "training_sets": TrainingOptions.objects.all()}
    return render(request, "browse.html", context)


def trained_model_details_from_url(request, trainset_id):
    return show_model_details(request, trainset_id, "No work")


def apply_model(request, trainset_id):
    res = start_prediction(trainset_id)
    return show_model_details(request, trainset_id, res)


def show_model_details(request, trainset_id, status):
    set = TrainingOptions.objects.filter(id=trainset_id).get()
    features = set.settings
    context = {"page": "details", "set": set, "features": features, "status": status}
    return render(request, "details.html", context)


def delete(request, trainset_id):
    item = TrainingOptions.objects.filter(id=trainset_id).get()
    item.delete()
    return browse_trained_models_from_url(request)
