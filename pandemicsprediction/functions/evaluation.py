FOLDS_SEPARATOR = "_"
LINE_SEPARATOR = "\n"
VALUES_SEPARATOR = " "
TARGET_FILE_PATH = "C:\\Users\\Lorenzo\\Desktop\\DataMining\\"


def tag(keyword, val):
    return str(keyword) + ":" + str(val) + VALUES_SEPARATOR


class Meta:
    def __init__(self, name, sampling_rate, repetition, folds, features_dim, training_dim, validation_dim):
        self.identifier = name+"_"+str(repetition)
        self.recap = tag("Regressor", name)
        self.recap = self.recap + tag("SR", sampling_rate)
        self.recap = self.recap + tag("RepCount", repetition)
        self.recap = self.recap + tag("K", folds)
        self.recap = self.recap + tag("F_dim", features_dim)
        self.recap = self.recap + tag("T_dim", training_dim)
        self.recap = self.recap + tag("V_dim", validation_dim)


class Evaluation:
    def __init__(self, meta):
        self.labels = []
        self.folds = 0
        self.meta = meta

    def save_predictions(self, pred):
        self.labels.append(pred)
        self.folds += 1

    def conclude(self):
        result = self.meta.recap + LINE_SEPARATOR
        for iteration in range(self.folds):
            values = self.labels[iteration]
            for i in range(len(values)):
                if iteration > 0 and i == 0:
                    result = result + LINE_SEPARATOR
                output = str(values[i]) + VALUES_SEPARATOR
                result = result + output
            result = result + FOLDS_SEPARATOR
        return result


def export_on_txt(eval_list):
    for eval in eval_list:
        text_file = open(TARGET_FILE_PATH + eval.meta.identifier + ".csv", "w")
        text_file.write(eval.conclude())
        text_file.close()
