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


class RawVendorEventAllOf(object):
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
        'effective_at': 'datetime',
        'event_value': 'LifeCycleEventValue',
        'event_type': 'str',
        'event_status': 'str',
        'instrument_event_type': 'str'
    }

    attribute_map = {
        'effective_at': 'effectiveAt',
        'event_value': 'eventValue',
        'event_type': 'eventType',
        'event_status': 'eventStatus',
        'instrument_event_type': 'instrumentEventType'
    }

    required_map = {
        'effective_at': 'required',
        'event_value': 'required',
        'event_type': 'required',
        'event_status': 'required',
        'instrument_event_type': 'required'
    }

    def __init__(self, effective_at=None, event_value=None, event_type=None, event_status=None, instrument_event_type=None, local_vars_configuration=None):  # noqa: E501
        """RawVendorEventAllOf - a model defined in OpenAPI"
        
        :param effective_at:  The effective date of the event (required)
        :type effective_at: datetime
        :param event_value:  (required)
        :type event_value: lusid.LifeCycleEventValue
        :param event_type:  What type of internal event does this represent; reset, exercise, amortisation etc. (required)
        :type event_type: str
        :param event_status:  What is the event status, is it a known (ie historic) or unknown (ie projected) event? (required)
        :type event_status: str
        :param instrument_event_type:  The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent, TriggerEvent, RawVendorEvent, InformationalErrorEvent (required)
        :type instrument_event_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._effective_at = None
        self._event_value = None
        self._event_type = None
        self._event_status = None
        self._instrument_event_type = None
        self.discriminator = None

        self.effective_at = effective_at
        self.event_value = event_value
        self.event_type = event_type
        self.event_status = event_status
        self.instrument_event_type = instrument_event_type

    @property
    def effective_at(self):
        """Gets the effective_at of this RawVendorEventAllOf.  # noqa: E501

        The effective date of the event  # noqa: E501

        :return: The effective_at of this RawVendorEventAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_at

    @effective_at.setter
    def effective_at(self, effective_at):
        """Sets the effective_at of this RawVendorEventAllOf.

        The effective date of the event  # noqa: E501

        :param effective_at: The effective_at of this RawVendorEventAllOf.  # noqa: E501
        :type effective_at: datetime
        """
        if self.local_vars_configuration.client_side_validation and effective_at is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_at`, must not be `None`")  # noqa: E501

        self._effective_at = effective_at

    @property
    def event_value(self):
        """Gets the event_value of this RawVendorEventAllOf.  # noqa: E501


        :return: The event_value of this RawVendorEventAllOf.  # noqa: E501
        :rtype: lusid.LifeCycleEventValue
        """
        return self._event_value

    @event_value.setter
    def event_value(self, event_value):
        """Sets the event_value of this RawVendorEventAllOf.


        :param event_value: The event_value of this RawVendorEventAllOf.  # noqa: E501
        :type event_value: lusid.LifeCycleEventValue
        """
        if self.local_vars_configuration.client_side_validation and event_value is None:  # noqa: E501
            raise ValueError("Invalid value for `event_value`, must not be `None`")  # noqa: E501

        self._event_value = event_value

    @property
    def event_type(self):
        """Gets the event_type of this RawVendorEventAllOf.  # noqa: E501

        What type of internal event does this represent; reset, exercise, amortisation etc.  # noqa: E501

        :return: The event_type of this RawVendorEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this RawVendorEventAllOf.

        What type of internal event does this represent; reset, exercise, amortisation etc.  # noqa: E501

        :param event_type: The event_type of this RawVendorEventAllOf.  # noqa: E501
        :type event_type: str
        """
        if self.local_vars_configuration.client_side_validation and event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `event_type`, must not be `None`")  # noqa: E501

        self._event_type = event_type

    @property
    def event_status(self):
        """Gets the event_status of this RawVendorEventAllOf.  # noqa: E501

        What is the event status, is it a known (ie historic) or unknown (ie projected) event?  # noqa: E501

        :return: The event_status of this RawVendorEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._event_status

    @event_status.setter
    def event_status(self, event_status):
        """Sets the event_status of this RawVendorEventAllOf.

        What is the event status, is it a known (ie historic) or unknown (ie projected) event?  # noqa: E501

        :param event_status: The event_status of this RawVendorEventAllOf.  # noqa: E501
        :type event_status: str
        """
        if self.local_vars_configuration.client_side_validation and event_status is None:  # noqa: E501
            raise ValueError("Invalid value for `event_status`, must not be `None`")  # noqa: E501

        self._event_status = event_status

    @property
    def instrument_event_type(self):
        """Gets the instrument_event_type of this RawVendorEventAllOf.  # noqa: E501

        The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent, TriggerEvent, RawVendorEvent, InformationalErrorEvent  # noqa: E501

        :return: The instrument_event_type of this RawVendorEventAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_event_type

    @instrument_event_type.setter
    def instrument_event_type(self, instrument_event_type):
        """Sets the instrument_event_type of this RawVendorEventAllOf.

        The Type of Event. The available values are: TransitionEvent, InformationalEvent, OpenEvent, CloseEvent, StockSplitEvent, BondDefaultEvent, CashDividendEvent, AmortisationEvent, CashFlowEvent, ExerciseEvent, ResetEvent, TriggerEvent, RawVendorEvent, InformationalErrorEvent  # noqa: E501

        :param instrument_event_type: The instrument_event_type of this RawVendorEventAllOf.  # noqa: E501
        :type instrument_event_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_event_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_event_type`, must not be `None`")  # noqa: E501
        allowed_values = ["TransitionEvent", "InformationalEvent", "OpenEvent", "CloseEvent", "StockSplitEvent", "BondDefaultEvent", "CashDividendEvent", "AmortisationEvent", "CashFlowEvent", "ExerciseEvent", "ResetEvent", "TriggerEvent", "RawVendorEvent", "InformationalErrorEvent"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_event_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_event_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_event_type, allowed_values)
            )

        self._instrument_event_type = instrument_event_type

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
        if not isinstance(other, RawVendorEventAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RawVendorEventAllOf):
            return True

        return self.to_dict() != other.to_dict()
