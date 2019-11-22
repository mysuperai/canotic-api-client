from datetime import datetime
from typing import List

from abc import ABC, abstractmethod


class JobsApiMixin(ABC):

    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    def create_job(self, api_id: str, callbackUrl: str = None, inputs: List[dict] = None, inputsFileUrl: str = None,
                   metadata: dict = None) -> dict:
        """
        Submit a job

        :param api_id: Application id
        :param callback_url: URL that should be POSTed once the job is completed for the response data.
        :param inputs: List of objects that represent the input of the job (based on the particular app type)
        :param inputsFileUrl: URL of json file containing list of input objects
        :param metadata: Object you can attach to job
        :return: Confirmation message of submission
        """
        body_json = {}
        if callbackUrl is not None:
            body_json['callbackUrl'] = callbackUrl
        if inputs is not None:
            body_json['inputs'] = inputs
        if inputsFileUrl is not None:
            body_json['inputsFileUrl'] = inputsFileUrl
        if metadata is not None:
            body_json['metadata'] = metadata
        uri = f'apps/{api_id}/jobs'
        return self.request(uri, method='POST', body_params=body_json, required_api_key=True)

    def fetch_job(self, job_id: str) -> dict:
        """
        Get Job given job id

        :param job_id: Job id
        :return: Dict with job data
        """
        uri = f'jobs/{job_id}'
        return self.request(uri, method='GET', required_api_key=True)

    def get_job_response(self, job_id: str) -> dict:
        """
        Get Job Response given job id
        :param job_id:
        :return: Dict with job response
        """
        uri = f'jobs/{job_id}/response'
        return self.request(uri, method='GET', required_api_key=True)

    def cancel_job(self, job_id: str) -> dict:
        """
        Cancel a job given job id. Only for jobs in SCHEDULED, IN_PROGRESS or SUSPENDED state.

        :param job_id: Job id
        :return: Dict with job data
        """

        uri = f'jobs/{job_id}/cancel'
        return self.request(uri, method='POST', required_api_key=True)

    def list_jobs(self, app_id: str, page: int = None, size: int = None, sortBy: str = 'id', orderBy: str = 'asc',
                  createdStartDate: datetime = None, createdEndDate: datetime = None,
                  completedStartDate: datetime = None, completedEndDate: datetime = None,
                  statusIn: List[str] = None) -> dict:
        """
        Get a paginated list of jobs given an application id
        :param app_id: Application id
        :param page: Page number [0..N]
        :param size: Size of page
        :param sortBy: Job field to sort by
        :param orderBy: Sort direction (asc or desc)
        :param createdStartDate: Created start date
        :param createdEndDate: Created end date
        :param completedStartDate: Completed start date
        :param completedEndDate: Completed end date
        :param statusIn: Status of jobs
        :return: Paginated list of dicts with jobs data
        """
        uri = f'apps/{app_id}/jobs'
        query_params = {}
        if page is not None:
            query_params['page'] = page
        if size is not None:
            query_params['size'] = size
        if sortBy is not None:
            query_params['sortBy'] = sortBy
        if orderBy is not None:
            query_params['orderBy'] = orderBy
        if createdStartDate is not None:
            query_params['createdStartDate'] = createdStartDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        if createdEndDate is not None:
            query_params['createdEndDate'] = createdEndDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        if completedStartDate is not None:
            query_params['completedStartDate'] = completedStartDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        if completedEndDate is not None:
            query_params['completedEndDate'] = completedEndDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        if statusIn is not None:
            query_params['statusIn'] = statusIn
        return self.request(uri, method='GET', query_params=query_params, required_api_key=True)
