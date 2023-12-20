from PIL import Image
import numpy as np

aurora = np.asarray(Image.open('frames/frame0001.png')).astype("uint32")
for i in range(1, 50):
    aurora += np.asarray(Image.open(f'frames/frame{i:04}.png'))
aurora = Image.fromarray((aurora//50).astype("uint8"))
aurora.show()
aurora.save('solve.png')