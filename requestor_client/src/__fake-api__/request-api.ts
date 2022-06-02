import { subDays, subHours, subMinutes, subSeconds } from 'date-fns';
import type { Request } from '../types/request';

const now = new Date();

class RequestApi {
  getRequests(): Promise<Request[]> {
    const requests: Request[] = [
      {
        id: '5e887ac47eed253091be10cb',
        name: "Test workload",
        machineType: "L2 DS",
        image: "test image",
        status: "complete"
      },
      {
        id: '6e887ac47eed253091be10cb',
        name: "Test workload 2",
        machineType: "L2 DS",
        image: "test image",
        status: "complete"
      },
      {
        id: '6e887ac47eed253091be10cb',
        name: "Test workload 2",
        machineType: "L2 DS",
        image: "test image",
        status: "complete"
      },
      {
        id: '6e887ac47eed253091be10cb',
        name: "Test workload 2",
        machineType: "L2 DS",
        image: "test image",
        status: "complete"
      },
      {
        id: '6e887ac47eed253091be10cb',
        name: "Test workload 2",
        machineType: "L2 DS",
        image: "test image",
        status: "complete"
      },
      {
        id: '6e887ac47eed253091be10cb',
        name: "Test workload 2",
        machineType: "L2 DS",
        image: "test image",
        status: "complete"
      }
    ];

    return Promise.resolve(requests);
  }

  getRequest(): Promise<Request> {
    const request: Request = {
      id: '6e887ac47eed253091be10cb',
      name: "Test workload 2",
      machineType: "L2 DS",
      image: "test image",
      status: "complete"
    };

    return Promise.resolve(request);
  }

}

export const requestApi = new RequestApi();
