# Andreani Advanced Analytics tools

## Instalar usando pip

```

pip install andreani-aa-ml

```

## Importación

```

import aa_ml

```

## Ejemplo de uso

- AML Pipeline: Pipeline de ejecución de experimentos en Azure Machine Learning

```

from aa_tools import aml_pipeline, logger

if __name__ == "__main__":

    log = logger("test.py", "main")

    # Not part of pipeline
    aml_pipeline.create_train_template("test_file.py")
    log.log_console("Template file created as test_file.py", "INFO")

    tags = {
      "scale" : "false",
      "balanced" : "false",
      "outliers" : "false",
      "target" : "target"
    }
    log.log_console("Tags defined", "INFO")
    try:
      Pipeline = aml_pipeline.pipeline("aa_tools_test", "linear_regression", "regression", tags)
    except Exception as e:
      log.log_console(f"Exception initializing pipeline: {e}")
      log.close()
      raise e

    try:
      Pipeline.run("aml/azure.pkl", "aml/environment.yml", "aml", "train_template.py", log)
    except Exception as e:
      log.log_console(f"Exception running pipeline: {e}")
      log.close()
      raise e

    log.close()

```
