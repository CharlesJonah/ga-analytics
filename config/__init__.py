from .production import ProductionConfig
from .development import DevelopmentConfig
from .staging import StagingConfig

config = {
    "production": ProductionConfig,
    "staging": StagingConfig,
    "development": DevelopmentConfig,
}
