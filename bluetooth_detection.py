import dbus

def proxyobj(bus, path, interface):
	obj = bus.get_object('org.bluez', path)
	return dbus.Interface(obj, interface)

def filter_by_interface(objects, interface_name):
	result = []
	for path in objects.keys():
		interfaces = objects[path]
		for interface in interfaces.keys():
			if interface == interface_name:
				result.append(path)
	return result
global count():
	bus = dbus.SystemBus()

	manager = proxyobj(bus, "/", "org.freedesktop.DBus.ObjectManager")
	objects = manager.GetManagedObjects()

	devices = filter_by_interface(objects, "org.bluez.Device1")

	bt_devices = []
	count = 0
	for device in devices:
		obj = proxyobj(bus, device, 'org.freedesktop.DBus.Properties')
	
		try:
			id = str(obj.Get("org.bluez.Device1", "Name"))
			bt_devices.append([
				id,
				str(obj.Get("org.bluez.Device1", "Address"))
				])
			if id == "HC-06": 
				count+=1
		except:
			bt_devices.append([0, str(obj.Get("org.bluez.Device1", "Address"))])
	

	#print bt_devices
	return count


#for device in devices:
#	print device
