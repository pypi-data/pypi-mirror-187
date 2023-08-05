import logging
__version__ = 2.1 
adapter_logger = logging.getLogger(__file__)
from .implementation import ArgparserAdapter, CommandLine, Choice,ChoiceCommand
