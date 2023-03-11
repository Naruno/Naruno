from naruno.apps.remote_app import Integration

from naruno.lib.settings_system import baklava_settings
baklava_settings(True)

integration = Integration("SamiName", password="password", host="localhost")

#integration.disable_cache()

#print(integration.get())

integration.send("action", "app_data", "cbdeeab5577f6f8693e571494e61dc0f356d9d09")
