from abc import ABC, abstractmethod


class GroundTruthApiMixin(ABC):
    @abstractmethod
    def request(self, uri, method, body_params=None, query_params=None, required_api_key=False):
        pass

    def create_ground_truth(self, app_id: str, input_json: dict = None, label: dict = None, tag: str = None) -> dict:
        """
        Submit fresh ground truth data
        :param app_id: Application instance id
        :param input_json: Input that should match input schema of data program
        :param label: Label, or output that should match output schema of data program
        :param tag: Tag to identify ground truth data
        :return: Ground truth data object
        """
        body_json = {}
        if input_json is not None:
            body_json['input'] = input_json
        if label is not None:
            body_json['label'] = label
        if tag is not None:
            body_json['tag'] = tag
        uri = f'apis/{app_id}/baselineData'
        return self.request(uri, 'POST', body_params=body_json, required_api_key=True)

    def update_ground_truth(self, ground_truth_data_id: str, input_json: dict = None, label: dict = None,
                            tag: str = None) -> dict:
        """
        Upload (patch) ground truth data
        :param ground_truth_data_id: Id of ground truth data
        :param input_json: Input that should match input schema of data program
        :param label: Label, or output that should match output schema of data program
        :param tag: Tag to identify ground truth data
        :return: Updated ground truth data object
        """
        body_json = {}
        if input_json is not None:
            body_json['input'] = input_json
        if label is not None:
            body_json['label'] = label
        if tag is not None:
            body_json['tag'] = tag
        uri = f'baselineData/{ground_truth_data_id}'
        return self.request(uri, 'PATCH', required_api_key=True)

    def list_ground_truth_data(self, app_id: str) -> dict:
        """
        List all ground truth data for an application
        :param app_id: Application id
        :return: Paginated list of ground truth data objects
        """
        uri = f'apis/{app_id}/baselineData'
        return self.request(uri, 'GET', required_api_key=True)

    def get_ground_truth_data(self, ground_truth_data_id: str) -> dict:
        """
        Fetch single ground truth data object
        :param ground_truth_data_id: Id of ground truth data
        :return: Ground truth data object
        """
        uri = f'baselineData/{ground_truth_data_id}'
        return self.request(uri, 'GET', required_api_key=True)

    def delete_ground_truth_data(self, ground_truth_data_id) -> dict:
        """
        Mark ground truth data as deleted
        :param ground_truth_data_id: If of ground truth data
        :return Deleted ground truth daata object:
        """
        uri = f'baselineData/{ground_truth_data_id}'
        return self.request(uri, 'DELETE', required_api_key=True)

    def create_ground_truth_from_job(self, app_id: str, job_id: str) -> dict:
        """
        Convert completed job to ground truth data
        :param app_id: Application id
        :param job_id: Job id
        :return: Ground truth data object
        """
        uri = f'apis/{app_id}/baselineData/job/{job_id}'
        return self.request(uri, 'POST', required_api_key=True)
