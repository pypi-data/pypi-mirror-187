import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *


@jsii.enum(jsii_type="neulabs-cdk-constructs.env.TagsKey")
class TagsKey(enum.Enum):
    ENVIRONMENT = "ENVIRONMENT"
    TIMESTAMP_DEPLOY_CDK = "TIMESTAMP_DEPLOY_CDK"
    BUSINESS_UNIT = "BUSINESS_UNIT"
    DOMAIN = "DOMAIN"
    REPOSITORY_NAME = "REPOSITORY_NAME"
    REPOSITORY_VERSION = "REPOSITORY_VERSION"


__all__ = [
    "TagsKey",
]

publication.publish()
