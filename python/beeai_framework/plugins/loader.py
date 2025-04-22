# Copyright 2025 © BeeAI a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any

from beeai_framework.plugins.types import PluggableFactory, PluggableRegistry


class PluginLoader:
        def __init__(self, *, registry: PluggableFactory | None = None) -> None:
            self.factories = registry or PluggableFactory()
            self.instances = PluggableRegistry()

        def load(self, /, config: dict[str, Any]) -> None:
            for name, options in config.items():
                plugin_name = options["plugin"]
                if not isinstance(plugin_name, str):
                    raise ValueError(f"Plugin name must be a string, got {type(plugin_name)}")

                plugin_parameters = options.get("parameters", {})
                if not isinstance(plugin_parameters, dict):
                    raise ValueError(f"Plugin parameters must be a dict, got {type(plugin_parameters)}")

                instance = self.factories.create(plugin_name, **self._parse_plugin_parameters(plugin_parameters))
                self.instances.register(instance, name=name)

        def _parse_plugin_parameters(self, /, input: Any) -> Any:
            if isinstance(input, dict):
                return {key: self._parse_plugin_parameters(value) for key, value in input.items()}
            elif isinstance(input, list):
                return [self._parse_plugin_parameters(item) for item in input]

            if isinstance(input, str) and input.startswith("#"):
                return self.instances.lookup(input[1:]).ref
            else:
                return input
