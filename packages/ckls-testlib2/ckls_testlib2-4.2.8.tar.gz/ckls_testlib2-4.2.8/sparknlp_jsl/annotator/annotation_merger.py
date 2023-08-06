from sparknlp import Finisher
from sparknlp_jsl.common import *


class AnnotationMerger(AnnotatorModelInternal):
    """
    Merges Annotations from multiple columns.

    ====================== ======================
    Input Annotation types Output Annotation type
    ====================== ======================
    ``ANY``                ``ANY``
    ====================== ======================

    Parameters
    ----------
    inputType
        The type of the annotations that you want to merge. Possible values
        ``document|token|wordpiece|word_embeddings|sentence_embeddings|category|date|sentiment|pos|chunk|named_entity|regex|dependency|labeled_dependency|language|keyword``

    Examples
    --------
>>> docs = [[""]]
>>> test_data = spark.createDataFrame(docs).toDF("text")
>>> document1 = DocumentAssembler().setInputCol("text").setOutputCol("document1")
>>> document2 = DocumentAssembler().setInputCol("text").setOutputCol("document2")
>>> annotation_merger = AnnotationMerger()\
...     .setInputCols("document1", "document2")\
...     .setInputType("document")\
...     .setOutputCol("all_docs")
>>>
>>> pipeline = Pipeline().setStages([document1, document2, annotation_merger]).fit(docs)
>>> lp = LightPipeline(pipeline)
>>> lp.fullAnnotate("one doc to be replicated")
[{'document1': [Annotation(document, 0, 23, one doc to be replicated, {})], 'document2': [Annotation(document, 0, 23, one doc to be replicated, {})], 'all_docs': [Annotation(document, 0, 23, one doc to be replicated, {}), Annotation(document, 0, 23, one doc to be replicated, {})]}]


    """
    inputAnnotatorTypes = [AnnotatorType.DOCUMENT, AnnotatorType.TOKEN]
    outputAnnotatorType = [AnnotatorType.DOCUMENT, AnnotatorType.TOKEN]
    skipLPInputColsValidation = True

    name = "AnnotationMerger"

    inputType = Param(Params._dummy(), "inputType",
                      "The type of the entity that you want to filter by default sentence_embeddings.Possible values document|token|wordpiece|word_embeddings|"
                      "sentence_embeddings|category|date|sentiment|pos|chunk|named_entity|regex|dependency|labeled_dependency|language|keyword ",
                      TypeConverters.toString)

    def setInputType(self, value):
        """Sets the type of the entity that you want to filter by default sentence_embedding

        Parameters
        ----------
        value : int
            The type of the entity that you want to filter by default sentence_embedding
        """
        return self._set(inputType=value)

    def __init__(self, classname="com.johnsnowlabs.annotator.AnnotationMerger", java_model=None):
        super(AnnotationMerger, self).__init__(
            classname=classname,
            java_model=java_model
        )

    def setInputCols(self, *value):
        """Sets column names of input annotations.
        Parameters
        ----------
        *value : str
            Input columns for the annotator
        """
        # Overloaded setInputCols to evade validation until updated on Spark-NLP side
        if type(value[0]) == str or type(value[0]) == list:
            # self.inputColsValidation(value)
            if len(value) == 1 and type(value[0]) == list:
                return self._set(inputCols=value[0])
            else:
                return self._set(inputCols=list(value))
        else:
            raise TypeError("InputCols datatype not supported. It must be either str or list")
