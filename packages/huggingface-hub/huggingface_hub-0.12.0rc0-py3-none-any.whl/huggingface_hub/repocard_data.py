import copy
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from huggingface_hub.utils import yaml_dump

from .utils.logging import get_logger


logger = get_logger(__name__)


@dataclass
class EvalResult:
    """
    Flattened representation of individual evaluation results found in model-index of Model Cards.

    For more information on the model-index spec, see https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1.

    Args:
        task_type (`str`):
            The task identifier. Example: "image-classification".
        dataset_type (`str`):
            The dataset identifier. Example: "common_voice". Use dataset id from https://hf.co/datasets.
        dataset_name (`str`):
            A pretty name for the dataset. Example: "Common Voice (French)".
        metric_type (`str`):
            The metric identifier. Example: "wer". Use metric id from https://hf.co/metrics.
        metric_value (`Any`):
            The metric value. Example: 0.9 or "20.0 ± 1.2".
        task_name (`str`, *optional*):
            A pretty name for the task. Example: "Speech Recognition".
        dataset_config (`str`, *optional*):
            The name of the dataset configuration used in `load_dataset()`.
            Example: fr in `load_dataset("common_voice", "fr")`. See the `datasets` docs for more info:
            https://hf.co/docs/datasets/package_reference/loading_methods#datasets.load_dataset.name
        dataset_split (`str`, *optional*):
            The split used in `load_dataset()`. Example: "test".
        dataset_revision (`str`, *optional*):
            The revision (AKA Git Sha) of the dataset used in `load_dataset()`.
            Example: 5503434ddd753f426f4b38109466949a1217c2bb
        dataset_args (`Dict[str, Any]`, *optional*):
            The arguments passed during `Metric.compute()`. Example for `bleu`: `{"max_order": 4}`
        metric_name (`str`, *optional*):
            A pretty name for the metric. Example: "Test WER".
        metric_config (`str`, *optional*):
            The name of the metric configuration used in `load_metric()`.
            Example: bleurt-large-512 in `load_metric("bleurt", "bleurt-large-512")`.
            See the `datasets` docs for more info: https://huggingface.co/docs/datasets/v2.1.0/en/loading#load-configurations
        metric_args (`Dict[str, Any]`, *optional*):
            The arguments passed during `Metric.compute()`. Example for `bleu`: max_order: 4
        verified (`bool`, *optional*):
            Indicates whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not. Automatically computed by Hugging Face, do not set.
        verify_token (`str`, *optional*):
            A JSON Web Token that is used to verify whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not.
    """

    # Required

    # The task identifier
    # Example: automatic-speech-recognition
    task_type: str

    # The dataset identifier
    # Example: common_voice. Use dataset id from https://hf.co/datasets
    dataset_type: str

    # A pretty name for the dataset.
    # Example: Common Voice (French)
    dataset_name: str

    # The metric identifier
    # Example: wer. Use metric id from https://hf.co/metrics
    metric_type: str

    # Value of the metric.
    # Example: 20.0 or "20.0 ± 1.2"
    metric_value: Any

    # Optional

    # A pretty name for the task.
    # Example: Speech Recognition
    task_name: Optional[str] = None

    # The name of the dataset configuration used in `load_dataset()`.
    # Example: fr in `load_dataset("common_voice", "fr")`.
    # See the `datasets` docs for more info:
    # https://huggingface.co/docs/datasets/package_reference/loading_methods#datasets.load_dataset.name
    dataset_config: Optional[str] = None

    # The split used in `load_dataset()`.
    # Example: test
    dataset_split: Optional[str] = None

    # The revision (AKA Git Sha) of the dataset used in `load_dataset()`.
    # Example: 5503434ddd753f426f4b38109466949a1217c2bb
    dataset_revision: Optional[str] = None

    # The arguments passed during `Metric.compute()`.
    # Example for `bleu`: max_order: 4
    dataset_args: Optional[Dict[str, Any]] = None

    # A pretty name for the metric.
    # Example: Test WER
    metric_name: Optional[str] = None

    # The name of the metric configuration used in `load_metric()`.
    # Example: bleurt-large-512 in `load_metric("bleurt", "bleurt-large-512")`.
    # See the `datasets` docs for more info: https://huggingface.co/docs/datasets/v2.1.0/en/loading#load-configurations
    metric_config: Optional[str] = None

    # The arguments passed during `Metric.compute()`.
    # Example for `bleu`: max_order: 4
    metric_args: Optional[Dict[str, Any]] = None

    # Indicates whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not. Automatically computed by Hugging Face, do not set.
    verified: Optional[bool] = None

    # A JSON Web Token that is used to verify whether the metrics originate from Hugging Face's [evaluation service](https://huggingface.co/spaces/autoevaluate/model-evaluator) or not.
    verify_token: Optional[str] = None

    @property
    def unique_identifier(self) -> tuple:
        """Returns a tuple that uniquely identifies this evaluation."""
        return (
            self.task_type,
            self.dataset_type,
            self.dataset_config,
            self.dataset_split,
            self.dataset_revision,
        )

    def is_equal_except_value(self, other: "EvalResult") -> bool:
        """
        Return True if `self` and `other` describe exactly the same metric but with a
        different value.
        """
        for key, _ in self.__dict__.items():
            if key == "metric_value":
                continue
            # For metrics computed by Hugging Face's evaluation service, `verify_token` is derived from `metric_value`,
            # so we exclude it here in the comparison.
            if key != "verify_token" and getattr(self, key) != getattr(other, key):
                return False
        return True


