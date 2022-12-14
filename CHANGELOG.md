pympv
=====

## 0.8.0
- Update to libmpv API 2.0, removing previously deprecated APIs
- Optimise string conversion functions with Cython
- Give str its Python 3 meaning
- Simplify string conversions, since python2 is no more

## 0.7.1
- Extract examples into its own directory

## 0.6.0
- Add support for the render API
- Deprecate the legacy opengl-cb API

## 0.5.1
- Rename async -> asynchronous for Python 3.7 compatibility
- Force Cython rebuilds if Cython is installed

## 0.4.1

- Prepare packaging for PyPI

## 0.4.0
- Fix string support in Python2
- Add opengl-cb support
- Improve packaging/setup.py

## 0.3.0

- Fix various failures of data and callbacks
- Sync up header with new errors from 1.11
- Add shutdown() to cleanup a context, GCing the context calls this
- Callbacks and data are no longer associated weakly
- Async data and observe property system changed to be hash() based

## 0.2.1

- Fix possible failures setting property to a map
- Fix possible failures with every single string


## 0.2

- EOFReasons.restart removed to reflect client.h enum
- Bump to require libmpv 1.9
- Switch mpv.command() to use mpv_command_node, non-async will now return comamnd response data.
  This should make no difference to users, but now accepts various forms of data instead of just strings.
- Add try_get_property_async and try_get_property
- Add support for EndOfFileReached.error and EOFReasons.error
- Add support for LogMessage.log_level and LogLevels
- Fix Errors values being positive rather than negative (And totally wrong as a result)
- Add a few new Errors values
- Add support for setting properties, options, and commands to lists and maps
