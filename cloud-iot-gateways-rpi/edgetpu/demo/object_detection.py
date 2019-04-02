"""A demo for object detection.

For Raspberry Pi, you need to install 'feh' as image viewer:
sudo apt-get install feh

Example (Running under python-tflite-source/edgetpu directory):

  - Face detection:
    python3.5 demo/object_detection.py \
    --model='test_data/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite' \
    --input='test_data/face.jpg'

  - Pet detection:
    python3.5 demo/object_detection.py \
    --model='test_data/ssd_mobilenet_v1_fine_tuned_edgetpu.tflite' \
    --label='test_data/pet_labels.txt' \
    --input='test_data/pets.jpg'

'--output' is an optional flag to specify file name of output image.
"""
import argparse
import platform
import subprocess
from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from PIL import ImageDraw
import picamera
import io
import time
import numpy as np
# import cv2


# Function to read labels from text files.
def ReadLabelFile(file_path):
  with open(file_path, 'r') as f:
    lines = f.readlines()
  ret = {}
  for line in lines:
    pair = line.strip().split(maxsplit=1)
    ret[int(pair[0])] = pair[1].strip()
  return ret


def main(model='./test_data/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite'):
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--model', help='Path of the detection model.', default = model)
  parser.add_argument(
      '--label', help='Path of the labels file.')
  parser.add_argument(
      '--input', help='File path of the input image.', required=False)
  parser.add_argument(
      '--output', help='File path of the output image.')
  args = parser.parse_args()

  if not args.output:
    output_name = 'object_detection_result.jpg'
  else:
    output_name = args.output

  # Initialize engine.
  engine = DetectionEngine(args.model)
  labels = ReadLabelFile(args.label) if args.label else None

  with picamera.PiCamera() as camera:
      camera.resolution = (1028, 712)
      camera.framerate = 30
      _, width, height, channels = engine.get_input_tensor_shape()
      camera.start_preview()
      try:
          stream = io.BytesIO()
          for foo in camera.capture_continuous(stream,
                                               format='rgb',
                                               use_video_port=True,
                                               resize=(width, height)):
              stream.truncate()
              stream.seek(0)
              input = np.frombuffer(stream.getvalue(), dtype=np.uint8)
              # cv2.imwrite('current_frame.jpg', input)
              # img = Image.open('current_frame.jpg')
              # draw = ImageDraw.Draw(img)
              start_ms = time.time()
              ans = engine.DetectWithInputTensor(input, threshold=0.5, top_k=10)
              elapsed_ms = time.time() - start_ms
              # Display result.
              print ('-----------------------------------------')
              nPerson = 0
              bbox = list()
              scores = list()
              if ans:
                print(ans)
                for obj in ans:
                  nPerson = nPerson+ 1
                  if labels:
                    print(labels[obj.label_id])
                  score = [obj.score]
                  print ('score = ', obj.score)
                  box = obj.bounding_box.flatten().tolist()
                  print ('box = ', box)
                  # Draw a rectangle.
                #   draw.rectangle(box, outline='red')
                # img.save(output_name)
                # if platform.machine() == 'x86_64':
                #   # For gLinux, simply show the image.
                #   img.show()
                # elif platform.machine() == 'armv7l':
                #   # For Raspberry Pi, you need to install 'feh' to display image.
                #   subprocess.Popen(['feh', output_name])
                # else:
                #   print ('Please check ', output_name)
                  bbox.append(box)
                  scores.append(score)
                msg = {"nPersons":int(nPerson), "bounding_box":str(bbox), "scores": str(scores)}
                print("nPerson = " + str(nPerson))
                # msg = {"nPersons":int(nPerson)}
                # print(msg)
                return msg
              else:
                print ('No object detected!')
                msg = {"nPersons":int(nPerson), "bounding_box":str(bbox), "scores": str(scores)}
                # msg = {"nPersons":int(nPerson)}
                # print(msg)
                return msg
      finally:
          camera.stop_preview()

if __name__ == '__main__':
  main()
