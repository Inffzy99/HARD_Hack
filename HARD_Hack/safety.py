import dbus
import cv2
import numpy
ped_detector = cv2.CascadeClassifier('hogcascade_pedestrians.xml')
fac_detector = cv2.CascadeClassifier('haarcascade_upperbody.xml')

bluetooth_id = "HC-06"

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

#collect the bluetooth devices
#	majority of code taken from: https://stackoverflow.com/questions/14262315/list-nearby-discoverable-bl#	     uetooth-devices-including-already-paired-in-python
def count():
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
                        if id == bluetooth_id:
                                count+=1
                except:
                        bt_devices.append([0, str(obj.Get("org.bluez.Device1", "Address"))])


       	return count

# collect + count humans present w/ opencv image processing &
#	combines data w/ count() & return the number of strangers present
def main():
        windowName = "LIve Video Feed"
        cv2.namedWindow(windowName)
        cap = cv2.VideoCapture(0)

        cap.set(3, 400)
        cap.set(4, 300)

        if cap.isOpened():
                ret, frame = cap.read()
        else:
                ret = False

        body_average = 0
        face_average = 0
        body_sqsum = 0
        face_sqsum = 0
        loopdiv = 0
        clock = 0
        
# majority of the following OpenCV code was taken from: https://youtu.be/ktm06xnXWcY

        while ret:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                body = ped_detector.detectMultiScale(gray, 3, 2)
                face = fac_detector.detectMultiScale(gray, 2, 3)

                for (x, y, w, h) in body:
                        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        #print("a" + str(len(body)))
                
		for (x, y, w, h) in face:
                        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
		body_sqsum += len(body)
                face_sqsum += len(face)
                
		if clock%3 == 0:
                        body_average = round(body_sqsum / 3.0)
                        face_average = round(face_sqsum / 3.0)
			
			print("\nNumber of people present: " + str(body_average + face_average))
                        print("Body: " + str(body_average))
                        print("Face: " + str(face_average))
			
                        loopdiv = 0
                        body_sqsum = 0
                        face_sqsum = 0
			print("Number of students: " + str(count()))

			num_strange = body_average + face_average - count()

			if num_strange < 0: 
				print("Student ID in range, but image not detected by camera.")

			else:
                        	print("Number of strangers: " + str(num_strange))
			
                cv2.imshow(windowName, gray)
                
		if cv2.waitKey(1) == 27:
                        break

                loopdiv += 1
                clock += 1
        cv2.destroyWindow(windowName)

        cap.release()

if __name__ == "__main__":
        main()
