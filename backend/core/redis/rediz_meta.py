from rq import get_current_job

def write_meta_error(data):
    job = get_current_job()
    error_exists = job.meta.get("errors", False)
    if error_exists:
         job.meta['errors'].append(data)
         job.save_meta()
    else:
        job.meta['result'] = "failed"
        job.meta['errors'] = []
        job.meta['errors'].append(data)
        job.save_meta()

def write_meta_result(result):
    job = get_current_job()
    result = job.meta.get("result", False)
    if result != "failed":
        job.meta['result'] = result
        job.save_meta()

def prepare_netpalm_payload():
    try:
        job = get_current_job()
        resultdata = {
                "status": "success",
                "data": {
                    "task_id": job.id,
                    "created_on": job.created_on,
                    "task_queue": job.description,
                    "task_status": "finished",
                    "task_result": job.result
                }
        }
        return resultdata
    except Exception as e:
        return e