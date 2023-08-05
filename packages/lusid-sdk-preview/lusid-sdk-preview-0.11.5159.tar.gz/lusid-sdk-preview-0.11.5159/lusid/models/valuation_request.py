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


class ValuationRequest(object):
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
        'recipe_id': 'ResourceId',
        'as_at': 'datetime',
        'metrics': 'list[AggregateSpec]',
        'group_by': 'list[str]',
        'filters': 'list[PropertyFilter]',
        'sort': 'list[OrderBySpec]',
        'report_currency': 'str',
        'equip_with_subtotals': 'bool',
        'return_result_as_expanded_types': 'bool',
        'portfolio_entity_ids': 'list[PortfolioEntityId]',
        'valuation_schedule': 'ValuationSchedule',
        'market_data_overrides': 'MarketDataOverrides'
    }

    attribute_map = {
        'recipe_id': 'recipeId',
        'as_at': 'asAt',
        'metrics': 'metrics',
        'group_by': 'groupBy',
        'filters': 'filters',
        'sort': 'sort',
        'report_currency': 'reportCurrency',
        'equip_with_subtotals': 'equipWithSubtotals',
        'return_result_as_expanded_types': 'returnResultAsExpandedTypes',
        'portfolio_entity_ids': 'portfolioEntityIds',
        'valuation_schedule': 'valuationSchedule',
        'market_data_overrides': 'marketDataOverrides'
    }

    required_map = {
        'recipe_id': 'required',
        'as_at': 'optional',
        'metrics': 'required',
        'group_by': 'optional',
        'filters': 'optional',
        'sort': 'optional',
        'report_currency': 'optional',
        'equip_with_subtotals': 'optional',
        'return_result_as_expanded_types': 'optional',
        'portfolio_entity_ids': 'required',
        'valuation_schedule': 'required',
        'market_data_overrides': 'optional'
    }

    def __init__(self, recipe_id=None, as_at=None, metrics=None, group_by=None, filters=None, sort=None, report_currency=None, equip_with_subtotals=None, return_result_as_expanded_types=None, portfolio_entity_ids=None, valuation_schedule=None, market_data_overrides=None, local_vars_configuration=None):  # noqa: E501
        """ValuationRequest - a model defined in OpenAPI"
        
        :param recipe_id:  (required)
        :type recipe_id: lusid.ResourceId
        :param as_at:  The asAt date to use
        :type as_at: datetime
        :param metrics:  The set of specifications to calculate or retrieve during the valuation and present in the results. For example:  AggregateSpec('Valuation/PV','Sum') for returning the PV (present value) of holdings  AggregateSpec('Holding/default/Units','Sum') for returning the units of holidays  AggregateSpec('Instrument/default/LusidInstrumentId','Value') for returning the Lusid Instrument identifier (required)
        :type metrics: list[lusid.AggregateSpec]
        :param group_by:  The set of items by which to perform grouping. This primarily matters when one or more of the metric operators is a mapping  that reduces set size, e.g. sum or proportion. The group-by statement determines the set of keys by which to break the results out.
        :type group_by: list[str]
        :param filters:  A set of filters to use to reduce the data found in a request. Equivalent to the 'where ...' part of a Sql select statement.  For example, filter a set of values within a given range or matching a particular value.
        :type filters: list[lusid.PropertyFilter]
        :param sort:  A (possibly empty/null) set of specifications for how to order the results.
        :type sort: list[lusid.OrderBySpec]
        :param report_currency:  Three letter ISO currency string indicating what currency to report in for ReportCurrency denominated queries.  If not present, then the currency of the relevant portfolio will be used in its place.
        :type report_currency: str
        :param equip_with_subtotals:  Flag directing the Valuation call to populate the results with subtotals of aggregates.
        :type equip_with_subtotals: bool
        :param return_result_as_expanded_types:  Financially meaningful results can be presented as either simple flat types or more complex expanded types.  For example, the present value (PV) of a holding could be represented either as a simple decimal (with currency implied)  or as a decimal-currency pair. This flag allows either representation to be returned. In the PV example,  the returned value would be the decimal-currency pair if this flag is true, or the decimal only if this flag is false.
        :type return_result_as_expanded_types: bool
        :param portfolio_entity_ids:  The set of portfolio or portfolio group identifier(s) that is to be valued. (required)
        :type portfolio_entity_ids: list[lusid.PortfolioEntityId]
        :param valuation_schedule:  (required)
        :type valuation_schedule: lusid.ValuationSchedule
        :param market_data_overrides: 
        :type market_data_overrides: lusid.MarketDataOverrides

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._recipe_id = None
        self._as_at = None
        self._metrics = None
        self._group_by = None
        self._filters = None
        self._sort = None
        self._report_currency = None
        self._equip_with_subtotals = None
        self._return_result_as_expanded_types = None
        self._portfolio_entity_ids = None
        self._valuation_schedule = None
        self._market_data_overrides = None
        self.discriminator = None

        self.recipe_id = recipe_id
        self.as_at = as_at
        self.metrics = metrics
        self.group_by = group_by
        self.filters = filters
        self.sort = sort
        self.report_currency = report_currency
        if equip_with_subtotals is not None:
            self.equip_with_subtotals = equip_with_subtotals
        if return_result_as_expanded_types is not None:
            self.return_result_as_expanded_types = return_result_as_expanded_types
        self.portfolio_entity_ids = portfolio_entity_ids
        self.valuation_schedule = valuation_schedule
        if market_data_overrides is not None:
            self.market_data_overrides = market_data_overrides

    @property
    def recipe_id(self):
        """Gets the recipe_id of this ValuationRequest.  # noqa: E501


        :return: The recipe_id of this ValuationRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._recipe_id

    @recipe_id.setter
    def recipe_id(self, recipe_id):
        """Sets the recipe_id of this ValuationRequest.


        :param recipe_id: The recipe_id of this ValuationRequest.  # noqa: E501
        :type recipe_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and recipe_id is None:  # noqa: E501
            raise ValueError("Invalid value for `recipe_id`, must not be `None`")  # noqa: E501

        self._recipe_id = recipe_id

    @property
    def as_at(self):
        """Gets the as_at of this ValuationRequest.  # noqa: E501

        The asAt date to use  # noqa: E501

        :return: The as_at of this ValuationRequest.  # noqa: E501
        :rtype: datetime
        """
        return self._as_at

    @as_at.setter
    def as_at(self, as_at):
        """Sets the as_at of this ValuationRequest.

        The asAt date to use  # noqa: E501

        :param as_at: The as_at of this ValuationRequest.  # noqa: E501
        :type as_at: datetime
        """

        self._as_at = as_at

    @property
    def metrics(self):
        """Gets the metrics of this ValuationRequest.  # noqa: E501

        The set of specifications to calculate or retrieve during the valuation and present in the results. For example:  AggregateSpec('Valuation/PV','Sum') for returning the PV (present value) of holdings  AggregateSpec('Holding/default/Units','Sum') for returning the units of holidays  AggregateSpec('Instrument/default/LusidInstrumentId','Value') for returning the Lusid Instrument identifier  # noqa: E501

        :return: The metrics of this ValuationRequest.  # noqa: E501
        :rtype: list[lusid.AggregateSpec]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """Sets the metrics of this ValuationRequest.

        The set of specifications to calculate or retrieve during the valuation and present in the results. For example:  AggregateSpec('Valuation/PV','Sum') for returning the PV (present value) of holdings  AggregateSpec('Holding/default/Units','Sum') for returning the units of holidays  AggregateSpec('Instrument/default/LusidInstrumentId','Value') for returning the Lusid Instrument identifier  # noqa: E501

        :param metrics: The metrics of this ValuationRequest.  # noqa: E501
        :type metrics: list[lusid.AggregateSpec]
        """
        if self.local_vars_configuration.client_side_validation and metrics is None:  # noqa: E501
            raise ValueError("Invalid value for `metrics`, must not be `None`")  # noqa: E501

        self._metrics = metrics

    @property
    def group_by(self):
        """Gets the group_by of this ValuationRequest.  # noqa: E501

        The set of items by which to perform grouping. This primarily matters when one or more of the metric operators is a mapping  that reduces set size, e.g. sum or proportion. The group-by statement determines the set of keys by which to break the results out.  # noqa: E501

        :return: The group_by of this ValuationRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._group_by

    @group_by.setter
    def group_by(self, group_by):
        """Sets the group_by of this ValuationRequest.

        The set of items by which to perform grouping. This primarily matters when one or more of the metric operators is a mapping  that reduces set size, e.g. sum or proportion. The group-by statement determines the set of keys by which to break the results out.  # noqa: E501

        :param group_by: The group_by of this ValuationRequest.  # noqa: E501
        :type group_by: list[str]
        """

        self._group_by = group_by

    @property
    def filters(self):
        """Gets the filters of this ValuationRequest.  # noqa: E501

        A set of filters to use to reduce the data found in a request. Equivalent to the 'where ...' part of a Sql select statement.  For example, filter a set of values within a given range or matching a particular value.  # noqa: E501

        :return: The filters of this ValuationRequest.  # noqa: E501
        :rtype: list[lusid.PropertyFilter]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this ValuationRequest.

        A set of filters to use to reduce the data found in a request. Equivalent to the 'where ...' part of a Sql select statement.  For example, filter a set of values within a given range or matching a particular value.  # noqa: E501

        :param filters: The filters of this ValuationRequest.  # noqa: E501
        :type filters: list[lusid.PropertyFilter]
        """

        self._filters = filters

    @property
    def sort(self):
        """Gets the sort of this ValuationRequest.  # noqa: E501

        A (possibly empty/null) set of specifications for how to order the results.  # noqa: E501

        :return: The sort of this ValuationRequest.  # noqa: E501
        :rtype: list[lusid.OrderBySpec]
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """Sets the sort of this ValuationRequest.

        A (possibly empty/null) set of specifications for how to order the results.  # noqa: E501

        :param sort: The sort of this ValuationRequest.  # noqa: E501
        :type sort: list[lusid.OrderBySpec]
        """

        self._sort = sort

    @property
    def report_currency(self):
        """Gets the report_currency of this ValuationRequest.  # noqa: E501

        Three letter ISO currency string indicating what currency to report in for ReportCurrency denominated queries.  If not present, then the currency of the relevant portfolio will be used in its place.  # noqa: E501

        :return: The report_currency of this ValuationRequest.  # noqa: E501
        :rtype: str
        """
        return self._report_currency

    @report_currency.setter
    def report_currency(self, report_currency):
        """Sets the report_currency of this ValuationRequest.

        Three letter ISO currency string indicating what currency to report in for ReportCurrency denominated queries.  If not present, then the currency of the relevant portfolio will be used in its place.  # noqa: E501

        :param report_currency: The report_currency of this ValuationRequest.  # noqa: E501
        :type report_currency: str
        """
        if (self.local_vars_configuration.client_side_validation and
                report_currency is not None and len(report_currency) > 3):
            raise ValueError("Invalid value for `report_currency`, length must be less than or equal to `3`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                report_currency is not None and len(report_currency) < 0):
            raise ValueError("Invalid value for `report_currency`, length must be greater than or equal to `0`")  # noqa: E501

        self._report_currency = report_currency

    @property
    def equip_with_subtotals(self):
        """Gets the equip_with_subtotals of this ValuationRequest.  # noqa: E501

        Flag directing the Valuation call to populate the results with subtotals of aggregates.  # noqa: E501

        :return: The equip_with_subtotals of this ValuationRequest.  # noqa: E501
        :rtype: bool
        """
        return self._equip_with_subtotals

    @equip_with_subtotals.setter
    def equip_with_subtotals(self, equip_with_subtotals):
        """Sets the equip_with_subtotals of this ValuationRequest.

        Flag directing the Valuation call to populate the results with subtotals of aggregates.  # noqa: E501

        :param equip_with_subtotals: The equip_with_subtotals of this ValuationRequest.  # noqa: E501
        :type equip_with_subtotals: bool
        """

        self._equip_with_subtotals = equip_with_subtotals

    @property
    def return_result_as_expanded_types(self):
        """Gets the return_result_as_expanded_types of this ValuationRequest.  # noqa: E501

        Financially meaningful results can be presented as either simple flat types or more complex expanded types.  For example, the present value (PV) of a holding could be represented either as a simple decimal (with currency implied)  or as a decimal-currency pair. This flag allows either representation to be returned. In the PV example,  the returned value would be the decimal-currency pair if this flag is true, or the decimal only if this flag is false.  # noqa: E501

        :return: The return_result_as_expanded_types of this ValuationRequest.  # noqa: E501
        :rtype: bool
        """
        return self._return_result_as_expanded_types

    @return_result_as_expanded_types.setter
    def return_result_as_expanded_types(self, return_result_as_expanded_types):
        """Sets the return_result_as_expanded_types of this ValuationRequest.

        Financially meaningful results can be presented as either simple flat types or more complex expanded types.  For example, the present value (PV) of a holding could be represented either as a simple decimal (with currency implied)  or as a decimal-currency pair. This flag allows either representation to be returned. In the PV example,  the returned value would be the decimal-currency pair if this flag is true, or the decimal only if this flag is false.  # noqa: E501

        :param return_result_as_expanded_types: The return_result_as_expanded_types of this ValuationRequest.  # noqa: E501
        :type return_result_as_expanded_types: bool
        """

        self._return_result_as_expanded_types = return_result_as_expanded_types

    @property
    def portfolio_entity_ids(self):
        """Gets the portfolio_entity_ids of this ValuationRequest.  # noqa: E501

        The set of portfolio or portfolio group identifier(s) that is to be valued.  # noqa: E501

        :return: The portfolio_entity_ids of this ValuationRequest.  # noqa: E501
        :rtype: list[lusid.PortfolioEntityId]
        """
        return self._portfolio_entity_ids

    @portfolio_entity_ids.setter
    def portfolio_entity_ids(self, portfolio_entity_ids):
        """Sets the portfolio_entity_ids of this ValuationRequest.

        The set of portfolio or portfolio group identifier(s) that is to be valued.  # noqa: E501

        :param portfolio_entity_ids: The portfolio_entity_ids of this ValuationRequest.  # noqa: E501
        :type portfolio_entity_ids: list[lusid.PortfolioEntityId]
        """
        if self.local_vars_configuration.client_side_validation and portfolio_entity_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `portfolio_entity_ids`, must not be `None`")  # noqa: E501

        self._portfolio_entity_ids = portfolio_entity_ids

    @property
    def valuation_schedule(self):
        """Gets the valuation_schedule of this ValuationRequest.  # noqa: E501


        :return: The valuation_schedule of this ValuationRequest.  # noqa: E501
        :rtype: lusid.ValuationSchedule
        """
        return self._valuation_schedule

    @valuation_schedule.setter
    def valuation_schedule(self, valuation_schedule):
        """Sets the valuation_schedule of this ValuationRequest.


        :param valuation_schedule: The valuation_schedule of this ValuationRequest.  # noqa: E501
        :type valuation_schedule: lusid.ValuationSchedule
        """
        if self.local_vars_configuration.client_side_validation and valuation_schedule is None:  # noqa: E501
            raise ValueError("Invalid value for `valuation_schedule`, must not be `None`")  # noqa: E501

        self._valuation_schedule = valuation_schedule

    @property
    def market_data_overrides(self):
        """Gets the market_data_overrides of this ValuationRequest.  # noqa: E501


        :return: The market_data_overrides of this ValuationRequest.  # noqa: E501
        :rtype: lusid.MarketDataOverrides
        """
        return self._market_data_overrides

    @market_data_overrides.setter
    def market_data_overrides(self, market_data_overrides):
        """Sets the market_data_overrides of this ValuationRequest.


        :param market_data_overrides: The market_data_overrides of this ValuationRequest.  # noqa: E501
        :type market_data_overrides: lusid.MarketDataOverrides
        """

        self._market_data_overrides = market_data_overrides

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
        if not isinstance(other, ValuationRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ValuationRequest):
            return True

        return self.to_dict() != other.to_dict()
