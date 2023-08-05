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


class CashFlowValueSet(object):
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
        'cashflows': 'list[CashFlowValue]',
        'result_value_type': 'str'
    }

    attribute_map = {
        'cashflows': 'cashflows',
        'result_value_type': 'resultValueType'
    }

    required_map = {
        'cashflows': 'optional',
        'result_value_type': 'required'
    }

    def __init__(self, cashflows=None, result_value_type=None, local_vars_configuration=None):  # noqa: E501
        """CashFlowValueSet - a model defined in OpenAPI"
        
        :param cashflows:  The set of cash flows in the result
        :type cashflows: list[lusid.CashFlowValue]
        :param result_value_type:  The available values are: ResultValue, ResultValueDictionary, ResultValue0D, ResultValueDecimal, ResultValueInt, ResultValueString, CashFlowValue, CashFlowValueSet, ResultValueLifeCycleEventValue, ResultValueDateTimeOffset (required)
        :type result_value_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cashflows = None
        self._result_value_type = None
        self.discriminator = None

        self.cashflows = cashflows
        self.result_value_type = result_value_type

    @property
    def cashflows(self):
        """Gets the cashflows of this CashFlowValueSet.  # noqa: E501

        The set of cash flows in the result  # noqa: E501

        :return: The cashflows of this CashFlowValueSet.  # noqa: E501
        :rtype: list[lusid.CashFlowValue]
        """
        return self._cashflows

    @cashflows.setter
    def cashflows(self, cashflows):
        """Sets the cashflows of this CashFlowValueSet.

        The set of cash flows in the result  # noqa: E501

        :param cashflows: The cashflows of this CashFlowValueSet.  # noqa: E501
        :type cashflows: list[lusid.CashFlowValue]
        """

        self._cashflows = cashflows

    @property
    def result_value_type(self):
        """Gets the result_value_type of this CashFlowValueSet.  # noqa: E501

        The available values are: ResultValue, ResultValueDictionary, ResultValue0D, ResultValueDecimal, ResultValueInt, ResultValueString, CashFlowValue, CashFlowValueSet, ResultValueLifeCycleEventValue, ResultValueDateTimeOffset  # noqa: E501

        :return: The result_value_type of this CashFlowValueSet.  # noqa: E501
        :rtype: str
        """
        return self._result_value_type

    @result_value_type.setter
    def result_value_type(self, result_value_type):
        """Sets the result_value_type of this CashFlowValueSet.

        The available values are: ResultValue, ResultValueDictionary, ResultValue0D, ResultValueDecimal, ResultValueInt, ResultValueString, CashFlowValue, CashFlowValueSet, ResultValueLifeCycleEventValue, ResultValueDateTimeOffset  # noqa: E501

        :param result_value_type: The result_value_type of this CashFlowValueSet.  # noqa: E501
        :type result_value_type: str
        """
        if self.local_vars_configuration.client_side_validation and result_value_type is None:  # noqa: E501
            raise ValueError("Invalid value for `result_value_type`, must not be `None`")  # noqa: E501
        allowed_values = ["ResultValue", "ResultValueDictionary", "ResultValue0D", "ResultValueDecimal", "ResultValueInt", "ResultValueString", "CashFlowValue", "CashFlowValueSet", "ResultValueLifeCycleEventValue", "ResultValueDateTimeOffset"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and result_value_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `result_value_type` ({0}), must be one of {1}"  # noqa: E501
                .format(result_value_type, allowed_values)
            )

        self._result_value_type = result_value_type

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
        if not isinstance(other, CashFlowValueSet):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CashFlowValueSet):
            return True

        return self.to_dict() != other.to_dict()
