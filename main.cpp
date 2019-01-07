//
// Created by flo on 07.01.19.
//

#include <iostream>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include "structures.h"

void
parseTrack(xmlDocPtr doc, xmlNodePtr cur) {

    xmlChar *key;
    xmlChar * uri;
    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *)"box"))) {

            uri = xmlGetProp(cur, (const xmlChar *)"frame");
            key = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
            printf("keyword: %s\n", uri);
            xmlFree(key);
        }
        cur = cur->next;
    }
    return;
}

static void parseDoc(char *docname) {


    std::vector<cvatp::track> track;

    xmlDocPtr doc;
    xmlNodePtr cur;

    doc = xmlParseFile(docname);

    if (doc == NULL ) {
        fprintf(stderr,"Document not parsed successfully. \n");
        return;
    }

    cur = xmlDocGetRootElement(doc);

    if (cur == NULL) {
        fprintf(stderr,"empty document\n");
        xmlFreeDoc(doc);
        return;
    }

    if (xmlStrcmp(cur->name, (const xmlChar *) "annotations")) {
        fprintf(stderr,"document of the wrong type, root node != story");
        xmlFreeDoc(doc);
        return;
    }

    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *)"track" ))){
            track.emplace_back(cvatp::track());
            track.back().parseBoxes(cur);

        }

        cur = cur->next;
    }

    xmlFreeDoc(doc);
    return;
}

int
main(int argc, char **argv) {

    char *docname;

    if (argc <= 1) {
        printf("Usage: %s docname\n", argv[0]);
        return(0);
    }

    docname = argv[1];
    parseDoc (docname);

    return (1);
}

