import appdaemon.appapi as appapi
import datetime

#
# App to manage house modes
#
# I manage my automations around the concept of a house mode. Using an automation to set a mode can then be used by other
# Apps to simplify state checking. For instance, if I set the mode to Evening at a certain light level, there is
# no easy way for another app to be sure if that event has occured in another app. To handle this
# I have defined an input_select called "house_mode". This app sets it to various values depending on the appropriate criteria.
# Othe apps can read it to figure out what they should do.
#
# Args:
#
# Since this code is very specific to my setup I haven't bothered with parameters.
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class Modes(appapi.AppDaemon):

  def initialize(self):
    
    # get current mode
    self.mode = self.get_state("input_select.house_mode")
    # Create some callbacks
    self.listen_event(self.mode_event, "MODE_CHANGE")
    self.listen_state(self.light_event, "sensor.side_multisensor_luminance_25")
    self.listen_state(self.motion_event, "binary_sensor.downstairs_sensor_26")
  
  def light_event(self, entity, attribute, old, new, kwargs):
    # Use light levels to switch to Day or Evening modes as appropriate
    lux = float(new)
    if self.mode == "Morning" or self.mode == "Night" and self.now_is_between("sunrise", "12:00:00"):
      if lux > 200:
        self.day()
        
    if self.mode == "Day" and self.now_is_between("sunset - 02:00:00", "sunset"):
      if lux < 200:
        self.evening()
  
  def motion_event(self, entity, attribute, old, new, kwargs):
    # Use motion form somoeone coming downstairs to trigger morning mode (switches on a downstairs lamp)
    if new == "on" and self.mode == "Night" and self.now_is_between("04:30:00", "10:00:00"):
      self.morning()

  def mode_event(self, event_name, data, kwargs):
    # Listen for a MODE_CHANGE custom event - triggered from a HASS script either manually or via Alexa
    # When event occurs switch to the appropriate mode
    mode = data["mode"]
    
    if mode == "Morning":
      self.morning()
    elif mode == "Day":
      self.day()
    elif mode == "Evening":
      self.evening()
    elif mode == "Night":
      self.night()
    elif mode == "Night Quiet":
      self.night(True)
  
  # Main mode functions - set the house up appropriately for the mode in question as well as set the house_mode flag corrcetly
  
  def morning(self):
    #Set the house up for morning
    self.mode = "Morning"
    self.log("Switching mode to Morning")
    self.call_service("input_select/select_option", entity_id="input_select.house_mode", option="Morning")
    self.turn_on("scene.wendys_lamp")
    self.notify("Switching mode to Morning")
    
  def day(self):
    # Set the house up for daytime
    self.mode = "Day"
    self.log("Switching mode to Day")
    self.call_service("input_select/select_option", entity_id="input_select.house_mode", option="Day")
    self.turn_on("scene.downstairs_off")
    self.turn_on("scene.upstairs_off")
    self.notify("Switching mode to Day")

  def evening(self):
    #Set the house up for evening
    self.mode = "Evening"
    self.log("Switching mode to Evening")
    self.call_service("input_select/select_option", entity_id="input_select.house_mode", option="Evening")
    if self.anyone_home():
      self.turn_on("scene.downstairs_on")
    else:
      self.turn_on("scene.downstairs_front")
      
    self.notify("Switching mode to Evening")

  def night(self, quiet = False):
    #Set the house up for evening
    #
    # Quiet flag just turns the downstairs off and does not turn on any upstairs lights to avoid
    # Waking up anyone sleeping
    #
    self.mode = "Night"
    self.log("Switching mode to Night")
    self.call_service("input_select/select_option", entity_id="input_select.house_mode", option="Night")
    
    if self.anyone_home() and not quiet:
      self.turn_on("scene.upstairs_hall_on")
    else:
      self.turn_on("scene.upstairs_hall_off")

    wendy = self.get_state("device_tracker.dedb5e711a24415baaae5cf8e880d852")
    andrew = self.get_state("device_tracker.5722a8985b4043e9b59305b5e4f71502")
    
    # Switch on correct bedside lights according to presence
    if not quiet:
      if self.everyone_home():
        self.turn_on("scene.bedroom_on")
      elif wendy == "home":
        self.turn_on("scene.bedroom_on_wendy")
      elif andrew == "home":
        self.turn_on("scene.bedroom_on_andrew")
              
    self.notify("Switching mode to Night")
    
    # We turned the upstairs lights on, wait 5 seconds before turning off the downstairs lights
    self.run_in(self.downstairs_off, 5)
      
  def downstairs_off(self, kwargs):
    # Timed callback
    self.turn_on("scene.downstairs_off")
      
    
