# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class InfraEnvUpdateParams(object):
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
        'proxy': 'Proxy',
        'additional_ntp_sources': 'str',
        'ssh_authorized_key': 'str',
        'pull_secret': 'str',
        'static_network_config': 'list[HostStaticNetworkConfig]',
        'image_type': 'ImageType',
        'ignition_config_override': 'str',
        'kernel_arguments': 'KernelArguments',
        'additional_trust_bundle': 'str'
    }

    attribute_map = {
        'proxy': 'proxy',
        'additional_ntp_sources': 'additional_ntp_sources',
        'ssh_authorized_key': 'ssh_authorized_key',
        'pull_secret': 'pull_secret',
        'static_network_config': 'static_network_config',
        'image_type': 'image_type',
        'ignition_config_override': 'ignition_config_override',
        'kernel_arguments': 'kernel_arguments',
        'additional_trust_bundle': 'additional_trust_bundle'
    }

    def __init__(self, proxy=None, additional_ntp_sources=None, ssh_authorized_key=None, pull_secret=None, static_network_config=None, image_type=None, ignition_config_override=None, kernel_arguments=None, additional_trust_bundle=None):  # noqa: E501
        """InfraEnvUpdateParams - a model defined in Swagger"""  # noqa: E501

        self._proxy = None
        self._additional_ntp_sources = None
        self._ssh_authorized_key = None
        self._pull_secret = None
        self._static_network_config = None
        self._image_type = None
        self._ignition_config_override = None
        self._kernel_arguments = None
        self._additional_trust_bundle = None
        self.discriminator = None

        if proxy is not None:
            self.proxy = proxy
        if additional_ntp_sources is not None:
            self.additional_ntp_sources = additional_ntp_sources
        if ssh_authorized_key is not None:
            self.ssh_authorized_key = ssh_authorized_key
        if pull_secret is not None:
            self.pull_secret = pull_secret
        if static_network_config is not None:
            self.static_network_config = static_network_config
        if image_type is not None:
            self.image_type = image_type
        if ignition_config_override is not None:
            self.ignition_config_override = ignition_config_override
        if kernel_arguments is not None:
            self.kernel_arguments = kernel_arguments
        if additional_trust_bundle is not None:
            self.additional_trust_bundle = additional_trust_bundle

    @property
    def proxy(self):
        """Gets the proxy of this InfraEnvUpdateParams.  # noqa: E501


        :return: The proxy of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: Proxy
        """
        return self._proxy

    @proxy.setter
    def proxy(self, proxy):
        """Sets the proxy of this InfraEnvUpdateParams.


        :param proxy: The proxy of this InfraEnvUpdateParams.  # noqa: E501
        :type: Proxy
        """

        self._proxy = proxy

    @property
    def additional_ntp_sources(self):
        """Gets the additional_ntp_sources of this InfraEnvUpdateParams.  # noqa: E501

        A comma-separated list of NTP sources (name or IP) going to be added to all the hosts.  # noqa: E501

        :return: The additional_ntp_sources of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: str
        """
        return self._additional_ntp_sources

    @additional_ntp_sources.setter
    def additional_ntp_sources(self, additional_ntp_sources):
        """Sets the additional_ntp_sources of this InfraEnvUpdateParams.

        A comma-separated list of NTP sources (name or IP) going to be added to all the hosts.  # noqa: E501

        :param additional_ntp_sources: The additional_ntp_sources of this InfraEnvUpdateParams.  # noqa: E501
        :type: str
        """

        self._additional_ntp_sources = additional_ntp_sources

    @property
    def ssh_authorized_key(self):
        """Gets the ssh_authorized_key of this InfraEnvUpdateParams.  # noqa: E501

        SSH public key for debugging the installation.  # noqa: E501

        :return: The ssh_authorized_key of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: str
        """
        return self._ssh_authorized_key

    @ssh_authorized_key.setter
    def ssh_authorized_key(self, ssh_authorized_key):
        """Sets the ssh_authorized_key of this InfraEnvUpdateParams.

        SSH public key for debugging the installation.  # noqa: E501

        :param ssh_authorized_key: The ssh_authorized_key of this InfraEnvUpdateParams.  # noqa: E501
        :type: str
        """

        self._ssh_authorized_key = ssh_authorized_key

    @property
    def pull_secret(self):
        """Gets the pull_secret of this InfraEnvUpdateParams.  # noqa: E501

        The pull secret obtained from Red Hat OpenShift Cluster Manager at console.redhat.com/openshift/install/pull-secret.  # noqa: E501

        :return: The pull_secret of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: str
        """
        return self._pull_secret

    @pull_secret.setter
    def pull_secret(self, pull_secret):
        """Sets the pull_secret of this InfraEnvUpdateParams.

        The pull secret obtained from Red Hat OpenShift Cluster Manager at console.redhat.com/openshift/install/pull-secret.  # noqa: E501

        :param pull_secret: The pull_secret of this InfraEnvUpdateParams.  # noqa: E501
        :type: str
        """

        self._pull_secret = pull_secret

    @property
    def static_network_config(self):
        """Gets the static_network_config of this InfraEnvUpdateParams.  # noqa: E501


        :return: The static_network_config of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: list[HostStaticNetworkConfig]
        """
        return self._static_network_config

    @static_network_config.setter
    def static_network_config(self, static_network_config):
        """Sets the static_network_config of this InfraEnvUpdateParams.


        :param static_network_config: The static_network_config of this InfraEnvUpdateParams.  # noqa: E501
        :type: list[HostStaticNetworkConfig]
        """

        self._static_network_config = static_network_config

    @property
    def image_type(self):
        """Gets the image_type of this InfraEnvUpdateParams.  # noqa: E501


        :return: The image_type of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: ImageType
        """
        return self._image_type

    @image_type.setter
    def image_type(self, image_type):
        """Sets the image_type of this InfraEnvUpdateParams.


        :param image_type: The image_type of this InfraEnvUpdateParams.  # noqa: E501
        :type: ImageType
        """

        self._image_type = image_type

    @property
    def ignition_config_override(self):
        """Gets the ignition_config_override of this InfraEnvUpdateParams.  # noqa: E501

        JSON formatted string containing the user overrides for the initial ignition config.  # noqa: E501

        :return: The ignition_config_override of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: str
        """
        return self._ignition_config_override

    @ignition_config_override.setter
    def ignition_config_override(self, ignition_config_override):
        """Sets the ignition_config_override of this InfraEnvUpdateParams.

        JSON formatted string containing the user overrides for the initial ignition config.  # noqa: E501

        :param ignition_config_override: The ignition_config_override of this InfraEnvUpdateParams.  # noqa: E501
        :type: str
        """

        self._ignition_config_override = ignition_config_override

    @property
    def kernel_arguments(self):
        """Gets the kernel_arguments of this InfraEnvUpdateParams.  # noqa: E501


        :return: The kernel_arguments of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: KernelArguments
        """
        return self._kernel_arguments

    @kernel_arguments.setter
    def kernel_arguments(self, kernel_arguments):
        """Sets the kernel_arguments of this InfraEnvUpdateParams.


        :param kernel_arguments: The kernel_arguments of this InfraEnvUpdateParams.  # noqa: E501
        :type: KernelArguments
        """

        self._kernel_arguments = kernel_arguments

    @property
    def additional_trust_bundle(self):
        """Gets the additional_trust_bundle of this InfraEnvUpdateParams.  # noqa: E501

        Allows users to change the additional_trust_bundle infra-env field  # noqa: E501

        :return: The additional_trust_bundle of this InfraEnvUpdateParams.  # noqa: E501
        :rtype: str
        """
        return self._additional_trust_bundle

    @additional_trust_bundle.setter
    def additional_trust_bundle(self, additional_trust_bundle):
        """Sets the additional_trust_bundle of this InfraEnvUpdateParams.

        Allows users to change the additional_trust_bundle infra-env field  # noqa: E501

        :param additional_trust_bundle: The additional_trust_bundle of this InfraEnvUpdateParams.  # noqa: E501
        :type: str
        """

        self._additional_trust_bundle = additional_trust_bundle

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
        if issubclass(InfraEnvUpdateParams, dict):
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
        if not isinstance(other, InfraEnvUpdateParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
