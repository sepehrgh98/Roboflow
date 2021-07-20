import random
import cv2
import numpy as np

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



    # degre should be in ["ROTATE_90_CLOCKWISE", "ROTATE_180", "ROTATE_90_COUNTERCLOCKWISE"]
    def rotate(self, degre):
        rotate_type = getattr(cv2, degre)
        output = [
            cv2.rotate(cv2.imread(file_path), rotate_type) 
            for file_path in self.Data
        ]
        cv2.imshow("test", output[0])

        return output
    
    def resize(self, scale_percent):
        output = []
        for path in self.Data:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            output.append(resized)

        cv2.imshow("test", output[0])

        return output

    
    def filterGray(self):
        output = [
            cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2GRAY) 
            for file_path in self.Data
        ]
        return output


    def changeBrightness(self, value=30):
        output = []

        for file_path in self.Data:
            img = cv2.imread(file_path)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.add(v,value)
            v[v > 255] = 255
            v[v < 0] = 0
            final_hsv = cv2.merge((h, s, v))
            img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            output.append(img)

        cv2.imshow("test", output[0])


    def filterBlur(self):
        output = [
            cv2.GaussianBlur(cv2.imread(file_path), (5, 5), 0) 
            for file_path in self.Data
        ]
        return output


    def hueFilter(self):
        output = [
            cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2HSV) 
            for file_path in self.Data
        ]
        cv2.imshow("test", output[0])
        return output


    def noisyFilter(self, mean=0, var=0.01):
        output = [
            self.__random_noise(cv2.imread(file_path), mean=mean, var=var) 
            for file_path in self.Data
        ]
        return output



    def __mat2gray(self, img):
        A = np.double(img)
        out = np.zeros(A.shape, np.double)
        cv2.normalize(A, out, 1.0, 0.0, cv2.NORM_MINMAX)
        return out

    
    #Add noise to the image
    def __random_noise(self, image, mode='gaussian', seed=None, clip=True, **kwargs):
        image = self.__mat2gray(image)
        mode = mode.lower()
        if image.min() < 0:
            low_clip = -1
        else:
            low_clip = 0
        if seed is not None:
            np.random.seed(seed=seed)
        if mode == 'gaussian':
            noise = np.random.normal(kwargs['mean'], kwargs['var'] ** 0.5,
                                    image.shape)        
            out = image  + noise
        if clip:        
            out = np.clip(out, low_clip, 1.0)
        return out


    def crop(self, x, y, height, width):
        output = [
            self.__crop(cv2.imread(file_path), x, y, height, width) 
            for file_path in self.Data
        ]
        cv2.imshow("test", output[0])
        return output


    def __crop(self, img, x, y, height, width):
        crop_img = img[y:y+height, x:x+width]
        return crop_img            

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

            copy_Data.remove(self.validation[-1])
            self.validation.append(random.choice(copy_Data))
        for _ in range(validation_number):

        self.test = copy_Data
class myImage:
        self.path = path

    def __init__(self, path):
        self.detection_obj = []

        img = cv2.imread(self.path)
    def add_detection_obj(self, detObj):
        self.detection_obj.append(detObj)

class DetectionObject:

    def __init__(self, position, label):
        self.label = label

        self.position = position
    def __repr__(self):
        return f"{self.label} => {self.position}"
    def __str__(self):
        return f"{self.label} => {self.position}"

