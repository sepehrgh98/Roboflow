import random
import cv2
import numpy as np
import xml.etree.ElementTree as gfg 
import os
import pathlib

class RoboflowLogic:
    def __init__(self, projectName, detectionObject):
        self.projectName = projectName
        self.detectionObject = detectionObject
        self.Data = []
        self.p = []
        self.cashData_folder=[]
        self.cashData_files=[]
        self.test = []
        self.training = []
        self.validation = []
        self.test = []
        self.Output = []
        odir = "Outputs"
        self.output_path  = os.path.join(os.getcwd(), odir)
        if not pathlib.Path(self.output_path).exists():
            os.mkdir(self.output_path )



    # degre should be in ["ROTATE_90_CLOCKWISE", "ROTATE_180", "ROTATE_90_COUNTERCLOCKWISE"]
    def rotate(self , degre , obj):
        rotate_type = getattr(cv2, degre)
        rotated=cv2.rotate(obj.read(), rotate_type)
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), rotated)
        img=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img
        
    

    def resize(self, obj, scale_percent):
        img = cv2.imread(obj.path, cv2.IMREAD_UNCHANGED)
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), resized)
        imgobj=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  imgobj

        

    
    def filterGray(self, obj):
        grayed=cv2.cvtColor(obj.read(), cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), grayed)
        img=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img 

        


    def changeBrightness(self,obj, value=30):
        output = []
        hsv = cv2.cvtColor(obj.read(), cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v,value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        output.append(img)
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), output[0])
        img = myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img



    def filterBlur(self, obj):
        blured=cv2.GaussianBlur(obj.read(), (9, 9), 0) 
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), blured)
        img=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img


    def hueFilter(self, obj):
        hued=cv2.cvtColor(obj.read(), cv2.COLOR_BGR2HSV) 
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), hued)
        img=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img


    def noisyFilter(self,obj , mean=0, var=0.01):
        noised=self.__random_noise(obj.read(), mean=mean, var=var)
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), noised*255)
        img=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img



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


    def crop(self,obj,x, y, width, height):
        mainimg_height, mainimg_width, _ = obj.read().shape
        croped=self.__crop(obj.read(), int(x*mainimg_width), int(y*mainimg_height), int(height*mainimg_width), int(width*mainimg_height)) 
        cv2.imwrite(os.path.join(self.output_path , obj.name+".jpg"), croped)
        img=myImage(os.path.join(self.output_path , obj.name+".jpg"))
        return  img
            


    def __crop(self, img, x, y, width, height):
        crop_img = img[y:y+width, x:x+height]
        return crop_img            

    def Test_Train_data(self, training_pr, validation_pr, test_pr, data):

        training_number = round(training_pr * len(data))
        validation_number = round(validation_pr * len(data))
        test_number = round(test_pr * len(data))
        if round(test_pr * len(data)) == 0 :
            test_number +=1
            validation_number -=1

        copy_Data = data.copy()
        for _ in range(training_number):
            self.training.append(random.choice(copy_Data))
            copy_Data.remove(self.training[-1])


        for _ in range(validation_number):
            self.validation.append(random.choice(copy_Data))
            copy_Data.remove(self.validation[-1])

        self.test = copy_Data

    def make_final_files(self, dir):
        odir_test = "Test"
        out_test  = os.path.join(dir, odir_test)
        if not pathlib.Path(out_test).exists():
            os.mkdir(out_test)
        
        odir_train = "Train"
        out_train  = os.path.join(dir, odir_train)
        if not pathlib.Path(out_train).exists():
            os.mkdir(out_train)
        
        odir_validation = "Validation"
        out_validation  = os.path.join(dir, odir_validation)
        if not pathlib.Path(out_validation).exists():
            os.mkdir(out_validation)

        for item in self.test:
            t = item.read()
            cv2.imwrite(os.path.join(out_test , item.name+".jpg"), t)
            if item.detection_obj != None:
                item.XML_Generator(out_test)

        for item in self.training:
            t = item.read()
            cv2.imwrite(os.path.join(out_train , item.name+".jpg"), t)
            if item.detection_obj != None:
                item.XML_Generator(out_train)

        for item in self.validation:
            t = item.read()
            cv2.imwrite(os.path.join(out_validation , item.name+".jpg"), t)
            if item.detection_obj != None:
                item.XML_Generator(out_validation)
            


class myImage:
    def __init__(self, path):
        self.detection_obj = []
        self.path = path
        img = cv2.imread(self.path)
        self.height, self.width, c = img.shape
        self.name = ".".join(str(os.path.basename(os.path.normpath(self.path))).split(".")[:-1])

    def read(self):
        img = cv2.imread(self.path)
        return img


    def add_detection_obj(self, detObj):
        self.detection_obj.append(detObj)


    def XML_Generator(self,dir):
        root = gfg.Element("annotation")
        filename = gfg.SubElement(root,"filename")
        filename.text  = self.name
        path = gfg.SubElement(root,"path")
        path.text  = self.path
        size = gfg.SubElement(root, "size")
        width = gfg.SubElement(size,"width")
        height = gfg.SubElement(size, "height")
        width.text  = str(self.width)
        height.text  = str(self.height)
        for item in self.detection_obj:
            ob = gfg.SubElement(root, "object")
            name = gfg.SubElement(ob, "name")
            name.text = item.label
            ownPosition = gfg.SubElement(ob, "Position")
            x = gfg.SubElement(ownPosition, "x")
            y = gfg.SubElement(ownPosition, "y")
            x.text = str(item.position[0])
            y.text = str(item.position[1])
            BoxPosition = gfg.SubElement(ob, "BoxPosition")
            xmin = gfg.SubElement(BoxPosition, "xmin")
            ymin = gfg.SubElement(BoxPosition, "ymin")
            xmax = gfg.SubElement(BoxPosition, "xmax")
            ymax = gfg.SubElement(BoxPosition, "ymax")
            xmin.text = str(item.Box_start.x())
            ymin.text = str(item.Box_start.y())
            xmax.text = str(item.Box_end.x())
            ymax.text = str(item.Box_end.y())
  

        tree = gfg.ElementTree(root)

        with open (os.path.join(dir,rf'{self.name}.xml'), "wb") as files :
            tree.write(files)


    

class DetectionObject:

    def __init__(self, position, label, Box_start, Box_end):
        self.label = label
        self.position = position
        self.Box_start = Box_start
        self.Box_end = Box_end



    def __repr__(self):
        return f"{self.label} => {self.position}"

    def __str__(self):
        return f"{self.label} => {self.position}"



