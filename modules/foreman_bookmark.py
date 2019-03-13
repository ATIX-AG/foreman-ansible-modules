#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2019 Bernhard Hopfenmüller (ATIX AG)
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from ansible.module_utils.foreman_helper import ForemanEntityAnsibleModule
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: foreman_bookmark
short_description: Manage Foreman Bookmarks
description:
  - "Manage Foreman Bookmark Entities"
  - "Uses https://github.com/SatelliteQE/nailgun"
version_added: "2.4"
author:
  - "Bernhard Hopfenmueller (@Fobhep) ATIX AG"
  - "Matthias Dellweg (@mdellweg) ATIX AG"
requirements:
  - "nailgun >= 0.29.0"
  - "ansible >= 2.3"
options:
  server_url:
    description:
      - URL of Foreman server
    required: true
  username:
    description:
      - Username on Foreman server
    required: true
  password:
    description:
      - Password for user accessing Foreman server
    required: true
  verify_ssl:
    description:
      - Verify SSL of the Foreman server
    required: false
    default: true
    type: bool
  name:
    description:
      - Name of the Bookmark
    required: true
  controller:
    description:
      - Controller for the Bookmark
    required: false
  query:
    description:
      - Query of the Bookmark
  public:
    description:
      - Make Bookmark public
    required: false
    default: true
    type: bool
  state:
    description:
      - State of the Bookmark
    default: present
    choices:
      - present
      - present_with_defaults
      - absent
'''

EXAMPLES = '''
- name: "Create a Bookmark"
  foreman_bookmark:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "recent"
    controller: "job_invocations"
    query: "started_at > '24 hours ago'"
    state: present_with_defaults

- name: "Update a Bookmark"
  foreman_bookmark:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "recent"
    controller: "job_invocations"
    query: "started_at > '12 hours ago'"
    state: present

- name: "Delete a Bookmark"
  foreman_bookmark:
    username: "admin"
    password: "changeme"
    server_url: "https://foreman.example.com"
    name: "recent"
    state: absent
'''

RETURN = ''' # '''

try:
    from nailgun.entities import (
        Bookmark,
    )

    from ansible.module_utils.ansible_nailgun_cement import (
        find_bookmark,
        naildown_entity_state,
        sanitize_entity_dict,
    )
except ImportError:
    pass


# This is the only true source for names (and conversions thereof)
name_map = {
    'name': 'name',
    'controller': 'controller',
    'query': 'query',
    'public': 'public',
}


def main():
    module = ForemanEntityAnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            controller=dict(),
            query=dict(),
            public=dict(defaut='true', type='bool'),
            state=dict(default='present', choices=[
                       'present_with_defaults', 'present', 'absent']),
        ),
        required_if=(
            ['state', 'present_with_defaults', ['query', 'controller']],
        ),
        supports_check_mode=True,
    )

    (bookmark_dict, state) = module.parse_params()

    module.connect()

    entity = find_bookmark(module, bookmark_dict['name'], bookmark_dict['controller'], failsafe=True)

    bookmark_dict = sanitize_entity_dict(bookmark_dict, name_map)

    changed = naildown_entity_state(
        Bookmark, bookmark_dict, entity, state, module)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
