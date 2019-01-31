#! /usr/bin/python3.6

import xml.etree.ElementTree as ET
from copy import deepcopy
import json
import csv


class Track:
        def __init__(self):
                self.tracked_elements = dict()


class Box:
        def __init__(self, xml_node=None):
            if xml_node is not None:
                self.attributes = deepcopy(xml_node.attrib)
            else:
                self.attributes = dict()



class Polygon:
        def __init__(self, xml_node):
                self.attributes = deepcopy(xml_node.attrib)


class CVATDocument:

        def __init__(self, filepath=''):
            self.tracks = list()
            self.max_frame = 0
            self.doc_tree = None
            if filepath is not '':
                    self.doc_tree = ET.parse(filepath)

        def open_doc(self, filepath):
                self.doc_tree = ET.parse(filepath)

        def parse(self):
            if self.doc_tree is None:
                        raise ValueError("Doc Tree is none")

            root = self.doc_tree.getroot()
            self.max_frame = 0

            for child in root:
                    if child.tag == 'track':
                        new_track = Track()
                        for node in child:
                                frame = int(node.attrib['frame'])
                                self.max_frame = max(self.max_frame, frame)
                                new_track.tracked_elements[frame] = parse_node(node)
                        self.tracks.append(new_track)

        """
        MOT Format is used for the Multiple Object Tracking Benchmark.
        Documented on their [Website](https://motchallenge.net/instructions/) under the section Format. 
        conf will be 0, x,y and z will always be -1.
        <id> will simply the position of the track in the list.
        
        <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
        1, 3, 794.27, 247.59, 71.245, 174.88, -1, -1, -1, -1
        1, 6, 1648.1, 119.61, 66.504, 163.24, -1, -1, -1, -1
        1, 8, 875.49, 399.98, 95.303, 233.93, -1, -1, -1, -1
        """

        def to_format(self, format_id, filepath=''):
            output_file = None
            if not filepath == '':
                output_file = open(filepath, "w")
            
            uniqueId = 0
            if format_id in ["2D MOT 2015", "MOT16", "PETS2017", "MOT17"]:
                        for frame in range(0, (self.max_frame + 1)):
                                for track in self.tracks:
                                        if frame in track.tracked_elements:
                                                frame_info = track.tracked_elements[frame].attributes
                                                bb_left = float(frame_info['xtl'])
                                                bb_top = float(frame_info['ytl'])
                                                bb_width = float(frame_info['xbr']) - bb_left
                                                bb_height = float(frame_info['ybr']) - bb_top

                                                formatted_line = "{0}, {1}, {2}, {3}, {4}, " \
                                                                 "{5}, {6}, {7}, {7}, {7} \n".format(
                                                                        frame,         
                                                                        #-1,
                                                                        self.tracks.index(track),
                                                                        bb_left, bb_top, bb_width,
                                                                        bb_height, 0, -1)

                                                if output_file is not None:
                                                        output_file.write(formatted_line)

                                                print(formatted_line)

        def to_sloth_format(self, groundtruth = False, output_path=''):

            sloth_representation = [ {'frames':[]}]

            sloth_representation[0]['class'] = 'video'
            sloth_representation[0]['filename'] = 'dontcare.mp4'

            frames_list = sloth_representation[0]['frames']

            if not output_path == '':
                output_file = open(output_path, "w")

            for frame in range(0, self.max_frame + 1):
                frames_list.append({
                    'timestamp': frame,
                    'frame': frame,
                    'class': 'frame',
                })
                annotation_list = None
                if not groundtruth:
                    frames_list[-1]['hypotheses'] = list()
                    annotation_list = frames_list[-1]['hypotheses']
                else:
                    frames_list[-1]['annotations'] = list()
                    annotation_list = frames_list[-1]['annotations']

                for track in self.tracks:
                    if frame in track.tracked_elements:
                        annotation_list.append(dict())
                        current_annotation = annotation_list[-1]

                        frame_info = track.tracked_elements[frame].attributes
                        bb_left = float(frame_info['xtl'])
                        bb_top = float(frame_info['ytl'])
                        current_annotation['width'] = float(frame_info['xbr']) - bb_left
                        current_annotation['height'] = float(frame_info['ybr']) - bb_top

                        current_annotation['x'] = bb_left
                        current_annotation['y'] = bb_top

                        current_annotation['id'] = self.tracks.index(track)

                        if groundtruth:
                            current_annotation['dco'] = bool(float(frame_info['outside'])) or\
                                                        bool(float(frame_info['occluded']))

            json_string = json.dumps(sloth_representation, sort_keys=True, indent=4)
            if(not output_path == ''):
                output_file.write(json_string)
            else:
                print(json_string)


        def MOT_to_CVAT_parsetree(self, docpath):
            num_ids = 0
            map_id_trackindex = dict()

            self.tracks = list()
            self.doc_tree = None
            self.max_frame = -1
            input_file = open(docpath, 'r')

            with open(docpath, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    (frame, id, bb_left, bb_top, bb_width, bb_height, conf) = row[0:7]

                    frame = int(frame)

                    # get the right track
                    object_track = None
                    if id not in map_id_trackindex:
                        current_track = Track()
                        self.tracks.append(current_track)
                        map_id_trackindex[id] = num_ids
                        num_ids += 1
                    else:
                        current_track = self.tracks[map_id_trackindex[id]]

                    new_box = Box()
                    current_track.tracked_elements[frame] = new_box
                    new_box.attributes['ytl'] = float(bb_top)
                    new_box.attributes['xtl'] = float(bb_left)
                    new_box.attributes['xbr'] = str(float(bb_left) + float(bb_width))
                    new_box.attributes['ybr'] = str(float(bb_height)+ float(bb_top))

            self.max_frame = int(frame)


def parse_node(node):
        if node.tag == 'box':
                return Box(node)
        if node.tag == 'polygon':
                return Polygon(node)




# Get Ground Truth from CVAT
gtDoc = CVATDocument('2_TS_10_05.xml')
gtDoc.parse()
gtDoc.to_sloth_format(groundtruth=True, output_path='groundtruth.json')

# Get tracking results Doc

trDoc = CVATDocument()
trDoc.MOT_to_CVAT_parsetree('trackingResult_ts_10_05.txt')
trDoc.to_sloth_format(output_path='hypotheses.json')


#doc.to_format("MOT17", 'asdf.txt')

# doc.MOT_to_CVAT_parsetree('trackingResult_ts_10_05.txt')
#doc.to_format("MOT17", '2_.txt')
