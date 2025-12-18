from lmdeploy import pipeline
from lmdeploy.vl import load_image

pipe = pipeline('/scratch/gilbreth/park1361/models')

#image = "./images/out1.png"
#response = pipe(('describe this image', image))

image_names = [ "out1.png", "out2.png", "out3.png", "out4.png", "out5.png", "out6.png", "out7.png" ]
images = [load_image("./images/" + name) for name in image_names]
response = pipe(('describe these images', images))

print(response)
