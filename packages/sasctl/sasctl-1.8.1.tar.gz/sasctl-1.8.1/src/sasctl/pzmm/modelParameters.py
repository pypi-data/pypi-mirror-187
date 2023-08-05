# Copyright (c) 2022, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import json

from .._services.model_repository import ModelRepository as mr

# TODO: Convert STRINGIO calls to string or dict format


def _find_file(model, file_name):
    """
    Retrieves the first file from a registered model on SAS Model Manager that contains the provided
    file_name as an exact match or substring.

    Parameters
    ----------
    model : str or dict
        The name or id of the model, or a dictionary representation of the model.
    file_name : str
        The name of the desired file, or a substring that is contained within the file name.

    Returns
    -------
    RestObj
        The first file with a name containing file_name.
    """
    from ..core import current_session

    sess = current_session()
    file_list = mr.get_model_contents(model)
    for file in file_list:
        print(file.name)
        if file_name.lower() in file.name.lower():
            correct_file = sess.get(
                f"modelRepository/models/{model}/contents/{file.id}/content"
            )
            return correct_file


class ModelParameters:
    @classmethod
    def generate_hyperparameters(cls, model, model_prefix, pickle_path):
        """
        Generates hyperparameters for a given model and creates a JSON file representation.

        Currently only supports generation of scikit-learn model hyperparameters.

        Parameters
        ----------
        model : Python object
            Python object representing the model.
        model_prefix : str
            Name used to create model files. (e.g. (modelPrefix) + "Hyperparameters.json")
        pickle_path : str, Path
            Directory location of model files.

        Yields
        ------
        JSON file
            Named {model_prefix}Hyperparameters.json.
        """

        def sklearn_params():
            """
            Generates hyperparameters for the models generated by scikit-learn.
            """
            hyperparameters = model.get_params()
            model_json = {"hyperparameters": hyperparameters}
            with open(
                Path(pickle_path) / f"{model_prefix}Hyperparameters.json", "w"
            ) as f:
                f.write(json.dumps(model_json, indent=4))

        if all(hasattr(model, attr) for attr in ["_estimator_type", "get_params"]):
            sklearn_params()
        else:
            raise ValueError(
                "This model type is not currently supported for hyperparameter generation."
            )

    @classmethod
    def update_kpis(
        cls,
        project,
        server="cas-shared-default",
        caslib="ModelPerformanceData",
    ):
        """
        Updates hyperparameter file to include KPIs generated by performance definitions, as well
        as any custom KPIs imported by user to the SAS KPI data table.

        Parameters
        ----------
        project : str or dict
            The name or id of the project, or a dictionary representation of the project.
        server : str, optional
            Server on which the KPI data table is stored. Defaults to "cas-shared-default".
        caslib : str, optional
            CAS Library on which the KPI data table is stored. Defaults to "ModelPerformanceData".
        """
        from ..tasks import get_project_kpis
        from io import StringIO

        kpis = get_project_kpis(project, server, caslib)
        models_to_update = kpis["ModelUUID"].unique().tolist()
        for model in models_to_update:
            current_params = _find_file(model, "hyperparameters")
            current_json = current_params.json()
            model_rows = kpis.loc[kpis["ModelUUID"] == model]
            model_rows.set_index("TimeLabel", inplace=True)
            kpi_json = model_rows.to_json(orient="index")
            parsed_json = json.loads(kpi_json)
            current_json["kpis"] = parsed_json
            file_name = "{}Hyperparameters.json".format(
                current_json["kpis"][list(current_json["kpis"].keys())[0]]["ModelName"]
            )
            mr.add_model_content(
                model,
                StringIO(json.dumps(current_json, indent=4)),
                file_name,
            )

    @classmethod
    def get_hyperparameters(cls, model):
        """
        Retrieves the hyperparameter json file from specified model on SAS Model Manager.

        Parameters
        ----------
        model : str or dict
            The name or id of the model, or a dictionary representation of the model.

        Returns
        -------
        dict
            Dictionary containing the contents of the hyperparameter file.
        """
        if mr.is_uuid(model):
            id_ = model
        elif isinstance(model, dict) and "id" in model:
            id_ = model["id"]
        else:
            model = mr.get_model(model)
            id_ = model["id"]
        file = _find_file(id_, "hyperparameters")
        return file.json()

    @classmethod
    def add_hyperparameters(cls, model, **kwargs):
        """
        Adds custom hyperparameters to the hyperparameter file contained within the model in SAS Model Manager.

        Parameters
        ----------
        model : str or dict
            The name or id of the model, or a dictionary representation of the model.
        kwargs
            Named variables pairs representing hyperparameters to be added to the hyperparameter file.
        """
        from io import StringIO

        if not isinstance(model, dict):
            model = mr.get_model(model)
        hyperparameters = cls.get_hyperparameters(model.id)
        for key, value in kwargs.items():
            hyperparameters["hyperparameters"][key] = value
        mr.add_model_content(
            model,
            StringIO(json.dumps(hyperparameters, indent=4)),
            f"{model.name}Hyperparameters.json",
        )
