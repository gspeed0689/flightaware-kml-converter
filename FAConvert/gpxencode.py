from xml.dom import minidom as xdmd
from typing import Optional
from datetime import datetime

class gpx:
    def __init__(self, documentName: str):
        self.doc = xdmd.Document()
        self.gpx = self.create_element(self.doc, "gpx", attributes={"xmlns": "http://www.topografix.com/GPX/1/1",
                                                         "version": "1.1", 
                                                         "creator": "FAConvert", 
                                                         "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                                         "xsi:schemaLocation": "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd "})
        self.metadata = self.create_element(self.gpx, "metadata")
        self.create_element(self.metadata, "name", childTextNode=documentName)
        self.trk = self.create_element(self.gpx, "trk")
        self.trkseg = self.create_element(self.trk, "trkseg")
    def create_element(self, 
                       parent, 
                       elementName: str, 
                       attributes: Optional[dict]=None, 
                       childTextNode: Optional[str]=None, 
                       cdataContentNode: Optional[str]=None):
        new_element = self.doc.createElement(elementName)
        parent.appendChild(new_element)
        if attributes:
            for att in attributes.items():
                new_element.setAttribute(att[0], str(att[1]))
        if childTextNode:
            childTextNodeObject = self.doc.createTextNode(str(childTextNode))
            new_element.appendChild(childTextNodeObject)
        if cdataContentNode:
            cdataContentNodeObject = self.doc.createCDATASection(str(cdataContentNode))
            new_element.appendChild(cdataContentNodeObject)
        return new_element
    def add_point_to_track(self, 
                           lat: float, 
                           lon: float, 
                           time: datetime,
                           ele: Optional[float]=None,
                           ):
        trkpt = self.create_element(self.trkseg, "trkpt", {"lat": lat, "lon": lon})
        ele = self.create_element(trkpt, "ele", childTextNode=ele)
        time = self.create_element(trkpt, "time", childTextNode=time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        

# print(gpx("Example GPX File").doc.toprettyxml())