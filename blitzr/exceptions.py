class ConfigurationException(IOError):
    """There is a problem with your configuration, check your Blitzr API Key."""

class NetworkException(IOError):
    """A network problem occured, try again."""

class ClientException(IOError):
    """You just sent a bad request."""

class ServerException(IOError):
    """An error occured on the Blitzr side, try again."""
