# Copyright 2022 DevGuyAhnaf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import Dict, List
from .service import Instance, Service


class RegistryCache:
    """An internal caching mechanism for storing registry data in memory"""

    def __init__(self):
        self.state: Dict[str, Service] = {}

    def set(self, services: List[dict]):
        """Resets the cache and sets new data"""
        service_names = [i["name"] for i in services]

        state_data = (
            {}.update(self.state) or {}
        )  # So that there's no runtimeerror dict changed size during iter
        for x in state_data:
            # Removing the services which do not exist anymore
            if x not in service_names:
                self.state.pop(x)

        for i in services:
            instances = [Instance(**x) for x in i["instances"]]
            new_service = Service(i["name"], instances)

            # Setting the last instance index so that it can load balance properly
            if i["name"] in self.state:
                new_service._last_instance_index = self.state[
                    i["name"]
                ]._last_instance_index
            self.state[new_service.name.lower()] = new_service

    def get(self, service_name: str):
        return self.state.get(service_name.lower())
