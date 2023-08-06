from extras.plugins import PluginConfig


class Portmanager(PluginConfig):
    name = "netbox_portmanager"
    verbose_name = "Portmanager"
    description = "Plugin for ports managing"
    version = "0.3"
    author = "Michal Drobný"
    author_email = "drobny@ics.muni.cz"
    base_url = "netbox-portmanager"
    min_version = "3.3"
    required_settings = []
    default_settings = {
        "static_image_directory": "netbox_portmanager/img",
    }


config = Portmanager
