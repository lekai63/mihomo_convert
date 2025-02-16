from typing import Any, Dict

from src.utils.template_handler import TemplateHandler
from src.utils.yaml_handler import YamlHandler


class Base:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.data: Dict[str, Any] = {}
        self.yaml_handler = YamlHandler()
        self.template_handler = TemplateHandler()

    def _load_yaml(self) -> None:
        """Load YAML file"""
        self.data = self.yaml_handler.load(self.input_file)

    def _save_yaml(self) -> None:
        """Save YAML file"""
        self.yaml_handler.save(self.output_file, self.data)

    def _update_settings(self) -> None:
        """Update general settings"""
        if not isinstance(self.data, dict):
            return
        if "find-process-mode" in self.data and self.data["find-process-mode"] is False:
            self.data["find-process-mode"] = "off"

    def _get_proxy_providers(self) -> list:
        providers = []
        for name, config in self.data.get("proxy-providers", {}).items():
            providers.append(
                {
                    "name": name,
                    "url": config.get("url", ""),
                }
            )
        return providers

    def _get_proxy_groups(self) -> list:
        groups = []
        for group in self.data.get("proxy-groups", []):
            if isinstance(group, dict):
                groups.append(group)
        return groups

    def _get_proxies(self) -> list:
        """Extract proxy configurations from YAML data

        Returns:
            list: List of proxy configurations, where each proxy is a dict containing
                name and other configuration details
        """
        proxies = []
        for proxy in self.data.get("proxies", []):
            if isinstance(proxy, dict):
                proxies.append(proxy)
        return proxies

    def _get_rule_providers(self) -> list:
        providers = []
        rule_set_policies = self._extract_rule_set_policies()

        for name, config in self.data.get("rule-providers", {}).items():
            providers.append(
                {
                    "name": name,
                    "url": config.get("url", ""),
                    "path": config.get("path", ""),
                    "policy": rule_set_policies.get(name, "Proxy"),
                }
            )
        return providers

    def _extract_rule_set_policies(self) -> dict:
        policies = {}
        for rule in self.data.get("rules", []):
            if isinstance(rule, str) and rule.startswith("RULE-SET"):
                parts = rule.split(",")
                if len(parts) == 3:
                    policies[parts[1]] = parts[2]
        return policies

    def _get_rules(self) -> list:
        return self.data.get("rules", [])

    def _get_hosts(self) -> list:
        return self.data.get("hosts", [])
