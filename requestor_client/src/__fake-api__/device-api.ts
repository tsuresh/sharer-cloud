import { subDays, subHours, subMinutes, subSeconds } from 'date-fns';
import type { Device } from '../types/device';

const now = new Date();

class DeviceApi {
  getDevices(): Promise<Device[]> {
    const requests: Device[] = [
      {
        id: '5e887ac47eed253091be10cb',
        name: "Device 1",
        machineType: "L2 DS",
        uptime: "10 H",
      },
      {
        id: '5e887ac47eed253091be10cb',
        name: "Device 2",
        machineType: "L2 DS",
        uptime: "10 H",
      },
      {
        id: '5e887ac47eed253091be10cb',
        name: "Device 3",
        machineType: "L2 DS",
        uptime: "10 H",
      }
    ];

    return Promise.resolve(requests);
  }

  getDevice(): Promise<Device> {
    const device: Device = {
        id: '5e887ac47eed253091be10cb',
        name: "Device 1",
        machineType: "L2 DS",
        uptime: "10 H",
      };

    return Promise.resolve(device);
  }

}

export const deviceApi = new DeviceApi();
