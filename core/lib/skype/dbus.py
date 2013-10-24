#!/usr/bin/env python
#Read more: http://atamanenko.blogspot.com/2010/03/skype-d-bus-python.html#ixzz1dlFrT5Uv
import dbus, sys

def connect():
    remote_bus = dbus.SessionBus()

    # Check if skype is running.
    system_service_list = remote_bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus').ListNames()
    skype_api_found = 0
    for service in system_service_list:
        if service=='com.Skype.API':
            skype_api_found = 1
            break
    if not skype_api_found:
        sys.exit('No running API-capable Skype found')

    # Get skype dbus api
    skype_service = remote_bus.get_object('com.Skype.API', '/com/Skype')

    # Connect to skype.
    answer = skype_service.Invoke('NAME SkypeApiClient')
    if answer != 'OK':
        sys.exit('Could not bind to Skype client')

    # Check if protocol is supported.
    answer = skype_service.Invoke('PROTOCOL 1')
    if answer != 'PROTOCOL 1':
        sys.exit('This test program only supports Skype API protocol version 1')

    # Invoke operations
    for arg in sys.argv:
        skype_service.Invoke(arg)

    return 0

if __name__ == "__main__":
    main()


