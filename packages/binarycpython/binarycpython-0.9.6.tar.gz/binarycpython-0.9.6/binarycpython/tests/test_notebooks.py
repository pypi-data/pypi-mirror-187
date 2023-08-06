"""
Notebook tests
"""

import os
import unittest

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

from binarycpython.utils.functions import temp_dir

TMP_DIR = temp_dir("testing", "test_notebooks")
NOTEBOOKS_DIR = os.path.abspath(
    os.path.join(os.path.abspath(__file__), "../../../examples")
)

# define notebooks
notebooks = [
    "notebook_api_functionality.ipynb",
    "notebook_population.ipynb",
    "notebook_individual_systems.ipynb",
    "notebook_custom_logging.ipynb",
    "notebook_extra_features.ipynb",
    "notebook_luminosity_function_single.ipynb",
    "notebook_luminosity_function_binaries.ipynb",
    "notebook_BHBH.ipynb",
    "notebook_common_envelope_evolution.ipynb",
    "notebook_ensembles.ipynb",
    "notebook_solar_system.ipynb",
]


def run_notebook(notebook_path):
    """
    Function to run notebooks and get the errors
    """
    print("Running tests for notebook {}".format(notebook_path))
    # https://www.blog.pythonlibrary.org/2018/10/16/testing-jupyter-notebooks/
    nb_name, _ = os.path.splitext(os.path.basename(notebook_path))
    output_path = os.path.join(TMP_DIR, "{}_all_output.ipynb".format(nb_name))

    # Open notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    # Set up processor
    proc = ExecutePreprocessor(timeout=600, kernel_name="python3")
    proc.allow_errors = True

    # pre-process
    proc.preprocess(nb, {"metadata": {"path": "/"}})

    #
    with open(output_path, mode="wt") as f:
        nbformat.write(nb, f)

    # register errors
    errors = []
    for cell in nb.cells:
        if "outputs" in cell:
            for output in cell["outputs"]:
                if output.output_type == "error":
                    errors.append(output)

    return nb, errors


class TestNotebookMeta(type):
    # from https://stackoverflow.com/questions/32899/how-do-you-generate-dynamic-parameterized-unit-tests-in-python
    def __new__(mcs, name, bases, dct):
        def generate_notebook_test(notebook_name):
            def _notebook_test_function(self):
                """
                Function to handle testing the notebook
                """

                full_notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
                _, errors = run_notebook(full_notebook_path)
                msg = "\nNotebook: {}\n\n".format(notebook_name) + "\n".join(
                    [
                        "{}: {}\n{}".format(
                            el["ename"], el["evalue"], "\n".join(el["traceback"])
                        )
                        for el in errors
                    ]
                )
                self.assertEqual(errors, [], msg=msg)

            return _notebook_test_function

        # Loop over notebooks
        for notebook_name in notebooks:
            # Extract basename and construct methodname
            notebook_basename = notebook_name.split(".")[0]
            methodname = "test_{}".format(notebook_basename)

            # Add to dict
            dct[methodname] = generate_notebook_test(notebook_name=notebook_name)

        # return meta instance with updated methods
        return type.__new__(mcs, name, bases, dct)


class TestSequence(unittest.TestCase, metaclass=TestNotebookMeta):
    pass


if __name__ == "__main__":
    unittest.main()
