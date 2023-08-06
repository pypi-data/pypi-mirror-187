from sparknlp_jsl.common import *


class ReIdentification(AnnotatorModelInternal):
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.CHUNK]
    outputAnnotatorType = AnnotatorType.DOCUMENT
    name = "ReDeideintification"

    def __init__(self, classname="com.johnsnowlabs.nlp.annotators.deid.ReIdentification", java_model=None):
        super(ReIdentification, self).__init__(
            classname=classname,
            java_model=java_model
        )