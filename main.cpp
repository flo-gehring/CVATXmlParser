//
// Created by flo on 07.01.19.
//

#include <iostream>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>
#include "CVATXMLParser.h"


int main(int argc, char **argv) {

    char *docname;

    if (argc <= 1) {
        printf("Usage: %s docname\n", argv[0]);
        return(0);
    }
    docname = argv[1];
    std::cout << docname << std::endl;
    cvatp::CVATXML doc(docname, cvatp::INTERPOLATION);
    doc.parse();

    return (1);
}

