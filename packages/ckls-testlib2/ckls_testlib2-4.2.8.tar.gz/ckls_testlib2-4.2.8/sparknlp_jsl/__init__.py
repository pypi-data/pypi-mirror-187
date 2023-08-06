import os
import re
import sys
from pyspark.sql import SparkSession
from sparknlp_jsl import finance
from sparknlp_jsl import legal
from sparknlp_jsl import annotator
# from util import read_version

import com.johnsnowlabs
com.johnsnowlabs.legal = legal
com.johnsnowlabs.finance = finance
com.johnsnowlabs.annotator = annotator
sys.modules['com.johnsnowlabs.annotator'] = annotator

sys.modules['com.johnsnowlabs.nlp.annotators.assertion'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.assertion.logreg'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.assertion.dl'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.resolution'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.deid'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.classification'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.generic_classifier'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.context'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.merge'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.keyword'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.re'] = annotator
sys.modules['com.johnsnowlabs.nlp.annotators.chunker'] = annotator

sys.modules['com.johnsnowlabs.finance'] = finance
sys.modules['com.johnsnowlabs.finance.token_classification'] = finance
sys.modules['com.johnsnowlabs.finance.token_classification.ner'] = finance
sys.modules['com.johnsnowlabs.finance.chunk_classification'] = finance
sys.modules['com.johnsnowlabs.finance.chunk_classification.resolution'] = finance
sys.modules['com.johnsnowlabs.finance.chunk_classification.deid'] = finance
sys.modules['com.johnsnowlabs.finance.chunk_classification.assert'] = finance
sys.modules['com.johnsnowlabs.finance.chunk_classification.assertion'] = finance
sys.modules['com.johnsnowlabs.finance.graph'] = finance
sys.modules['com.johnsnowlabs.finance.graph.relation_extraction'] = finance
sys.modules['com.johnsnowlabs.finance.sequence_classification'] = finance

sys.modules['com.johnsnowlabs.legal'] = legal
sys.modules['com.johnsnowlabs.legal.token_classification'] = legal
sys.modules['com.johnsnowlabs.legal.token_classification.ner'] = legal
sys.modules['com.johnsnowlabs.legal.chunk_classification'] = legal
sys.modules['com.johnsnowlabs.legal.chunk_classification.resolution'] = legal
sys.modules['com.johnsnowlabs.legal.chunk_classification.deid'] = legal
sys.modules['com.johnsnowlabs.legal.chunk_classification.assert'] = legal
sys.modules['com.johnsnowlabs.legal.chunk_classification.assertion'] = legal
sys.modules['com.johnsnowlabs.legal.graph'] = legal
sys.modules['com.johnsnowlabs.legal.graph.relation_extraction'] = legal
sys.modules['com.johnsnowlabs.legal.sequence_classification'] = legal

annotators = annotator
transformer_seq_classification = annotator

version_regex = re.compile("^(\\d+\\.)(\\d+\\.)(\\*|\\d+)(-?rc\\d*)?$")
size_regex = re.compile("([0-9])+[GMK]")


def start(secret, gpu=False, m1=False, public="", params=None):
    if params is None:
        params = {}
    if '_instantiatedSession' in dir(SparkSession) and SparkSession._instantiatedSession is not None:
        print('Warning::Spark Session already created, some configs may not take.')

    try:
        matched = re.match(version_regex, public)
        if matched:
            public = matched.string
        else:
            public = pub_version()
    except:
        public = pub_version()

    # Spark NLP on Apache Spark 3.0.x
    maven_spark = "com.johnsnowlabs.nlp:spark-nlp_2.12:{}".format(public)
    maven_gpu_spark = "com.johnsnowlabs.nlp:spark-nlp-gpu_2.12:{}".format(public)
    maven_m1_spark = "com.johnsnowlabs.nlp:spark-nlp-m1_2.12:{}".format(public)

    __check_size_and_overwrite("spark.driver.memory", "32G", params)
    __check_size_and_overwrite("spark.kryoserializer.buffer.max", "2000M", params)
    __check_size_and_overwrite("spark.driver.maxResultSize", "2000M", params)

    params.update({"spark.serializer": "org.apache.spark.serializer.KryoSerializer"})

    builder = SparkSession.builder \
        .appName("Spark NLP Licensed") \
        .master("local[*]")

    for key, value in params.items():
        builder.config(key, value)

    if gpu:
        builder.config("spark.jars.packages", maven_gpu_spark)
        builder.config("spark.jars", "https://pypi.johnsnowlabs.com/" + secret + f"/spark-nlp-jsl-{version()}.jar")
    elif m1:
        builder.config("spark.jars.packages", maven_m1_spark)
        builder.config("spark.jars", "https://pypi.johnsnowlabs.com/" + secret + f"/spark-nlp-jsl-{version()}.jar")
    else:
        builder.config("spark.jars.packages", maven_spark)
        builder.config("spark.jars", "https://pypi.johnsnowlabs.com/" + secret + f"/spark-nlp-jsl-{version()}.jar")

    # Force the check of the license and load of S3 credentials
    spark = builder.getOrCreate()

    spark._jvm.com.johnsnowlabs.util.start.registerListenerAndStartRefresh()
    return spark


def get_credentials(spark):
    creds = spark._jvm.com.johnsnowlabs.util.start.getAwsCredentials()
    return (creds.secretKey(), creds.keyId(), creds.token())


def __check_size_and_overwrite(key, defaultValue, params):
    if (params.get(key)):
        value = params[key]
        matched = re.match(size_regex, value)
        if not matched:
            params[key] = defaultValue
    else:
        params[key] = defaultValue


def pub_version():
    return read_version.get_version_from_file('PUBLIC_VERSION')


def version():
    return read_version.get_version_from_file('VERSION')


def library_settings(spark):
    configs = spark._jvm.com.johnsnowlabs.util.LibrarySettings.getAllConfigsAsString()
    return configs


def __set_s3_credentials_as_spark_properties(spark):
    credentials = spark._jvm.com.johnsnowlabs.license.LicenseValidator.getS3Credentials()
    if credentials.isDefined():
        awsid = credentials.get()._2()
        secret = credentials.get()._1()
        spark.conf.set("spark.jsl.settings.pretrained.credentials.secret_access_key", secret)
        spark.conf.set("spark.jsl.settings.pretrained.credentials.access_key_id", awsid)

# auto register and start refresh for databricks environments
if "DATABRICKS_RUNTIME_VERSION" in os.environ and "AWS_ACCESS_KEY_ID" not in os.environ:
    try:
        from pyspark.sql import SparkSession
        SparkSession.getActiveSession()._jvm.com.johnsnowlabs.util.start.registerListenerAndStartRefresh()
    except:
        print("Warning::Can not fetch aws credentials. you need to start the library manually using sparknlp_jsl.start().")

# set ipython kernel name as env variable
try:
    from IPython import get_ipython
    os.environ["IPYTHON_NAME"] =  str(get_ipython())
except:
    pass
