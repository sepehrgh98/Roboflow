import cv2
import numpy as np


class RoboflowLogic:
    def __init__(self, projectName, AnnotationGroup):
        self.projectName = projectName
        self.AnnotationGroup = AnnotationGroup
        self.Data = []



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







if __name__ == "__main__":
    rf = RoboflowLogic("tewst", "test")
    rf.Data.append("test.jpeg")
    # rf.rotate("ROTATE_180")
    # rf.resize(60)
    # rf.filterGray()
    # rf.increaseBrightness(value=-100)
    # rf.filterBlur()
    # rf.hueFilter()
    # rf.noisyFilter()
    # rf.crop(10, 10, 200, 200)


    # cv2.imshow("test", output[0])
    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
