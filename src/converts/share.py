from src.converts.base import Base
from src.converts.loon import Loon


class ShareMihomo(Base):
    def convert(self) -> None:
        """Convert to a shared configuration"""
        self._load_yaml()
        self._update_settings()
        self._save_yaml()


class ShareLoon(Loon):
    def convert(self) -> None:
        """Convert mihomo configuration to Loon format"""
        self._load_yaml()

        self.template_data = {
            "proxy_providers": self._get_proxy_providers(),
            "proxy_groups": self._get_proxy_groups(),
            "proxies": self._get_proxies(),
            "rule_providers": self._get_rule_providers(),
            "rules": self._get_rules(),
            "hosts": self._get_hosts(),
        }

        output = self.template_handler.render("loon.conf", self.template_data)
        self.template_handler.save(self.output_file, output)
