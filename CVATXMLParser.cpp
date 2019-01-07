//
// Created by flo on 07.01.19.
//

#include "CVATXMLParser.h"



void cvatp::track::parseTrack(xmlNodePtr nodePtr) {

    nodePtr = nodePtr->xmlChildrenNode;
    box * newBox;
    polygon * newPolygon;
    while (nodePtr != NULL) {
        if ((!xmlStrcmp(nodePtr->name, (const xmlChar *)"box"))) {
            newBox = new box(nodePtr);
            boxes.push_back(newBox);
            annotatedObjects.emplace_back(newBox);
        }
        else if((!xmlStrcmp(nodePtr->name, (const xmlChar *)"polygon"))){
            newPolygon = new polygon(nodePtr);
            polygons.push_back(newPolygon);
            annotatedObjects.push_back(newPolygon);

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

cvatp::CVATXML::CVATXML(const char * filename, cvatp::ANNOTATION_TYPE type) {


        std::vector<cvatp::track> track;
        annotationType =type;

        xmlNodePtr cur;

        doc = xmlParseFile(filename);

        if (doc == NULL ) {
            fprintf(stderr,"Document not parsed successfully. \n");
            return;
        }

        cur = xmlDocGetRootElement(doc);

        if (cur == NULL) {
            fprintf(stderr,"empty document\n");
            return;
        }

        if (xmlStrcmp(cur->name, (const xmlChar *) "annotations")) {
            fprintf(stderr,"document of the wrong type, root node != annotations");
            return;
        }
}

cvatp::CVATXML::~CVATXML() {
    xmlFree(doc);
    for(track t: tracks){
        for(AnnotationObject * a: t.annotatedObjects)
            delete a;
    }

}

void cvatp::CVATXML::parse() {

    xmlNodePtr current;
    current = xmlDocGetRootElement(doc);

    current = current->xmlChildrenNode;

    if(annotationType == INTERPOLATION) {
        while (current) {
            if ((!xmlStrcmp(current->name, (const xmlChar *)"track" ))){
                tracks.emplace_back(cvatp::track());
                tracks.back().parseTrack(current);
            }
            current = current->next;
        }
    }


}
