from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index_from_url, name='index'),

    url(r'^upload_data/$', views.csv_uploader_data_from_url, name='csv_uploader_data'),
    url(r'^dataset_uploaded/$', views.dataset_upload_from_url, name='dataset_uploaded'),
    url(r'^upload_training_labels/$', views.csv_uploader_labels_from_url, name='csv_uploader_labels'),
    url(r'^labels_uploaded/$', views.training_label_upload_from_url, name='label_uploaded'),

    url(r'^training/$', views.training_page_from_url, name='training_page'),
    url(r'^training_start/$', views.training_start_from_url, name='training_start'),

    url(r'^trained_models/$', views.browse_trained_models_from_url, name='browse_trained_models'),

    url(r'^download/(?P<trainset_id>.*)/$', views.csv_download_from_url, name='download'),

    url(r'^trained_model_details/(?P<trainset_id>\w+)/$', views.trained_model_details_from_url,
        name='trained_model_details'),
    url(r'^delete/(?P<trainset_id>.*)/$', views.delete, name='delete'),
    url(r'^apply_model/(?P<trainset_id>.*)/$', views.apply_model, name='apply_model'),

]