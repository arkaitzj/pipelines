# Copyright 2021-2022 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Functions for loading components from compiled YAML."""

from typing import Optional, Tuple

from kfp import components
from kfp.components import structures
import requests


class YamlComponent(components.BaseComponent):
    """A component loaded from a YAML file.

    **Note:** ``YamlComponent`` is not intended to be used to construct components directly. Use ``kfp.components.load_component_from_*()`` instead.

    Args:
        component_spec: Component definition.
    """

    def execute(self, *args, **kwargs):
        """Not implemented."""
        raise NotImplementedError


def load_component_from_text(text: str) -> YamlComponent:
    """Loads a component from text.

    Args:
        text (str): Component YAML text.

    Returns:
        Component loaded from YAML.
    """
    return YamlComponent(
        structures.ComponentSpec.load_from_component_yaml(text))


def load_component_from_file(file_path: str) -> YamlComponent:
    """Loads a component from a file.

    Args:
        file_path (str): Filepath to a YAML component.

    Returns:
        Component loaded from YAML.

    Example:
      ::

        from kfp import components

        components.load_component_from_file('~/path/to/pipeline.yaml')
    """
    with open(file_path, 'r') as component_stream:
        return load_component_from_text(component_stream.read())


def load_component_from_url(url: str,
                            auth: Optional[Tuple[str,
                                                 str]] = None) -> YamlComponent:
    """Loads a component from a URL.

    Args:
        url (str): URL to a YAML component.
        auth (Tuple[str, str], optional): A ``('<username>', '<password>')`` tuple of authentication credentials necessary for URL access. See `Requests Authorization <https://requests.readthedocs.io/en/latest/user/authentication/#authentication>`_ for more information.

    Returns:
        Component loaded from YAML.

    Example:
      ::

        from kfp import components

        components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/7b49eadf621a9054e1f1315c86f95fb8cf8c17c3/sdk/python/kfp/compiler/test_data/components/identity.yaml')

        components.load_component_from_url('gs://path/to/pipeline.yaml')
    """
    if url is None:
        raise ValueError('url must be a string.')

    if url.startswith('gs://'):
        #Replacing the gs:// URI with https:// URI (works for public objects)
        url = 'https://storage.googleapis.com/' + url[len('gs://'):]

    resp = requests.get(url, auth=auth)
    resp.raise_for_status()

    return load_component_from_text(resp.content.decode('utf-8'))
