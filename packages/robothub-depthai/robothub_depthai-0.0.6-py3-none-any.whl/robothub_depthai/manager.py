import logging as log
import os
import contextlib
import time
from typing import List

import robothub
from robothub import RobotHubApplication

from robothub_depthai.hub_camera import HubCamera

__all__ = ['HubCameraManager']


class NoDevicesException(Exception):
    pass


class HubCameraManager:
    """
    A manager class to handle multiple HubCamera instances.
    """
    REPORT_FREQUENCY = 10  # seconds
    POLL_FREQUENCY = 0.002

    def __init__(self, app: RobotHubApplication, devices: List[dict]):
        """
        :param app: The RobotHubApplication instance.
        :param devices: A list of devices to be managed.
        """
        self.hub_cameras = [HubCamera(app, device_mxid=device.oak['serialNumber'], id=i)
                            for i, device in enumerate(devices)]
        self.app = app

        self.reporting_thread = robothub.threading.Thread(target=self._report, name='ReportingThread', daemon=False)
        self.polling_thread = robothub.threading.Thread(target=self._poll, name='PollingThread', daemon=False)

    def __exit__(self):
        self.stop()

    def start(self) -> None:
        """
        Start the cameras, start reporting and polling threads.
        """
        if not self.hub_cameras:
            # Endless loop to prevent app from exiting if no devices are found
            while True:
                self.app.wait(1)


        print('Starting cameras...')
        for camera in self.hub_cameras:
            camera.start()

        print('Starting reporting thread...')
        self.reporting_thread.start()
        print('Reporting thread started successfully')

        print('Starting polling thread...')
        self.polling_thread.start()
        print('Polling thread started successfully')

        print('Cameras started successfully')

    def stop(self) -> None:
        """
        Stop the cameras, stop reporting and polling threads.
        """
        log.debug('Gracefully stopping threads...')
        self.app.stop_event.set()

        try:
            self.reporting_thread.join():
        except BaseException as e:
            log.error(f'self.reporting_thread join excepted with: {e}')
            
        try:
            self.polling_thread.join():
        except BaseException as e:
            log.error(f'self.polling_thread join excepted with: {e}')

        try:
            robothub.STREAMS.destroy_all_streams()
        except BaseException as e:
            raise Exception(f'Destroy all streams excepted with: {e}')

        for camera in self.hub_cameras:
            try:
                if camera.state != robothub.DeviceState.DISCONNECTED:
                    with open(os.devnull, 'w') as devnull:
                        with contextlib.redirect_stdout(devnull):
                            camera.oak_camera.__exit__(Exception, 'Device disconnected - app shutting down', None)
            except BaseException as e:
                raise Exception(f'Could not exit device with error: {e}')

        print('App stopped successfully')

    def _report(self) -> None:
        """
        Reports the state of the cameras to the agent. Active when app is running, inactive when app is stopped.
        Reporting frequency is defined by REPORT_FREQUENCY.
        """
        while self.app.running:
            for camera in self.hub_cameras:
                device_info = camera.info_report()
                device_stats = camera.stats_report()

                robothub.AGENT.publish_device_info(device_info)
                robothub.AGENT.publish_device_stats(device_stats)

            time.sleep(self.REPORT_FREQUENCY)

    def _poll(self) -> None:
        """
        Polls the cameras for new detections. Polling frequency is defined by POLL_FREQUENCY.
        """
        is_connected = True
        while self.app.running and is_connected:
            for camera in self.hub_cameras:
                camera.poll()
                if not camera.is_connected:
                    print(f'Camera {camera.id} disconnected. '
                          f'Please check if the device is connected and restart the application.')
                    is_connected = False

            time.sleep(self.POLL_FREQUENCY)
