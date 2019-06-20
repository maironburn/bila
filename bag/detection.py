from imageai.Detection import ObjectDetection
import os

# model_path = "resnet50_weights_tf_dim_ordering_tf_kernels.h5"
from config import input_folder, model_path, input_image, dataset_folder, output_folder

# prediction = ImagePrediction()
# prediction.setModelTypeAsResNet()
# prediction.setModelPath(os.path.join(os.getcwd(), "dataset", model_path))
# prediction.loadModel()
#
# predictions, percentage_probabilities = prediction.predictImage(os.path.join("input", input_image), result_count=30)
# for index in range(len(predictions)):
#     print(predictions[index], " : ", percentage_probabilities[index])
from models import Coord

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(os.getcwd(), dataset_folder, model_path))
detector.loadModel()
detections, extracted_objects = detector.detectObjectsFromImage(input_image=os.path.join(input_folder, input_image),
                                                                # output_type="array",
                                                                output_image_path=os.path.join(output_folder,
                                                                                               input_image),
                                                                extract_detected_objects=True,

                                                                minimum_percentage_probability=60)


def create_region_info(detection):
    coord = detection.get("box_points").tolist()

    region_info = Coord(
        x1=coord[0],
        y1=coord[1],
        x2=coord[2],
        y2=coord[3],
        name=detection.get("name"),
        percent_accuracy=detection.get("percentage_probability"),
    ).__dict__

    return region_info


if len(detections) == 1:
    print(create_region_info(detections[0]))


elif len(detections) > 1:
    for detection in detections:
        print(create_region_info(detection))
else:
    print("No se ha detectado imagen")
