import os
import time

import PIL

# Import PyhtonNet
import clr
from PIL import Image
from PIL import ImageDraw

clr.AddReference('TIS.Imaging.ICImagingControl35')
clr.AddReference('System')

# Import the IC Imaging Control namespace.
import TIS.Imaging
from System import TimeSpan


class Camera:
    def __init__(self, plotter, sample_rate=0.01):
        self.sample_rate = sample_rate
        self.ic = TIS.Imaging.ICImagingControl()
        self.plotter = plotter

        # Create the sink for snapping images on demand.
        self.snapsink = TIS.Imaging.FrameSnapSink(TIS.Imaging.MediaSubtypes.RGB32)
        self.ic.Sink = self.snapsink

        self.cam_on = False

    def configure_camera(self):
        os.system('py CameraConfiguration.py')

    def repeated_snap_save(self, directory):
        self.ic.LiveDisplay = True
        self.cam_on = True

        # Try to open the last used video capture device.
        try:
            self.ic.LoadDeviceStateFromFile("device.xml", True)
            if self.ic.DeviceValid is True:
                self.ic.LiveStart()

        except Exception as ex:
            self.ic.ShowDeviceSettingsDialog()
            if self.ic.DeviceValid is True:
                self.ic.SaveDeviceStateToFile("device.xml")
                self.ic.LiveStart()
            pass

        os.chdir(directory)
        if not os.path.isdir(directory + "/CAM"):
            os.mkdir(directory + "/CAM")

        img_num = 0
        if directory != "":
            while self.cam_on:
                frame = self.snapsink.SnapSingle(TimeSpan.FromSeconds(5))
                frame_name = "CAM/image0" + str(img_num) + ".jpg"
                img_num += 1
                # Save the frame as JPG with 75% quality.
                TIS.Imaging.FrameExtensions.SaveAsJpeg(frame, frame_name, 100)
                img = Image.open(frame_name)
                # Call draw Method to add 2D graphics in an image
                I1 = ImageDraw.Draw(img)

                text = "true_amplitude = " + str(self.plotter.get_current_amplitudes()) + ", true_time = " + str(self.plotter.get_current_time())
                # Add Text to an image
                I1.text((28, 36), text, fill=(255, 0, 0))

                # Save the edited image
                img.save(frame_name)
                time.sleep(0.1)

        self.ic.LiveDisplay = False
        self.ic.LiveStop()
        self.ic.Dispose()
