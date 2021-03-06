=======
History
=======

1.3.2 (2016-09-06)
------------------

**Features**

- Document "Time Travel" functionality
- Add convenience function to set input_select called `select_option()` - contributed by [jbardi](https://community.home-assistant.io/users/jbardi/activity)
- Add global access to configuration and global configuration variables - suggested by [ReneTode](https://community.home-assistant.io/users/renetode/activity) 

**Fixes**

- Tidy up examples for listen state - suggested by [ReneTode](https://community.home-assistant.io/users/renetode/activity)
- Warning when setting state for a non-existent entity is now only given the first time
- Allow operation with no `ha_key` specified
- AppDaemon will now use the supplied timezone for all operations rather than just for calculating sunrise and sunset
- Reduce the chance of a spurious Clock Skew error at startup

**Breaking Changes**

None

1.3.1 (2016-09-04)
------------------

**Features**

- Add convenience function to set input_selector called `select_value()` - contributed by [Dave Banks](https://github.com/djbanks)

**Fixes**

None

**Breaking Changes**

None

1.3.0 (2016-09-04)
------------------

**Features**

- Add ability to randomize times in scheduler
- Add `duration` to listen_state() to fire event when a state condition has been met for a period of time
- Rewrite scheduler to allow time travel (for testing purposes only, no effect on regular usage!)
- Allow input_boolean constraints to have reversed logic
- Add info_listen_state(), info_listen_event() and info_schedule() calls

**Fixes**

- Thorough proofreading correcting typos and formatting of API.md - contributed by [Robin Lauren](https://github.com/llauren)
- Fixed a bug that was causing scheduled events to fire a second late
- Fixed a bug in `get_app()` that caused it to return a dict instead of an object
- Fixed an error when missing state right after HA restart

**Breaking Changes**

- `run_at_sunrise(`) and `run_at_sunset()` no longer take a fixed offset parameter, it is now a keyword, e.g. `offset = 60`


1.2.2 (2016-31-09)
------------------

**Features**

None

**Fixes**

- Fixed a bug preventing get_state() calls for device types
- Fixed a bug that would cause an error in the last minute of an hour or last hour of a day in run_minutely() and run)hourly() respectively

**Breaking Changes**

None

1.2.1 (2016-26-09)
------------------

**Features**

- Add support for windows

**Fixes**

None

**Breaking Changes**

None


1.2.0 (2016-24-09)
------------------

**Features**

- Add support for recursive directories - suggested by [jbardi](https://github.com/jbardi)

**Fixes**

None

**Breaking Changes**

None

1.1.1 (2016-23-09)
------------------

**Fixes**

- Fix init scripts

1.1.0 (2016-21-09)
------------------

**Features**

- Installation via pip3 - contributed by [Martin Hjelmare](https://github.com/MartinHjelmare)
- Docker support (non Raspbian only) - contributed by [Jesse Newland](https://github.com/jnewland)
- Allow use of STDERR and SDTOUT as logfile paths to redirect to stdout and stderr respectively - contributed by [Jason Hite](https://github.com/jasonmhite)
- Deprecated "timezone" directive on cfg file in favor of "time_zone" for consistency with Home Assistant config
- Added default paths for config file and apps directory
- Log and error files default to STDOUT and STDERR respectively if not specified
- Added systemd service file - contributed by [Jason Hite](https://github.com/jasonmhite)

**Fixes**

- Fix to give more information if initial connect to HA fails (but still avoid spamming logs too badly if it restarts)
- Rename 'init' directory to 'scripts'
- Tidy up docs

**Breaking Changes**

- As a result of the repackaging for PIP3 installation, all apps must be edited to change the import statement of the api to `import appdaemon.appapi as appapi`
- Config must now be explicitly specfied with the -c option if you don't want it to pick a default file location
- Logfile will no longer implicitly redirect to STDOUT if running without the -d flag, instead specify STDOUT in the config file or remove the logfile directive entirely
- timezone is deprecated in favor of time_zone but still works for now

1.0.0 (2016-08-09)
------------------

**Initial Release**
