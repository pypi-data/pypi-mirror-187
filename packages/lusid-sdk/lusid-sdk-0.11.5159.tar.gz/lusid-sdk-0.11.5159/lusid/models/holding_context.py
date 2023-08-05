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


class HoldingContext(object):
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
        'tax_lot_level_holdings': 'bool'
    }

    attribute_map = {
        'tax_lot_level_holdings': 'taxLotLevelHoldings'
    }

    required_map = {
        'tax_lot_level_holdings': 'optional'
    }

    def __init__(self, tax_lot_level_holdings=None, local_vars_configuration=None):  # noqa: E501
        """HoldingContext - a model defined in OpenAPI"
        
        :param tax_lot_level_holdings:  Whether or not to expand the holdings to return the underlying tax-lots. Defaults to True.
        :type tax_lot_level_holdings: bool

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._tax_lot_level_holdings = None
        self.discriminator = None

        if tax_lot_level_holdings is not None:
            self.tax_lot_level_holdings = tax_lot_level_holdings

    @property
    def tax_lot_level_holdings(self):
        """Gets the tax_lot_level_holdings of this HoldingContext.  # noqa: E501

        Whether or not to expand the holdings to return the underlying tax-lots. Defaults to True.  # noqa: E501

        :return: The tax_lot_level_holdings of this HoldingContext.  # noqa: E501
        :rtype: bool
        """
        return self._tax_lot_level_holdings

    @tax_lot_level_holdings.setter
    def tax_lot_level_holdings(self, tax_lot_level_holdings):
        """Sets the tax_lot_level_holdings of this HoldingContext.

        Whether or not to expand the holdings to return the underlying tax-lots. Defaults to True.  # noqa: E501

        :param tax_lot_level_holdings: The tax_lot_level_holdings of this HoldingContext.  # noqa: E501
        :type tax_lot_level_holdings: bool
        """

        self._tax_lot_level_holdings = tax_lot_level_holdings

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
        if not isinstance(other, HoldingContext):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HoldingContext):
            return True

        return self.to_dict() != other.to_dict()
