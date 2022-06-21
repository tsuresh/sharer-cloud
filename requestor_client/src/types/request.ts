export interface Request {
    workload_id: string;
    workload_name: string;
    machine_type: string;
    machine_image: string;
    artefact_url: string;
    replicas: string;
    spec_url: string;
    user_id: string;
    status: string;
    logUrl?: string;
}

export interface RequestResponse {
    contributor_id:string;
    file_url: string;
    result_id: string;
    status: string;
    time_consumed: string;
    workload_id: string;
}

export interface WorkloadDetail {
    request?: Request;
    responses: RequestResponse[];
}