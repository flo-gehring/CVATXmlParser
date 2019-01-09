import xml.etree.ElementTree as ET
from copy import deepcopy


class Track:
        def __init__(self):
                self.tracked_elements = dict()


class Box:
        def __init__(self, xml_node):
                self.attributes = deepcopy(xml_node.attrib)


class Polygon:
        def __init__(self, xml_node):
                self.attributes = deepcopy(xml_node.attrib)


class CVATDocument:

        def __init__(self, filepath=''):
            self.tracks = list()
            self.max_frame = 0
            self.doc_tree = None
            if filepath is not '':
                    self.doc_tree = ET.parse('example.xml')

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
                                new_track.tracked_elements[frame] = parse(node)
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
                output_file = open(filepath)

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
                                                                        frame, self.tracks.index(track),
                                                                        bb_left, bb_top, bb_width,
                                                                        bb_height, 0, -1)

                                                if output_file is not None:
                                                        output_file.write(formatted_line)

                                                print(formatted_line)


def parse(node):
        if node.tag == 'box':
                return Box(node)
        if node.tag == 'polygon':
                return Polygon(node)


doc = CVATDocument('example.xml')
doc.parse()
doc.to_format("MOT17")
