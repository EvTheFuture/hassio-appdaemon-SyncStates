Sync States
===========

_Synchronize states of switches and lights that doesn't have read back i e TellStick devices_

Ever got frustrated when you have more than one switch to control a light, the state is not updated on the light for all switches used?

This [AppDaemon](https://appdaemon.readthedocs.io/en/latest/#) app for [Home Assistant](https://www.home-assistant.io/) try to fix that by updating the state of the light and or switches.

[![buy-me-a-coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/EvTheFuture)

## Quick Examples

Here is an example configuration for the appdaemon configuration file apps.yaml.

**Please Note:** You need to change the entities to match your setup.
```
sync_hallway_light:
  module: sync_states
  class: SyncStates
  entity: light.hallway
  switches: 
    - switch.hallway2
    - switch.hallway3  
    - switch.hallway4
    - switch.hallway5
    - switch.hallway6
    - switch.hallway7
  debug: no
```
