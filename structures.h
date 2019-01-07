//
// Created by flo on 07.01.19.
//

#ifndef CVATXMLPARSER_STRUCTURES_H
#define CVATXMLPARSER_STRUCTURES_H

#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include <vector>
#include <tuple>

// https://github.com/opencv/cvat/blob/develop/cvat/apps/documentation/xml_format.md#interpolation


namespace cvatp {
    /*
    <?xml version="1.0" encoding="utf-8"?>
    <annotations>
    ...
    <track id="Number: id of the track (doesn't have any special meeting" label="String: the associated label">
                                                                                <box frame="Number: frame" xtl="Number: float" ytl="Number: float" xbr="Number: float" ybr="Number: float" outside="Number: 0 - False, 1 - True" occluded="Number: 0 - False, 1 - True" keyframe="Number: 0 - False, 1 - True">
                                                                                                                                                                                                                                                                                 <attribute name="String: an attribute name">String: the attribute value</attribute>
    ...
    </box>
    <polygon frame="Number: frame" points="x0,y0;x1,y1;..." outside="Number: 0 - False, 1 - True" occluded="Number: 0 - False, 1 - True" keyframe="Number: 0 - False, 1 - True">
                                                                                                                                                  <attribute name="String: an attribute name">String: the attribute value</attribute>
    </polygon>
    <polyline frame="Number: frame" points="x0,y0;x1,y1;..." outside="Number: 0 - False, 1 - True" occluded="Number: 0 - False, 1 - True" keyframe="Number: 0 - False, 1 - True">
                                                                                                                                                   <attribute name="String: an attribute name">String: the attribute value</attribute>
    </polyline>
    <points frame="Number: frame" points="x0,y0;x1,y1;..." outside="Number: 0 - False, 1 - True" occluded="Number: 0 - False, 1 - True" keyframe="Number: 0 - False, 1 - True">
                                                                                                                                                 <attribute name="String: an attribute name">String: the attribute value</attribute>
    </points>
    ...
    </track>
    ...
    </annotations>
     */
    class attributes {

    public:
        std::string info;

    };

    enum OBJECT_TYPE{
        BOX,
        POLYGON,
        POLYLINE

    };
    /*
     * <box frame="Number: frame" xtl="Number: float" ytl="Number: float" xbr="Number: float" ybr="Number: float" outside="Number: 0 - False, 1 - True" occluded="Number: 0 - False, 1 - True" keyframe="Number: 0 - False, 1 - True">
      <attribute name="String: an attribute name">String: the attribute value</attribute>
      ...
    </box>
     */

    class AnnotationObject {
    public:
        unsigned long frameNumber;
        bool outside, occluded, keyframe;
        // std::vector<attributes> attributes;
        explicit AnnotationObject(xmlNodePtr nodePtr);
        OBJECT_TYPE type;



    };

    class box : public AnnotationObject{
    public:
        explicit box(xmlNodePtr nodePtr);
        float xtl, ytl, xbr, ybr;

    };

    class polygon: public AnnotationObject{
    public:
        explicit polygon(xmlNodePtr nodePtr);
        std::vector<std::tuple<float, float>> points;


    };

    class track{

    public:
        std::vector<AnnotationObject *> annotatedObjects;
        std::vector<box> boxes;
        void parseTrack(xmlNodePtr nodePtr);
        void parseBoxes(xmlNodePtr nodePtr);

    };


}


#endif //CVATXMLPARSER_STRUCTURES_H
