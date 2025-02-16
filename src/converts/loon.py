from src.converts.base import Base


class Loon(Base):
    def convert(self) -> None:
        """Convert to a loon configuration"""
        self.data = self.yaml_handler.load_with_override(
            "config/base.yaml",
            [
                "config/override/private_proxy_provider.yaml",
                "config/override/backhome_proxy.yaml",
            ],
        )

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

    def _get_rules(self) -> list:
        # 先调用父类的方法获取原始的 rules
        rules = super()._get_rules()

        # 替换 backhome 为 GOHOME
        new_rules = []
        for rule in rules:
            if "backhome" in rule:
                new_rules.append(rule.replace("backhome", "GOHOME"))
            else:
                new_rules.append(rule)

        return new_rules

    def _get_proxy_groups(self) -> list:
        # 先获取原始的代理组
        proxy_groups = super()._get_proxy_groups()

        # 检查是否存在 backhome 代理
        proxies = self._get_proxies()
        has_backhome = any(proxy["name"] == "backhome" for proxy in proxies)

        # 如果存在 backhome，添加 GOHOME 组
        if has_backhome:
            gohome_group = {
                "name": "GOHOME",
                "type": "ssid",
                "ssid_setting": 'ssid,default=backhome,cellular=backhome,"2"=DIRECT,"5"=DIRECT,"5_EXT"=DIRECT',
                "url": "http://cp.cloudflare.com/generate_204",
                "icon": "homekit",
            }
            proxy_groups.append(gohome_group)

            # 将 GOHOME 添加到 Proxy 组的 proxies 中
            for group in proxy_groups:
                if group["name"] == "Proxy":
                    if "proxies" not in group:
                        group["proxies"] = []
                    group["proxies"].append("GOHOME")
                    break

        return proxy_groups
