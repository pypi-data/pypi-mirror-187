# coding: utf-8

"""
    Research Object Certification

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Batch(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'public_key': 'str',
        'crid': 'list[str]',
        'crid_type': 'str',
        'enable_ipfs': 'bool',
        'metadata_json': 'str'
    }

    attribute_map = {
        'public_key': 'publicKey',
        'crid': 'crid',
        'crid_type': 'cridType',
        'enable_ipfs': 'enableIPFS',
        'metadata_json': 'metadataJson'
    }

    def __init__(self, public_key=None, crid=None, crid_type=None, enable_ipfs=None, metadata_json=None):  # noqa: E501
        """Batch - a model defined in Swagger"""  # noqa: E501
        self._public_key = None
        self._crid = None
        self._crid_type = None
        self._enable_ipfs = None
        self._metadata_json = None
        self.discriminator = None
        self.public_key = public_key
        self.crid = crid
        if crid_type is not None:
            self.crid_type = crid_type
        self.enable_ipfs = enable_ipfs
        if metadata_json is not None:
            self.metadata_json = metadata_json

    @property
    def public_key(self):
        """Gets the public_key of this Batch.  # noqa: E501

        Public bloxberg address where the Research Object Certificate token will be minted  # noqa: E501

        :return: The public_key of this Batch.  # noqa: E501
        :rtype: str
        """
        return self._public_key

    @public_key.setter
    def public_key(self, public_key):
        """Sets the public_key of this Batch.

        Public bloxberg address where the Research Object Certificate token will be minted  # noqa: E501

        :param public_key: The public_key of this Batch.  # noqa: E501
        :type: str
        """
        if public_key is None:
            raise ValueError("Invalid value for `public_key`, must not be `None`")  # noqa: E501

        self._public_key = public_key

    @property
    def crid(self):
        """Gets the crid of this Batch.  # noqa: E501

        Cryptographic Identifier of each file you wish to certify. One certificate will be generated per hash up to a maximum of 1001 in a single request  # noqa: E501

        :return: The crid of this Batch.  # noqa: E501
        :rtype: list[str]
        """
        return self._crid

    @crid.setter
    def crid(self, crid):
        """Sets the crid of this Batch.

        Cryptographic Identifier of each file you wish to certify. One certificate will be generated per hash up to a maximum of 1001 in a single request  # noqa: E501

        :param crid: The crid of this Batch.  # noqa: E501
        :type: list[str]
        """
        if crid is None:
            raise ValueError("Invalid value for `crid`, must not be `None`")  # noqa: E501

        self._crid = crid

    @property
    def crid_type(self):
        """Gets the crid_type of this Batch.  # noqa: E501

        If crid is not self-describing, provide the type of cryptographic function you used to generate the cryptographic identifier. Please use the name field from the multihash list to ensure compatibility: https://github.com/multiformats/multicodec/blob/master/table.csv  # noqa: E501

        :return: The crid_type of this Batch.  # noqa: E501
        :rtype: str
        """
        return self._crid_type

    @crid_type.setter
    def crid_type(self, crid_type):
        """Sets the crid_type of this Batch.

        If crid is not self-describing, provide the type of cryptographic function you used to generate the cryptographic identifier. Please use the name field from the multihash list to ensure compatibility: https://github.com/multiformats/multicodec/blob/master/table.csv  # noqa: E501

        :param crid_type: The crid_type of this Batch.  # noqa: E501
        :type: str
        """

        self._crid_type = crid_type

    @property
    def enable_ipfs(self):
        """Gets the enable_ipfs of this Batch.  # noqa: E501

        EXPERIMENTAL: Set to true to enable posting certificate to IPFS. If set to false, will simply return certificates in the response. By default, this is disabled on the server due to performance and storage problems with IPFS  # noqa: E501

        :return: The enable_ipfs of this Batch.  # noqa: E501
        :rtype: bool
        """
        return self._enable_ipfs

    @enable_ipfs.setter
    def enable_ipfs(self, enable_ipfs):
        """Sets the enable_ipfs of this Batch.

        EXPERIMENTAL: Set to true to enable posting certificate to IPFS. If set to false, will simply return certificates in the response. By default, this is disabled on the server due to performance and storage problems with IPFS  # noqa: E501

        :param enable_ipfs: The enable_ipfs of this Batch.  # noqa: E501
        :type: bool
        """
        if enable_ipfs is None:
            raise ValueError("Invalid value for `enable_ipfs`, must not be `None`")  # noqa: E501

        self._enable_ipfs = enable_ipfs

    @property
    def metadata_json(self):
        """Gets the metadata_json of this Batch.  # noqa: E501

        Provide optional metadata to describe the research object batch in more detail that will be included in the certificate.  # noqa: E501

        :return: The metadata_json of this Batch.  # noqa: E501
        :rtype: str
        """
        return self._metadata_json

    @metadata_json.setter
    def metadata_json(self, metadata_json):
        """Sets the metadata_json of this Batch.

        Provide optional metadata to describe the research object batch in more detail that will be included in the certificate.  # noqa: E501

        :param metadata_json: The metadata_json of this Batch.  # noqa: E501
        :type: str
        """

        self._metadata_json = metadata_json

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(Batch, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Batch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
