# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.5159
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class StructuredResultData(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'document_format': 'str',
        'version': 'str',
        'name': 'str',
        'document': 'str',
        'data_map_key': 'DataMapKey'
    }

    attribute_map = {
        'document_format': 'documentFormat',
        'version': 'version',
        'name': 'name',
        'document': 'document',
        'data_map_key': 'dataMapKey'
    }

    required_map = {
        'document_format': 'required',
        'version': 'optional',
        'name': 'optional',
        'document': 'required',
        'data_map_key': 'optional'
    }

    def __init__(self, document_format=None, version=None, name=None, document=None, data_map_key=None, local_vars_configuration=None):  # noqa: E501
        """StructuredResultData - a model defined in OpenAPI"
        
        :param document_format:  The format of the accompanying document. (required)
        :type document_format: str
        :param version:  The semantic version of the document format; MAJOR.MINOR.PATCH
        :type version: str
        :param name:  The name or description for the document
        :type name: str
        :param document:  The document that will be stored (or retrieved) and which describes a unit result data entity such as a set of prices or yields (required)
        :type document: str
        :param data_map_key: 
        :type data_map_key: lusid.DataMapKey

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._document_format = None
        self._version = None
        self._name = None
        self._document = None
        self._data_map_key = None
        self.discriminator = None

        self.document_format = document_format
        self.version = version
        self.name = name
        self.document = document
        if data_map_key is not None:
            self.data_map_key = data_map_key

    @property
    def document_format(self):
        """Gets the document_format of this StructuredResultData.  # noqa: E501

        The format of the accompanying document.  # noqa: E501

        :return: The document_format of this StructuredResultData.  # noqa: E501
        :rtype: str
        """
        return self._document_format

    @document_format.setter
    def document_format(self, document_format):
        """Sets the document_format of this StructuredResultData.

        The format of the accompanying document.  # noqa: E501

        :param document_format: The document_format of this StructuredResultData.  # noqa: E501
        :type document_format: str
        """
        if self.local_vars_configuration.client_side_validation and document_format is None:  # noqa: E501
            raise ValueError("Invalid value for `document_format`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                document_format is not None and len(document_format) > 128):
            raise ValueError("Invalid value for `document_format`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                document_format is not None and len(document_format) < 0):
            raise ValueError("Invalid value for `document_format`, length must be greater than or equal to `0`")  # noqa: E501

        self._document_format = document_format

    @property
    def version(self):
        """Gets the version of this StructuredResultData.  # noqa: E501

        The semantic version of the document format; MAJOR.MINOR.PATCH  # noqa: E501

        :return: The version of this StructuredResultData.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this StructuredResultData.

        The semantic version of the document format; MAJOR.MINOR.PATCH  # noqa: E501

        :param version: The version of this StructuredResultData.  # noqa: E501
        :type version: str
        """

        self._version = version

    @property
    def name(self):
        """Gets the name of this StructuredResultData.  # noqa: E501

        The name or description for the document  # noqa: E501

        :return: The name of this StructuredResultData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StructuredResultData.

        The name or description for the document  # noqa: E501

        :param name: The name of this StructuredResultData.  # noqa: E501
        :type name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 256):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def document(self):
        """Gets the document of this StructuredResultData.  # noqa: E501

        The document that will be stored (or retrieved) and which describes a unit result data entity such as a set of prices or yields  # noqa: E501

        :return: The document of this StructuredResultData.  # noqa: E501
        :rtype: str
        """
        return self._document

    @document.setter
    def document(self, document):
        """Sets the document of this StructuredResultData.

        The document that will be stored (or retrieved) and which describes a unit result data entity such as a set of prices or yields  # noqa: E501

        :param document: The document of this StructuredResultData.  # noqa: E501
        :type document: str
        """
        if self.local_vars_configuration.client_side_validation and document is None:  # noqa: E501
            raise ValueError("Invalid value for `document`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                document is not None and len(document) > 256000):
            raise ValueError("Invalid value for `document`, length must be less than or equal to `256000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                document is not None and len(document) < 0):
            raise ValueError("Invalid value for `document`, length must be greater than or equal to `0`")  # noqa: E501

        self._document = document

    @property
    def data_map_key(self):
        """Gets the data_map_key of this StructuredResultData.  # noqa: E501


        :return: The data_map_key of this StructuredResultData.  # noqa: E501
        :rtype: lusid.DataMapKey
        """
        return self._data_map_key

    @data_map_key.setter
    def data_map_key(self, data_map_key):
        """Sets the data_map_key of this StructuredResultData.


        :param data_map_key: The data_map_key of this StructuredResultData.  # noqa: E501
        :type data_map_key: lusid.DataMapKey
        """

        self._data_map_key = data_map_key

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, StructuredResultData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StructuredResultData):
            return True

        return self.to_dict() != other.to_dict()
