//
// Created by flo on 07.01.19.
//

#include "structures.h"



void cvatp::track::parseTrack(xmlNodePtr nodePtr) {

    nodePtr = nodePtr->xmlChildrenNode;

    while (nodePtr != NULL) {
        if ((!xmlStrcmp(nodePtr->name, (const xmlChar *)"box"))) {
            annotatedObjects.emplace_back(new box(nodePtr));
        }
        else if((!xmlStrcmp(nodePtr->name, (const xmlChar *)"polygon"))){

            annotatedObjects.emplace_back(new polygon(nodePtr));

        }
        nodePtr =nodePtr->next;
    }
}

void cvatp::track::parseBoxes(xmlNodePtr nodePtr) {
    nodePtr = nodePtr->xmlChildrenNode;

    while (nodePtr != NULL) {
        if ((!xmlStrcmp(nodePtr->name, (const xmlChar *)"box"))) {
            boxes.emplace_back(box(nodePtr));
        }
        nodePtr =nodePtr->next;
    }
}


cvatp::polygon::polygon(xmlNodePtr nodePtr) : AnnotationObject(nodePtr) {

    type = POLYGON;

}

cvatp::box::box(xmlNodePtr nodePtr) : AnnotationObject(nodePtr) {

    xtl = std::stof((char *)(xmlGetProp(nodePtr, (const unsigned char *)"xtl")));
    ytl = std::stof((char *)(xmlGetProp(nodePtr, (const unsigned char *)"ytl")));
    xbr = std::stof((char *)(xmlGetProp(nodePtr, (const unsigned char *)"xbr")));
    ybr = std::stof((char *)(xmlGetProp(nodePtr, (const unsigned char *)"ybr")));

    type = BOX;

}

cvatp::AnnotationObject::AnnotationObject(xmlNodePtr nodePtr) {
    xmlChar * xmlFrame = xmlGetProp(nodePtr, (const xmlChar *)"frame");
    xmlChar * xmlOutside = xmlGetProp(nodePtr, (const xmlChar*) "outside");
    xmlChar * xmlOccluded = xmlGetProp(nodePtr, (const xmlChar*)"occluded");
    xmlChar * xmlKeyframe = xmlGetProp(nodePtr, (const xmlChar*)"keyframe");

    frameNumber = std::stoul((char *)xmlFrame);
    outside = bool(xmlOutside[0] & 1);
    occluded = bool(xmlOccluded[0] & 1);
    keyframe = bool(xmlKeyframe[0] & 1);



}
