[app]
title = Decentra-Network
package.name = decentra_network
package.domain = org.decentra_network
source.dir = decentra_network/
source.include_exts = py,png,jpg,kv,atlas
version = 0.25.0
orientation = all
fullscreen = 0
android.permissions = INTERNET
icon.filename = decentra_network/gui_lib/images/logo.ico
p4a.local_recipes = recipes/src/python-for-android/recipes/

[app@api]
title = Decentra-Network-API
package.name = decentra_network_api
source.dir = decentra_network/api/buildozer/
requirements =  decentra_network==0.25.0, Kivy==2.0.0, waitress==2.1.2, werkzeug==2.0.3, flask==2.0.0


[buildozer]
log_level = 2
warn_on_root = 1
