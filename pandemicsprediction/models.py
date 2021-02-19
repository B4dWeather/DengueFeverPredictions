from django.db import models


def feature_names():
    return ["city",
            "year",
            "weekofyear",
            "week_start_date",
            "ndvi_ne",
            "ndvi_nw",
            "ndvi_se",
            "ndvi_sw",
            "precipitation_amt_mm",
            "reanalysis_air_temp_k",
            "reanalysis_avg_temp_k",
            "reanalysis_dew_point_temp_k",
            "reanalysis_max_air_temp_k",
            "reanalysis_min_air_temp_k",
            "reanalysis_precip_amt_kg_per_m2",
            "reanalysis_relative_humidity_percent",
            "reanalysis_sat_precip_amt_mm",
            "reanalysis_specific_humidity_g_per_kg",
            "reanalysis_tdtr_k",
            "station_avg_temp_c",
            "station_diur_temp_rng_c",
            "station_max_temp_c",
            "station_min_temp_c",
            "station_precip_mm"]


class WeatherRecord(models.Model):
    city = models.CharField(max_length=2)
    year = models.IntegerField()
    weekofyear = models.IntegerField()
    week_start_date = models.DateField()
    ndvi_ne = models.FloatField()
    ndvi_nw = models.FloatField()
    ndvi_se = models.FloatField()
    ndvi_sw = models.FloatField()
    precipitation_amt_mm = models.FloatField()
    reanalysis_air_temp_k = models.FloatField()
    reanalysis_avg_temp_k = models.FloatField()
    reanalysis_dew_point_temp_k = models.FloatField()
    reanalysis_max_air_temp_k = models.FloatField()
    reanalysis_min_air_temp_k = models.FloatField()
    reanalysis_precip_amt_kg_per_m2 = models.FloatField()
    reanalysis_relative_humidity_percent = models.FloatField()
    reanalysis_sat_precip_amt_mm = models.FloatField()
    reanalysis_specific_humidity_g_per_kg = models.FloatField()
    reanalysis_tdtr_k = models.FloatField()
    station_avg_temp_c = models.FloatField()
    station_diur_temp_rng_c = models.FloatField()
    station_max_temp_c = models.FloatField()
    station_min_temp_c = models.FloatField()
    station_precip_mm = models.FloatField()

    @property
    def city_code(self):
        if self.city == "iq":
            return 1
        if self.city == "sj":
            return 2
        return 0

    @property
    def week_start_date_integer(self):
        time = self.week_start_date
        m = time.month
        if m == 2:
            d = 28
        else:
            if m in [11, 4, 6, 9]:
                d = 30
            else:
                d = 31
        return 365 * time.year + time.day + d

    def as_Array(self, settings):
        me = []
        features = feature_names()
        index = 0
        for feature in settings:
            if feature == 'on':
                if index == 0:
                    me.append(self.city_code)
                else:
                    if index == 3:
                        me.append(self.week_start_date_integer)
                    else:
                        me.append(self.__getattribute__(features[index]))
            index += 1
        return me

    def __str__(self):
        return str(self.city) + "_" + str(self.week_start_date)


class ResultRecord(models.Model):
    city = models.CharField(max_length=2)
    year = models.IntegerField()
    weekofyear = models.IntegerField()
    total_cases = models.IntegerField()
    def as_array(self):
        return [self.city,self.year,self.weekofyear,self.total_cases]
    def __str__(self):
        return str(self.city) + ',' + str(self.year) + ',' + str(self.weekofyear) + ',' + str(self.total_cases)


class TrainingRecord(models.Model):
    city = models.CharField(max_length=2)
    year = models.IntegerField()
    weekofyear = models.IntegerField()
    total_cases = models.IntegerField()

    def __str__(self):
        return str(self.year) + "_" + str(self.weekofyear) + "_" + str(self.city)


class TrainingOptions(models.Model):
    settings = models.TextField(default="")
    model_name = models.TextField(default="")
    regressor = models.BinaryField(default=None)

    def __str__(self):
        c = len(self.settings.split(";"))
        return str(self.model_name) + " trained on " + str(c) + " features"
