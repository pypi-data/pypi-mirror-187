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


class DependencySourceFilter(object):
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
        'instrument_type': 'str',
        'asset_class': 'str',
        'dom_ccy': 'str'
    }

    attribute_map = {
        'instrument_type': 'instrumentType',
        'asset_class': 'assetClass',
        'dom_ccy': 'domCcy'
    }

    required_map = {
        'instrument_type': 'optional',
        'asset_class': 'optional',
        'dom_ccy': 'optional'
    }

    def __init__(self, instrument_type=None, asset_class=None, dom_ccy=None, local_vars_configuration=None):  # noqa: E501
        """DependencySourceFilter - a model defined in OpenAPI"
        
        :param instrument_type:  Specify that a rule should only apply if the market data is requested by an instrument of a given instrument type.  If null, then no filtering on instrument type is applied.
        :type instrument_type: str
        :param asset_class:  Specify that a rule should only apply if the market data is requested by an instrument of a given asset class.  If null, then no filtering on asset class is applied.
        :type asset_class: str
        :param dom_ccy:  Specify that a rule should only apply if the market data is requested by an instrument with a given domestic currency.  If null, then no filtering on currency is applied.
        :type dom_ccy: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._instrument_type = None
        self._asset_class = None
        self._dom_ccy = None
        self.discriminator = None

        self.instrument_type = instrument_type
        self.asset_class = asset_class
        self.dom_ccy = dom_ccy

    @property
    def instrument_type(self):
        """Gets the instrument_type of this DependencySourceFilter.  # noqa: E501

        Specify that a rule should only apply if the market data is requested by an instrument of a given instrument type.  If null, then no filtering on instrument type is applied.  # noqa: E501

        :return: The instrument_type of this DependencySourceFilter.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this DependencySourceFilter.

        Specify that a rule should only apply if the market data is requested by an instrument of a given instrument type.  If null, then no filtering on instrument type is applied.  # noqa: E501

        :param instrument_type: The instrument_type of this DependencySourceFilter.  # noqa: E501
        :type instrument_type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                instrument_type is not None and len(instrument_type) > 32):
            raise ValueError("Invalid value for `instrument_type`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                instrument_type is not None and len(instrument_type) < 0):
            raise ValueError("Invalid value for `instrument_type`, length must be greater than or equal to `0`")  # noqa: E501

        self._instrument_type = instrument_type

    @property
    def asset_class(self):
        """Gets the asset_class of this DependencySourceFilter.  # noqa: E501

        Specify that a rule should only apply if the market data is requested by an instrument of a given asset class.  If null, then no filtering on asset class is applied.  # noqa: E501

        :return: The asset_class of this DependencySourceFilter.  # noqa: E501
        :rtype: str
        """
        return self._asset_class

    @asset_class.setter
    def asset_class(self, asset_class):
        """Sets the asset_class of this DependencySourceFilter.

        Specify that a rule should only apply if the market data is requested by an instrument of a given asset class.  If null, then no filtering on asset class is applied.  # noqa: E501

        :param asset_class: The asset_class of this DependencySourceFilter.  # noqa: E501
        :type asset_class: str
        """
        if (self.local_vars_configuration.client_side_validation and
                asset_class is not None and len(asset_class) > 32):
            raise ValueError("Invalid value for `asset_class`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                asset_class is not None and len(asset_class) < 0):
            raise ValueError("Invalid value for `asset_class`, length must be greater than or equal to `0`")  # noqa: E501

        self._asset_class = asset_class

    @property
    def dom_ccy(self):
        """Gets the dom_ccy of this DependencySourceFilter.  # noqa: E501

        Specify that a rule should only apply if the market data is requested by an instrument with a given domestic currency.  If null, then no filtering on currency is applied.  # noqa: E501

        :return: The dom_ccy of this DependencySourceFilter.  # noqa: E501
        :rtype: str
        """
        return self._dom_ccy

    @dom_ccy.setter
    def dom_ccy(self, dom_ccy):
        """Sets the dom_ccy of this DependencySourceFilter.

        Specify that a rule should only apply if the market data is requested by an instrument with a given domestic currency.  If null, then no filtering on currency is applied.  # noqa: E501

        :param dom_ccy: The dom_ccy of this DependencySourceFilter.  # noqa: E501
        :type dom_ccy: str
        """

        self._dom_ccy = dom_ccy

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
        if not isinstance(other, DependencySourceFilter):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DependencySourceFilter):
            return True

        return self.to_dict() != other.to_dict()
