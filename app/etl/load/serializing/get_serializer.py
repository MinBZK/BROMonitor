from etl.load.serializing.serializer_gmw import serializer_gmw
from etl.load.serializing.serializer_bhrgt import serializer_bhrgt
from etl.load.serializing.serializer_sfr import serializer_sfr
from etl.load.serializing.serializer_cpt import serializer_cpt
from etl.load.serializing.serializer_bhrp import serializer_bhrp
from etl.load.serializing.serializer_gmn import serializer_gmn
from etl.load.serializing.serializer_gld import serializer_gld

serializer_mapping = {
    "gmw": serializer_gmw,
    "bhr-gt": serializer_bhrgt,
    "sfr": serializer_sfr,
    "cpt": serializer_cpt,
    "bhr-p": serializer_bhrp,
    "gmn": serializer_gmn,
    "gld": serializer_gld,
}


def get_serializer(type, classes):
    return serializer_mapping[type](classes)
