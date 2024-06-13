import cv2
import numpy as np

def loadImage(filePath):
    return cv2.imread(filePath)

def convertColor(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def resizeImage(image, width, height):
    widthScale = width / image.shape[1]
    heightScale = height / image.shape[0]
    scale = widthScale if widthScale != 1 else heightScale

    dimension = (int(image.shape[1] * scale), int(image.shape[0] * scale))

    return cv2.resize(image, dimension)

def rotateImage(image, angle):
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE if angle == -90 else cv2.ROTATE_90_COUNTERCLOCKWISE)

def flipImage(image, direction):
    return cv2.flip(image, 1) if direction == 'horizontal' else cv2.flip(image, 0)

def adjustBrightness(image, val):
    image = np.int16(image)
    image += val*2
    image = np.clip(image, 0, 255)
    return np.uint8(image)

def adjustContrast(image, val):
    image = np.int16(image)
    image = image * (val / 127 + 1) - val
    image = np.clip(image, 0, 255)
    return np.uint8(image)

def adjustSaturation(image, val):
    if len(image.shape) < 3:
        return image
    
    saturationScale = (val + 100) / 100

    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    image = np.float32(image)

    image[:, :, 1] *= saturationScale
    image[:, :, 1] = np.clip(image[:, :, 1], 0, 255)

    image = np.uint8(image)

    return cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

def applyBlur(image):
    return cv2.blur(image, (15, 15))

def applyNoiseGause(image):
    noise_gauss = np.random.normal(0,1,image.size)
    noise_gauss = noise_gauss.reshape(image.shape[0],image.shape[1],image.shape[2]).astype('uint8')
    image = image + image * noise_gauss

    return image

def saveImage(filePath, image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filePath, image)