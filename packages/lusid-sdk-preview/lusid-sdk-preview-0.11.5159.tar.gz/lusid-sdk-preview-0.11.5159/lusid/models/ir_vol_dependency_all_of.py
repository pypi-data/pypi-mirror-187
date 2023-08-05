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


class IrVolDependencyAllOf(object):
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
        'currency': 'str',
        'vol_type': 'str',
        'date': 'datetime',
        'dependency_type': 'str'
    }

    attribute_map = {
        'currency': 'currency',
        'vol_type': 'volType',
        'date': 'date',
        'dependency_type': 'dependencyType'
    }

    required_map = {
        'currency': 'required',
        'vol_type': 'required',
        'date': 'required',
        'dependency_type': 'required'
    }

    def __init__(self, currency=None, vol_type=None, date=None, dependency_type=None, local_vars_configuration=None):  # noqa: E501
        """IrVolDependencyAllOf - a model defined in OpenAPI"
        
        :param currency:  The domestic currency of the instrument declaring this dependency. (required)
        :type currency: str
        :param vol_type:  Volatility type e.g. \"LN\" and \"N\" for log-normal and normal volatility. (required)
        :type vol_type: str
        :param date:  The effectiveDate of the entity that this is a dependency for.  Unless there is an obvious date this should be, like for a historic reset, then this is the valuation date. (required)
        :type date: datetime
        :param dependency_type:  The available values are: Opaque, Cash, Discounting, EquityCurve, EquityVol, Fx, FxForwards, FxVol, IndexProjection, IrVol, Quote, Vendor (required)
        :type dependency_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._currency = None
        self._vol_type = None
        self._date = None
        self._dependency_type = None
        self.discriminator = None

        self.currency = currency
        self.vol_type = vol_type
        self.date = date
        self.dependency_type = dependency_type

    @property
    def currency(self):
        """Gets the currency of this IrVolDependencyAllOf.  # noqa: E501

        The domestic currency of the instrument declaring this dependency.  # noqa: E501

        :return: The currency of this IrVolDependencyAllOf.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this IrVolDependencyAllOf.

        The domestic currency of the instrument declaring this dependency.  # noqa: E501

        :param currency: The currency of this IrVolDependencyAllOf.  # noqa: E501
        :type currency: str
        """
        if self.local_vars_configuration.client_side_validation and currency is None:  # noqa: E501
            raise ValueError("Invalid value for `currency`, must not be `None`")  # noqa: E501

        self._currency = currency

    @property
    def vol_type(self):
        """Gets the vol_type of this IrVolDependencyAllOf.  # noqa: E501

        Volatility type e.g. \"LN\" and \"N\" for log-normal and normal volatility.  # noqa: E501

        :return: The vol_type of this IrVolDependencyAllOf.  # noqa: E501
        :rtype: str
        """
        return self._vol_type

    @vol_type.setter
    def vol_type(self, vol_type):
        """Sets the vol_type of this IrVolDependencyAllOf.

        Volatility type e.g. \"LN\" and \"N\" for log-normal and normal volatility.  # noqa: E501

        :param vol_type: The vol_type of this IrVolDependencyAllOf.  # noqa: E501
        :type vol_type: str
        """
        if self.local_vars_configuration.client_side_validation and vol_type is None:  # noqa: E501
            raise ValueError("Invalid value for `vol_type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                vol_type is not None and len(vol_type) > 50):
            raise ValueError("Invalid value for `vol_type`, length must be less than or equal to `50`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                vol_type is not None and len(vol_type) < 0):
            raise ValueError("Invalid value for `vol_type`, length must be greater than or equal to `0`")  # noqa: E501

        self._vol_type = vol_type

    @property
    def date(self):
        """Gets the date of this IrVolDependencyAllOf.  # noqa: E501

        The effectiveDate of the entity that this is a dependency for.  Unless there is an obvious date this should be, like for a historic reset, then this is the valuation date.  # noqa: E501

        :return: The date of this IrVolDependencyAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this IrVolDependencyAllOf.

        The effectiveDate of the entity that this is a dependency for.  Unless there is an obvious date this should be, like for a historic reset, then this is the valuation date.  # noqa: E501

        :param date: The date of this IrVolDependencyAllOf.  # noqa: E501
        :type date: datetime
        """
        if self.local_vars_configuration.client_side_validation and date is None:  # noqa: E501
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def dependency_type(self):
        """Gets the dependency_type of this IrVolDependencyAllOf.  # noqa: E501

        The available values are: Opaque, Cash, Discounting, EquityCurve, EquityVol, Fx, FxForwards, FxVol, IndexProjection, IrVol, Quote, Vendor  # noqa: E501

        :return: The dependency_type of this IrVolDependencyAllOf.  # noqa: E501
        :rtype: str
        """
        return self._dependency_type

    @dependency_type.setter
    def dependency_type(self, dependency_type):
        """Sets the dependency_type of this IrVolDependencyAllOf.

        The available values are: Opaque, Cash, Discounting, EquityCurve, EquityVol, Fx, FxForwards, FxVol, IndexProjection, IrVol, Quote, Vendor  # noqa: E501

        :param dependency_type: The dependency_type of this IrVolDependencyAllOf.  # noqa: E501
        :type dependency_type: str
        """
        if self.local_vars_configuration.client_side_validation and dependency_type is None:  # noqa: E501
            raise ValueError("Invalid value for `dependency_type`, must not be `None`")  # noqa: E501
        allowed_values = ["Opaque", "Cash", "Discounting", "EquityCurve", "EquityVol", "Fx", "FxForwards", "FxVol", "IndexProjection", "IrVol", "Quote", "Vendor"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and dependency_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `dependency_type` ({0}), must be one of {1}"  # noqa: E501
                .format(dependency_type, allowed_values)
            )

        self._dependency_type = dependency_type

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
        if not isinstance(other, IrVolDependencyAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IrVolDependencyAllOf):
            return True

        return self.to_dict() != other.to_dict()
