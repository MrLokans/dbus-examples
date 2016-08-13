import dbus
from dbus.mainloop.glib import DBusGMainLoop


def dbus_obj_to_python_repr(dbus_object):
    import json
    return json.dumps(dbus_object, indent=2)


def device_mounted(sender, *args):
    print "-" * 20
    for arg in args:
        if "org.freedesktop.UDisks2.Job" in arg:
            job = arg["org.freedesktop.UDisks2.Job"]
            if "Operation" in job and job["Operation"] == "filesystem-unmount":
                objects = job["Objects"]
                print("Attemting to unmount {}".format(objects[0]))
            else:
                pass
    # print "ARG => \n{}".format(dbus_obj_to_python_repr(arg))

if __name__ == '__main__':
    # SystemBus is used to communicate with system services (like udev)
    DBusGMainLoop(set_as_default=True)
    system_bus = dbus.SystemBus()

    iface = 'org.freedesktop.DBus.ObjectManager'
    signal = 'InterfacesAdded'

    system_bus.add_signal_receiver(device_mounted, signal, iface)

    import gobject
    loop = gobject.MainLoop()
    loop.run()