@dataclass
class CardData:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Converts CardData to a dict.

        Returns:
            `dict`: CardData represented as a dictionary ready to be dumped to a YAML
            block for inclusion in a README.md file.
        """

        data_dict = copy.deepcopy(self.__dict__)
        self._to_dict(data_dict)
        return _remove_none(data_dict)

    def _to_dict(self, data_dict):
        """Use this method in child classes to alter the dict representation of the data. Alter the dict in-place.

        Args:
            data_dict (`dict`): The raw dict representation of the card data.
        """
        pass

    def to_yaml(self, line_break=None) -> str:
        """Dumps CardData to a YAML block for inclusion in a README.md file.

        Args:
            line_break (str, *optional*):
                The line break to use when dumping to yaml.

        Returns:
            `str`: CardData represented as a YAML block.
        """
        return yaml_dump(self.to_dict(), sort_keys=False, line_break=line_break).strip()

    def __repr__(self):
        return self.to_yaml()


class ModelCardData(CardData):
    """Model Card Metadata that is used by Hugging Face Hub when included at the top of your README.md

    Args:
        language (`Union[str, List[str]]`, *optional*):
            Language of model's training data or metadata. It must be an ISO 639-1, 639-2 or
            639-3 code (two/three letters), or a special value like "code", "multilingual". Defaults to `None`.
        license (`str`, *optional*):
            License of this model. Example: apache-2.0 or any license from
            https://huggingface.co/docs/hub/repositories-licenses. Defaults to None.
        library_name (`str`, *optional*):
            Name of library used by this model. Example: keras or any library from
            https://github.com/huggingface/hub-docs/blob/main/js/src/lib/interfaces/Libraries.ts.
            Defaults to None.
        tags (`List[str]`, *optional*):
            List of tags to add to your model that can be used when filtering on the Hugging
            Face Hub. Defaults to None.
        datasets (`Union[str, List[str]]`, *optional*):
            Dataset or list of datasets that were used to train this model. Should be a dataset ID
            found on https://hf.co/datasets. Defaults to None.
        metrics (`Union[str, List[str]]`, *optional*):
            List of metrics used to evaluate this model. Should be a metric name that can be found
            at https://hf.co/metrics. Example: 'accuracy'. Defaults to None.
        eval_results (`Union[List[EvalResult], EvalResult]`, *optional*):
            List of `huggingface_hub.EvalResult` that define evaluation results of the model. If provided,
            `model_name` is used to as a name on PapersWithCode's leaderboards. Defaults to `None`.
        model_name (`str`, *optional*):
            A name for this model. It is used along with
            `eval_results` to construct the `model-index` within the card's metadata. The name
            you supply here is what will be used on PapersWithCode's leaderboards. If None is provided
            then the repo name is used as a default. Defaults to None.
        kwargs (`dict`, *optional*):
            Additional metadata that will be added to the model card. Defaults to None.

    Example:
        ```python
        >>> from huggingface_hub import ModelCardData
        >>> card_data = ModelCardData(
        ...     language="en",
        ...     license="mit",
        ...     library_name="timm",
        ...     tags=['image-classification', 'resnet'],
        ... )
        >>> card_data.to_dict()
        {'language': 'en', 'license': 'mit', 'library_name': 'timm', 'tags': ['image-classification', 'resnet']}

        ```
    """

    def __init__(
        self,
        *,
        language: Optional[Union[str, List[str]]] = None,
        license: Optional[str] = None,
        library_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        datasets: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        eval_results: Optional[List[EvalResult]] = None,
        model_name: Optional[str] = None,
        **kwargs,
    ):
        self.language = language
        self.license = license
        self.library_name = library_name
        self.tags = tags
        self.datasets = datasets
        self.metrics = metrics
        self.eval_results = eval_results
        self.model_name = model_name

        model_index = kwargs.pop("model-index", None)
        if model_index:
            try:
                model_name, eval_results = model_index_to_eval_results(model_index)
                self.model_name = model_name
                self.eval_results = eval_results
            except KeyError:
                logger.warning(
                    "Invalid model-index. Not loading eval results into CardData."
                )

        super().__init__(**kwargs)

        if self.eval_results:
            if type(self.eval_results) == EvalResult:
                self.eval_results = [self.eval_results]
            if self.model_name is None:
                raise ValueError(
                    "Passing `eval_results` requires `model_name` to be set."
                )

    def _to_dict(self, data_dict):
        """Format the internal data dict. In this case, we convert eval results to a valid model index"""
        if self.eval_results is not None:
            data_dict["model-index"] = eval_results_to_model_index(
                self.model_name, self.eval_results
            )
            del data_dict["eval_results"], data_dict["model_name"]


class DatasetCardData(CardData):
    """Dataset Card Metadata that is used by Hugging Face Hub when included at the top of your README.md

    Args:
        language (`Union[str, List[str]]`, *optional*):
            Language of dataset's data or metadata. It must be an ISO 639-1, 639-2 or
            639-3 code (two/three letters), or a special value like "code", "multilingual".
        license (`Union[str, List[str]]`, *optional*):
            License(s) of this dataset. Example: apache-2.0 or any license from
            https://huggingface.co/docs/hub/repositories-licenses.
        annotations_creators (`Union[str, List[str]]`, *optional*):
            How the annotations for the dataset were created.
            Options are: 'found', 'crowdsourced', 'expert-generated', 'machine-generated', 'no-annotation', 'other'.
        language_creators (`Union[str, List[str]]`, *optional*):
            How the text-based data in the dataset was created.
            Options are: 'found', 'crowdsourced', 'expert-generated', 'machine-generated', 'other'
        multilinguality (`Union[str, List[str]]`, *optional*):
            Whether the dataset is multilingual.
            Options are: 'monolingual', 'multilingual', 'translation', 'other'.
        size_categories (`Union[str, List[str]]`, *optional*):
            The number of examples in the dataset. Options are: 'n<1K', '1K<n<10K', '10K<n<100K',
            '100K<n<1M', '1M<n<10M', '10M<n<100M', '100M<n<1B', '1B<n<10B', '10B<n<100B', '100B<n<1T', 'n>1T', and 'other'.
        source_datasets (`Union[str, List[str]]`, *optional*):
            Indicates whether the dataset is an original dataset or extended from another existing dataset.
            Options are: 'original' and 'extended'.
        task_categories (`Union[str, List[str]]`, *optional*):
            What categories of task does the dataset support?
        task_ids (`Union[str, List[str]]`, *optional*):
            What specific tasks does the dataset support?
        paperswithcode_id (`str`, *optional*):
            ID of the dataset on PapersWithCode.
        pretty_name (`str`, *optional*):
            A more human-readable name for the dataset. (ex. "Cats vs. Dogs")
        train_eval_index (`Dict`, *optional*):
            A dictionary that describes the necessary spec for doing evaluation on the Hub.
            If not provided, it will be gathered from the 'train-eval-index' key of the kwargs.
        configs (`Union[str, List[str]]`, *optional*):
            A list of the available dataset configs for the dataset.
    """

    def __init__(
        self,
        *,
        language: Optional[Union[str, List[str]]] = None,
        license: Optional[Union[str, List[str]]] = None,
        annotations_creators: Optional[Union[str, List[str]]] = None,
        language_creators: Optional[Union[str, List[str]]] = None,
        multilinguality: Optional[Union[str, List[str]]] = None,
        size_categories: Optional[Union[str, List[str]]] = None,
        source_datasets: Optional[Union[str, List[str]]] = None,
        task_categories: Optional[Union[str, List[str]]] = None,
        task_ids: Optional[Union[str, List[str]]] = None,
        paperswithcode_id: Optional[str] = None,
        pretty_name: Optional[str] = None,
        train_eval_index: Optional[Dict] = None,
        configs: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ):
        self.annotations_creators = annotations_creators
        self.language_creators = language_creators
        self.language = language
        self.license = license
        self.multilinguality = multilinguality
        self.size_categories = size_categories
        self.source_datasets = source_datasets
        self.task_categories = task_categories
        self.task_ids = task_ids
        self.paperswithcode_id = paperswithcode_id
        self.pretty_name = pretty_name
        self.configs = configs

        # TODO - maybe handle this similarly to EvalResult?
        self.train_eval_index = train_eval_index or kwargs.pop("train-eval-index", None)
        super().__init__(**kwargs)

    def _to_dict(self, data_dict):
        data_dict["train-eval-index"] = data_dict.pop("train_eval_index")


def model_index_to_eval_results(
    model_index: List[Dict[str, Any]]
) -> Tuple[str, List[EvalResult]]:
    """Takes in a model index and returns the model name and a list of `huggingface_hub.EvalResult` objects.

    A detailed spec of the model index can be found here:
    https://github.com/huggingface/hub-docs/blob/main/modelcard.md?plain=1

    Args:
        model_index (`List[Dict[str, Any]]`):
            A model index data structure, likely coming from a README.md file on the
            Hugging Face Hub.

    Returns:
        model_name (`str`):
            The name of the model as found in the model index. This is used as the
            identifier for the model on leaderboards like PapersWithCode.
        eval_results (`List[EvalResult]`):
            A list of `huggingface_hub.EvalResult` objects containing the metrics
            reported in the provided model_index.

    Example:
        ```python
        >>> from huggingface_hub.repocard_data import model_index_to_eval_results
        >>> # Define a minimal model index
        >>> model_index = [
        ...     {
        ...         "name": "my-cool-model",
        ...         "results": [
        ...             {
        ...                 "task": {
        ...                     "type": "image-classification"
        ...                 },
        ...                 "dataset": {
        ...                     "type": "beans",
        ...                     "name": "Beans"
        ...                 },
        ...                 "metrics": [
        ...                     {
        ...                         "type": "accuracy",
        ...                         "value": 0.9
        ...                     }
        ...                 ]
        ...             }
        ...         ]
        ...     }
        ... ]
        >>> model_name, eval_results = model_index_to_eval_results(model_index)
        >>> model_name
        'my-cool-model'
        >>> eval_results[0].task_type
        'image-classification'
        >>> eval_results[0].metric_type
        'accuracy'

        ```
    """

    eval_results = []
    for elem in model_index:
        name = elem["name"]
        results = elem["results"]
        for result in results:
            task_type = result["task"]["type"]
            task_name = result["task"].get("name")
            dataset_type = result["dataset"]["type"]
            dataset_name = result["dataset"]["name"]
            dataset_config = result["dataset"].get("config")
            dataset_split = result["dataset"].get("split")
            dataset_revision = result["dataset"].get("revision")
            dataset_args = result["dataset"].get("args")

            for metric in result["metrics"]:
                metric_type = metric["type"]
                metric_value = metric["value"]
                metric_name = metric.get("name")
                metric_args = metric.get("args")
                metric_config = metric.get("config")
                verified = metric.get("verified")
                verify_token = metric.get("verifyToken")

                eval_result = EvalResult(
                    task_type=task_type,  # Required
                    dataset_type=dataset_type,  # Required
                    dataset_name=dataset_name,  # Required
                    metric_type=metric_type,  # Required
                    metric_value=metric_value,  # Required
                    task_name=task_name,
                    dataset_config=dataset_config,
                    dataset_split=dataset_split,
                    dataset_revision=dataset_revision,
                    dataset_args=dataset_args,
                    metric_name=metric_name,
                    metric_args=metric_args,
                    metric_config=metric_config,
                    verified=verified,
                    verify_token=verify_token,
                )
                eval_results.append(eval_result)
    return name, eval_results


def _remove_none(obj):
    """
    Recursively remove `None` values from a dict. Borrowed from: https://stackoverflow.com/a/20558778
    """
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(_remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)(
            (_remove_none(k), _remove_none(v))
            for k, v in obj.items()
            if k is not None and v is not None
        )
    else:
        return obj


def eval_results_to_model_index(
    model_name: str, eval_results: List[EvalResult]
) -> List[Dict[str, Any]]:
    """Takes in given model name and list of `huggingface_hub.EvalResult` and returns a
    valid model-index that will be compatible with the format expected by the
    Hugging Face Hub.

    Args:
        model_name (`str`):
            Name of the model (ex. "my-cool-model"). This is used as the identifier
            for the model on leaderboards like PapersWithCode.
        eval_results (`List[EvalResult]`):
            List of `huggingface_hub.EvalResult` objects containing the metrics to be
            reported in the model-index.

    Returns:
        model_index (`List[Dict[str, Any]]`): The eval_results converted to a model-index.

    Example:
        ```python
        >>> from huggingface_hub.repocard_data import eval_results_to_model_index, EvalResult
        >>> # Define minimal eval_results
        >>> eval_results = [
        ...     EvalResult(
        ...         task_type="image-classification",  # Required
        ...         dataset_type="beans",  # Required
        ...         dataset_name="Beans",  # Required
        ...         metric_type="accuracy",  # Required
        ...         metric_value=0.9,  # Required
        ...     )
        ... ]
        >>> eval_results_to_model_index("my-cool-model", eval_results)
        [{'name': 'my-cool-model', 'results': [{'task': {'type': 'image-classification'}, 'dataset': {'name': 'Beans', 'type': 'beans'}, 'metrics': [{'type': 'accuracy', 'value': 0.9}]}]}]

        ```
    """

    # Metrics are reported on a unique task-and-dataset basis.
    # Here, we make a map of those pairs and the associated EvalResults.
    task_and_ds_types_map = defaultdict(list)
    for eval_result in eval_results:
        task_and_ds_types_map[eval_result.unique_identifier].append(eval_result)

    # Use the map from above to generate the model index data.
    model_index_data = []
    for results in task_and_ds_types_map.values():
        # All items from `results` share same metadata
        sample_result = results[0]
        data = {
            "task": {
                "type": sample_result.task_type,
                "name": sample_result.task_name,
            },
            "dataset": {
                "name": sample_result.dataset_name,
                "type": sample_result.dataset_type,
                "config": sample_result.dataset_config,
                "split": sample_result.dataset_split,
                "revision": sample_result.dataset_revision,
                "args": sample_result.dataset_args,
            },
            "metrics": [
                {
                    "type": result.metric_type,
                    "value": result.metric_value,
                    "name": result.metric_name,
                    "config": result.metric_config,
                    "args": result.metric_args,
                    "verified": result.verified,
                    "verifyToken": result.verify_token,
                }
                for result in results
            ],
        }
        model_index_data.append(data)

    # TODO - Check if there cases where this list is longer than one?
    # Finally, the model index itself is list of dicts.
    model_index = [
        {
            "name": model_name,
            "results": model_index_data,
        }
    ]
    return _remove_none(model_index)
