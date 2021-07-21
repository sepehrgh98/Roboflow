import cv2
import numpy as np


class RoboflowLogic:
    def __init__(self, projectName, AnnotationGroup):
        self.projectName = projectName
        self.AnnotationGroup = AnnotationGroup
        self.Data = []



    # degre should be in ["ROTATE_90_CLOCKWISE", "ROTATE_180", "ROTATE_90_COUNTERCLOCKWISE"]
    def rotate(self, data, degre):
        rotate_type = getattr(cv2, degre)
        output = [
            cv2.rotate(cv2.imread(file_path), rotate_type) 
            for file_path in data
        ]
        cv2.imshow("test", output[0])

        return output
    
    def resize(self, data, scale_percent):
        output = []
        for path in data:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            output.append(resized)

        cv2.imshow("test", output[0])

        return output

    
    def filterGray(self, data):
        output = [
            cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2GRAY) 
            for file_path in data
        ]
        return output


    def changeBrightness(self, data, value=30):
        output = []

        for file_path in data:
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


    def filterBlur(self, data):
        output = [
            cv2.GaussianBlur(cv2.imread(file_path), (5, 5), 0) 
            for file_path in data
        ]
        return output


    def hueFilter(self, data):
        output = [
            cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2HSV) 
            for file_path in data
        ]
        cv2.imshow("test", output[0])
        return output


    def noisyFilter(self, data, mean=0, var=0.01):
        output = [
            self.__random_noise(cv2.imread(file_path), mean=mean, var=var) 
            for file_path in data
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


    def crop(self, data, x, y, height, width):
        output = [
            self.__crop(cv2.imread(file_path), x, y, height, width) 
            for file_path in data
        ]
        cv2.imshow("test", output[0])
        return output


    def __crop(self, img, x, y, height, width):
        crop_img = img[y:y+height, x:x+width]
        return crop_img            


    # def shear(self, data):
    #     output = []
    #     for file_path in data:
    #         angle = 45 #Angle in degrees.
    #         shear = 1
    #         translation = 5

    #         type_border = cv2.BORDER_CONSTANT
    #         color_border = (255,255,255)

    #         original_image = cv2.imread(file_path)
    #         rows,cols,ch = original_image.shape;


    #         #First: Necessary space for the rotation
    #         M = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
    #         cos_part = np.abs(M[0, 0]); sin_part = np.abs(M[0, 1])
    #         new_cols = int((rows * sin_part) + (cols * cos_part)) 
    #         new_rows = int((rows * cos_part) + (cols * sin_part))

    #         #Second: Necessary space for the shear
    #         new_cols += (shear*new_cols)
    #         new_rows += (shear*new_rows)

    #         #Calculate the space to add with border
    #         up_down = int((new_rows-rows)/2); left_right = int((new_cols-cols)/2)

    #         final_image = cv2.copyMakeBorder(original_image, up_down, up_down,left_right,left_right,type_border, value = color_border)
    #         rows,cols,ch = final_image.shape

    #         #Application of the affine transform.
    #         M_rot = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    #         translat_center_x = -(shear*cols)/2
    #         translat_center_y = -(shear*rows)/2

    #         M = M_rot + np.float64([[0,shear,translation + translat_center_x], [shear,0,translation + translat_center_y]])
    #         final_image  = cv2.warpAffine(final_image , M, (cols,rows),borderMode = type_border, borderValue = color_border)
    #         output.append(final_image)

    #     cv2.imshow("test", output[0])
    #     return output

        




if __name__ == "__main__":
    rf = RoboflowLogic("tewst", "test")
    data = []
    data.append("test.jpeg")
    # rf.rotate(data, "ROTATE_180")
    # rf.resize(data, 60)
    # rf.filterGray(data)
    # rf.increaseBrightness(data, value=-100)
    # rf.filterBlur(data)
    # rf.hueFilter(data)
    # rf.noisyFilter(data)
    # rf.crop(data, 10, 10, 200, 200)



    # cv2.imshow("test", output[0])
    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
