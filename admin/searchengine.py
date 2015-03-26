from admin_classes import *


class SearchenginePage(webapp.RequestHandler):
    def get(self, cse_id):
        gdatafeed = GdataFeed(
            "http://www.google.com/cse/api/default/cse/%s" % cse_id
        )
        path = os.path.join(
            os.path.dirname(__file__),
            'templates/searchengine.html'
        )
        self.response.out.write(
            template.render(
                path,
                {'response': unicode(gdatafeed.response, errors="ignore"),
                 'searchengine': ""}
            )
        )


class SearchenginesPage(webapp.RequestHandler):
    def get(self):
        # gdatafeed = GdataFeed("http://www.google.com/cse/api/default/cse/")
        # searchengines = map(
        #     lambda cse_xml: SearchEngineFromXml(cse_xml),
        #     gdatafeed.elements("CustomSearchEngine")
        # )

        gdatafeed2 = GdataFeed(
            "http://www.google.com/cse/api/default/annotations/?num=5000")
        annotations = map(
            lambda annotation_xml: AnnotationFromXml(annotation_xml),
            gdatafeed2.elements("Annotation")
        )
        path = os.path.join(
            os.path.dirname(__file__),
            'templates/searchengines.html'
        )
        self.response.out.write(
            template.render(
                path,
                {'response': unicode(gdatafeed2.response, errors="ignore"),
                 'searchengines': searchengines,
                 'annotations': annotations
                 }
            )
        )
