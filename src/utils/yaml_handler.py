from pathlib import Path
from typing import Any, Dict, List

import yaml


class YamlHandler:
    def load(self, file_path: str) -> Dict[str, Any]:
        """Load YAML file"""
        try:
            with open(file_path, "r") as file:
                yaml_data = yaml.safe_load(file)
                return yaml_data if yaml_data is not None else {}
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
            return {}
        except yaml.YAMLError:
            print(f"Warning: Error parsing {file_path}")
            return {}

    def save(self, file_path: str, data: Dict[str, Any]) -> None:
        """Save YAML file"""
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as outfile:
            yaml.dump(
                data,
                outfile,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

    def load_with_override(
        self, base_path: str, override_paths: List[str]
    ) -> Dict[str, Any]:
        """
        Load base yaml and merge with specified override yamls

        Args:
            base_path: Path to base yaml file
            override_paths: List of paths to override yaml files

        Returns:
            Merged configuration dictionary
        """
        # Load base config
        base_config = self.load(base_path)

        # Load and merge override configs in order
        for override_path in override_paths:
            override_config = self.load(override_path)
            if isinstance(override_config, dict):
                self._deep_merge(base_config, override_config)

        return base_config

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """
        Recursively merge override dict into base dict

        Merge strategies:
        - proxies, rules: Prepend override items to base list
        - hosts: Check duplicates and merge if no duplicates
        - proxy-providers: Merge by name as dict
        - proxy-groups: Merge by name preserving order
        - nested dicts: Recursive merge
        - others: Replace base with override
        """
        for key, value in override.items():
            if key not in base:
                base[key] = value
                continue
            # Handle hosts merging with duplicate check
            if key == "hosts":
                # Find duplicate hosts
                duplicates = set(base[key].keys()) & set(value.keys())
                if duplicates:
                    print(
                        f"Warning: Duplicate hosts found: {duplicates}. Hosts merging skipped."
                    )
                    continue
                else:
                    # No duplicates found, merge the hosts
                    base[key].update(value)
                continue

            # Handle list prepending
            if key in ["proxies", "rules"]:
                self._merge_list_prepend(base, key, value)
                continue

            # Handle proxy provider merging
            if key == "proxy-providers":
                self._merge_proxy_providers(base, key, value)
                continue

            # Handle proxy groups merging
            if key == "proxy-groups":
                self._merge_proxy_groups(base, key, value)
                continue

            # Handle nested dictionary merging
            if isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
                continue

            # Default: replace base with override
            # 比如 hosts 字段
            base[key] = value

    def _merge_list_prepend(self, base: Dict[str, Any], key: str, value: Any) -> None:
        """Prepend override list to base list"""
        if not isinstance(base[key], list) or not isinstance(value, list):
            base[key] = value
            return

        if key == "proxies":
            # 创建一个现有代理名称的映射
            existing_proxies = {proxy["name"]: i for i, proxy in enumerate(base[key])}

            # 处理新的代理列表
            for proxy in value:
                if proxy["name"] in existing_proxies:
                    # 如果名称已存在,则用新配置覆盖原配置
                    base[key][existing_proxies[proxy["name"]]] = proxy
                else:
                    # 如果是新名称,则插入到列表开头
                    base[key].insert(0, proxy)
                    # 更新后续索引
                    for name, idx in existing_proxies.items():
                        existing_proxies[name] = idx + 1
                    existing_proxies[proxy["name"]] = 0
        else:
            # For other lists (like rules), just prepend
            base[key] = value + base[key]

    def _merge_proxy_providers(
        self, base: Dict[str, Any], key: str, value: Any
    ) -> None:
        """Merge proxy providers as dictionary"""
        if not isinstance(base[key], dict):
            base[key] = value
        else:
            base[key].update(value)

    def _merge_proxy_groups(self, base: Dict[str, Any], key: str, value: Any) -> None:
        """Merge proxy groups preserving order"""
        if not isinstance(base[key], list):
            base[key] = value
        else:
            existing = {g["name"]: i for i, g in enumerate(base[key])}
            for group in value:
                if group["name"] in existing:
                    # 更新已存在的组
                    base[key][existing[group["name"]]] = group
                else:
                    # 添加新组
                    base[key].append(group)
                    # 找到 "Proxy" 组并更新其 proxies 列表
                    for base_group in base[key]:
                        if base_group["name"] == "Proxy" and "proxies" in base_group:
                            if group["name"] not in base_group["proxies"]:
                                base_group["proxies"].append(group["name"])
