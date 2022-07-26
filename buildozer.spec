[app]
title = Decentra-Network
package.name = decentra_network
package.domain = com.example
source.dir = decentra_network/
source.include_exts = py,png,jpg,kv,atlas
version = 0.25.0
orientation = all
fullscreen = 0
android.permissions = INTERNET
icon.filename = decentra_network/gui_lib/images/logo.ico


[app@api]
title = Decentra-Network-API
source.dir = decentra_network/api/
requirements = flask==2.0.0, waitress==2.1.2, werkzeug==2.0.3


[buildozer]
log_level = 1
warn_on_root = 1