import axios, { AxiosResponse } from 'axios';
import { subDays, subHours, subMinutes, subSeconds } from 'date-fns';
import type { Request, RequestResponse } from '../types/request';

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

  getRequest(workload_id: string): Promise<Request> {
    let requests: Request[] = [];
    let axios = require('axios');
    const config = {
      method: 'get',
      url: 'http://localhost:5000/getWorkloadDetail?id='+workload_id,
      headers: { }
    };
    return new Promise((resolve, reject) => {
      axios(config)
        .then(function (response: AxiosResponse<Request>) {
          resolve(response.data);
        })
        .catch(function (error:any) {
          reject(requests);
        });
    });
  }

  getResponses(workload_id: string): Promise<RequestResponse[]> {
    let requests: RequestResponse[] = [];
    let axios = require('axios');
    const config = {
      method: 'get',
      url: 'http://localhost:5000/getWorkloadResponses?id='+workload_id,
      headers: { }
    };
    return new Promise((resolve, reject) => {
      axios(config)
        .then(function (response: AxiosResponse<RequestResponse[]>) {
          resolve(response.data);
        })
        .catch(function (error:any) {
          reject(requests);
        });
    });
  }

}

export const requestApi = new RequestApi();
