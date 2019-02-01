import xml.etree.ElementTree as ET
from copy import deepcopy
import json
import csv
import sys

import cv2

import argparse


# Some Constants

CORRESPONDENCE = u'correspondence'
MISS = u'miss'
FALSE_POSITIVE = u'false positive'
MISSMATCH = u'mismatch'

def get_annotations_for_frame(frame_counter, frames_list):
    if(frames_list[frame_counter]["timestamp"] == frame_counter):
        return frames_list[frame_counter]["annotations"]

    else:
        for frame in frames_list:
            if frame["timestamp"] == frame_counter:
                return frame["annotations"]

def get_bottom_left(x, y, width, heigth):
    return (x + width, y + heigth)


COLOR_SCHEME = {
    u'miss': (204, 0, 153),
    u'false positive': (204, 51, 0),
    u'correspondence': (255, 255, 255),
    u'mismatch': (0, 0, 255)
}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("debugfile", help="Path to Inputfile, "
                                       "in visual debug format as given by pymot")

    parser.add_argument("videofile", help="Path to the tracked Video")
    parser.add_argument("--inspect", help="Use this flag if the video should halt another class than a correspondence appears ",
                        action="store_true")


    args = parser.parse_args()

    print("Opening Video: ")
    videocapture = cv2.VideoCapture(args.videofile)
    if(videocapture.isOpened()):
        print("\t Success!")
    else:
        print("\t Error, abort.")
        sys.exit()


    print("Opening JSON File...")
    jsonfile = open(args.debugfile, "r")
    if(jsonfile is not None):
        print("\t File loaded, decoding JSON...")
    else:
        print("File could not be opened, does file exist and can be read?")
        sys.exit()

    loaded_json = json.load(jsonfile)
    frames_list = loaded_json[0]["frames"]
    print("JSON decoded, begin video playback..")

    ret, frame = videocapture.read()

    frame_counter = 0
    annotations_for_frame = list()

    all_correspond = True

    error_descriptions = list()

    while ret :

        error_descriptions = list()

        annotations_for_frame = get_annotations_for_frame(frame_counter, frames_list)
        all_correspond = True


        for annotation in annotations_for_frame:
            annotation_class = annotation["class"]
            color = COLOR_SCHEME[annotation_class]



            x = int(annotation["x"])
            y = int(annotation["y"])
            width = int(annotation["width"])
            height = int(annotation["height"])

            if(annotation_class != CORRESPONDENCE):
                description = annotation_class + ", id: " + str(len(error_descriptions))
                cv2.putText(frame, str(len(error_descriptions)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            1, color ,2 ,cv2.LINE_AA)
                error_descriptions.append(description)

            all_correspond &= (annotation_class == CORRESPONDENCE)
            cv2.rectangle(frame, (x,y), get_bottom_left(x, y, width, height), color)

        description_counter = 1
        for description in error_descriptions:
            cv2.putText(frame, description, (10, description_counter * 40), cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0,0,0))
            description_counter += 1


        frame = cv2.resize(frame, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
        cv2.imshow('frame', frame)
        if args.inspect:
            while  not (all_correspond or cv2.waitKey(1) & 0xFF == ord(' ')):
                pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = videocapture.read()
        frame_counter += 1


    videocapture.release()
    cv2.destroyAllWindows()


