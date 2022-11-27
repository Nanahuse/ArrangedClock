# Copyright (c) 2022 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ArrangedClock/blob/main/LICENSE

import obspython as obs
from typing import Any


def set_source_list(propery_list: Any, source_id_list: set[str]):
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id in source_id_list:
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(propery_list, name, name)
    obs.source_list_release(sources)
    return
