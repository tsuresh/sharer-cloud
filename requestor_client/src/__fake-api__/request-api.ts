import axios, { AxiosResponse } from 'axios';
import { subDays, subHours, subMinutes, subSeconds } from 'date-fns';
import type { Request } from '../types/request';

const now = new Date();

class RequestApi {
  getRequests(): Promise<Request[]> {
    let requests: Request[] = [];
    let axios = require('axios');
    const config = {
      method: 'get',
      url: 'http://localhost:5000/getWorkloads',
      headers: { }
    };
    return new Promise((resolve, reject) => {
      axios(config)
        .then(function (response: AxiosResponse<Request[]>) {
          resolve(response.data);
        })
        .catch(function (error:any) {
          reject(requests);
        });
    });
  }

  // getRequest(): Promise<Request> {
  //   const request: Request = {
  //     id: '6e887ac47eed253091be10cb',
  //     name: "Test workload 2",
  //     machineType: "L2 DS",
  //     image: "test image",
  //     status: "complete"
  //   };

  //   return Promise.resolve(request);
  // }

}

export const requestApi = new RequestApi();
