import axios, { AxiosResponse } from 'axios';
import { subDays, subHours, subMinutes, subSeconds } from 'date-fns';
import type { Device } from '../types/device';

const now = new Date();

class DeviceApi {
  getDevices(): Promise<Device[]> {
    const requests: Device[] = [];
    let axios = require('axios');
    const config = {
      method: 'get',
      url: 'http://localhost:5000/getNetwork',
      headers: { }
    };
    return new Promise((resolve, reject) => {
      axios(config)
        .then(function (response: AxiosResponse<Device[]>) {
          resolve(response.data);
        })
        .catch(function (error:any) {
          reject(requests);
        });
    });
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
