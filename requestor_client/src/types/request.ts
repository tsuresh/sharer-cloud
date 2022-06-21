export interface Request {
    workload_id: string;
    workload_name: string;
    machine_type: string;
    machine_image: string;
    status: string;
    logUrl?: string;
}