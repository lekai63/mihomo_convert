from src.converts.base import Base


class Router(Base):
    def convert(self) -> None:
        """Convert to a router configuration"""
        self.data = self.yaml_handler.load_with_override(
            "config/base.yaml",
            [
                "config/override/private_proxy_provider.yaml",
                "config/override/router.yaml",
            ],
        )
        self._update_settings()
        self._save_yaml()


class Client(Base):
    def convert(self) -> None:
        """Convert to a router configuration"""
        self.data = self.yaml_handler.load_with_override(
            "config/base.yaml",
            [
                "config/override/private_proxy_provider.yaml",
                "config/override/backhome_proxy.yaml",
            ],
        )
        self._update_settings()
        self._save_yaml()
