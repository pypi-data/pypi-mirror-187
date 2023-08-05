# Copyright 2022 The KServe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    KServe

    Python SDK for KServe  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from kserve.configuration import Configuration


class V1beta1LoggerSpec(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'mode': 'str',
        'url': 'str'
    }

    attribute_map = {
        'mode': 'mode',
        'url': 'url'
    }

    def __init__(self, mode=None, url=None, local_vars_configuration=None):  # noqa: E501
        """V1beta1LoggerSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._mode = None
        self._url = None
        self.discriminator = None

        if mode is not None:
            self.mode = mode
        if url is not None:
            self.url = url

    @property
    def mode(self):
        """Gets the mode of this V1beta1LoggerSpec.  # noqa: E501

        Specifies the scope of the loggers. <br /> Valid values are: <br /> - \"all\" (default): log both request and response; <br /> - \"request\": log only request; <br /> - \"response\": log only response <br />  # noqa: E501

        :return: The mode of this V1beta1LoggerSpec.  # noqa: E501
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this V1beta1LoggerSpec.

        Specifies the scope of the loggers. <br /> Valid values are: <br /> - \"all\" (default): log both request and response; <br /> - \"request\": log only request; <br /> - \"response\": log only response <br />  # noqa: E501

        :param mode: The mode of this V1beta1LoggerSpec.  # noqa: E501
        :type: str
        """

        self._mode = mode

    @property
    def url(self):
        """Gets the url of this V1beta1LoggerSpec.  # noqa: E501

        URL to send logging events  # noqa: E501

        :return: The url of this V1beta1LoggerSpec.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this V1beta1LoggerSpec.

        URL to send logging events  # noqa: E501

        :param url: The url of this V1beta1LoggerSpec.  # noqa: E501
        :type: str
        """

        self._url = url

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1beta1LoggerSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1beta1LoggerSpec):
            return True

        return self.to_dict() != other.to_dict()
