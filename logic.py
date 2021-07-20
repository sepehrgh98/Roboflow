import random
import cv2

class RoboflowLogic:
    def __init__(self, projectName, detectionObject):
        self.projectName = projectName
        self.detectionObject = detectionObject
        self.Data = []
        self.cash_Data=[]
        # self.Data = [4,9,5,8,5,8,5,8,5,6,9,1,2,8,5,6,9,8,7,4,1,5,9,8,7,4,5,2,3,21,6,5,4,9,8,5,1,9]
        self.training = []
        self.validation = []
        self.test = []

    def Test_Train_data(self, training_pr, validation_pr, test_pr):
        training_number = round(training_pr * len(self.Data))
        validation_number = round(validation_pr * len(self.Data))
        test_number = round(test_pr * len(self.Data))
        if round(test_pr * len(self.Data)) == 0 :
            test_number +=1
            validation_number -=1

        copy_Data = self.Data.copy()
        for _ in range(training_number):
            self.training.append(random.choice(copy_Data))
            copy_Data.remove(self.training[-1])

        for _ in range(validation_number):
            self.validation.append(random.choice(copy_Data))
            copy_Data.remove(self.validation[-1])

        self.test = copy_Data

class myImage:
    def __init__(self, path):
        self.path = path
        self.detection_obj = []
        img = cv2.imread(self.path)

    def add_detection_obj(self, detObj):
        self.detection_obj.append(detObj)


class DetectionObject:
    def __init__(self, position, label):
        self.position = position
        self.label = label

    def __str__(self):
        return f"{self.label} => {self.position}"

    def __repr__(self):
        return f"{self.label} => {self.position}"


