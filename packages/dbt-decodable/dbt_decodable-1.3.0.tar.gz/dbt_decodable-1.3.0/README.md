# dbt-decodable

[dbt] adapter for [Decodable].

[dbt] enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.

## Installation

`dbt-decodable` is available on [PyPI]. To install the latest version via `pip` (optionally using a virtual environment),
run:

```nofmt
python3 -m venv dbt-venv         # create the virtual environment
source dbt-venv/bin/activate     # activate the virtual environment
pip install dbt-decodable      # install the adapter
```

## Configuring your profile

Most of the profile configuration options available can be found inside the [`dbt documentation`](https://docs.getdbt.com/reference/profiles.yml). Additionally, `dbt-decodable` defines a few adapter-specific ones that can be found below.

```yml
dbt-decodable:
  target: dev
  outputs:
    dev:
      type: decodable
      # decodable specific settings
      account_name: [your account]
      profile_name: [name of the profile]
      materialize_tests: [true | false] # whether to materialize tests as a pipeline/stream pair, default is `false`
      timeout: [ms] # maximum accumulative time a preview request should run for, default is `60000`
      preview_start: [earliest | latest] # whether preview should be run with `earliest` or `latest` start position, default is `earliest`
      local_namespace: [namespace prefix] # prefix added to all entities created on Decodable, default is `None`, meaning no prefix gets added.
```

This file usually resides inside the `~/.dbt` directory.

## Supported Features

### Materializations

Only table [materialization](https://docs.getdbt.com/docs/build/materializations) is supported for dbt models at the moment. A dbt table model translates to a pipeline/stream pair on Decodable, both sharing the same name. Pipelines for models are automatically activated upon materialization.

To materialize your models simply run the [`dbt run`](https://docs.getdbt.com/reference/commands/run) command, which will perform the following steps for each model:

1. Create a stream with the model's name and schema inferred by Decodable from the model's SQL.

2. Create a pipeline that inserts the SQL's results into the newly created stream.

3. Activate the pipeline.

### Custom model configuration

A `watermark` option can be configured to specify the [watermark](https://docs.decodable.co/docs/streams#managing-streams) to be set for the model's respective Decodable stream.

More on specifying configuration options per model can be found [here](https://docs.getdbt.com/reference/model-configs).

### Seeds

[`dbt seed`](https://docs.getdbt.com/reference/commands/seed/) will perform the following steps for each specified seed:

1. Create a REST connection and an associated stream with the same name (reflecting the seed's name).

2. Activate the connection.

3. Send the data stored in the seed's `.csv` file to the connection as events.

4. Deactivate the connection.

After these steps are completed, you can access the seed's data on the newly created stream.

### Sources

[`dbt source`](https://docs.getdbt.com/docs/build/sources) is not supported at the moment.

### Documentation

[`dbt docs`](https://docs.getdbt.com/reference/commands/cmd-docs) is not supported at the moment. You can check your Decodable account for details about your models.

### Testing

Based on the `materialize_tests` option set for the current target, [`dbt test`](https://docs.getdbt.com/reference/commands/test) will behave differently:

* `materialize_tests = false` will cause dbt to run the specified tests as previews return the results after they finish. The exact time the preview runs for, as well as whether they run starting positions should be set to `earliest` or `latest` can be changed using the `timeout` and `preview_start` target configurations respectively.

* `materialize_tests = true` will cause dbt to persist the specified tests as pipeline/stream pairs on Decodable. This configuration is designed to allow continous testing of your models. You can then run a preview on the created stream (for example using [Decodable CLI]) to monitor the results.

### Snapshots

Neither the [`dbt snapshot`] command nor the notion of snapshots are supported at the moment.

### Additional Operations

`dbt-decodable` provides a set of commands for managing the project's resources on Decodable. Those commands can be run using [`dbt run-operation {name} --args {args}`](https://docs.getdbt.com/reference/commands/run-operation).

___

#### **`stop_pipelines(pipelines)`**

**pipelines** : Optional list of names. Default value is `None`.

Deactivate pipelines for resources defined within the project. If the `pipelines` arg is provided, the command only considers the listed resources. Otherwise, it deactivates all pipelines associated with the project.

___

#### **`delete_pipelines(pipelines)`**

**pipelines** : Optional list of names. Default value is `None`.

Delete pipelines for resources defined within the project. If the `pipelines` arg is provided, the command only considers the listed resources. Otherwise, it deletes all pipelines associated with the project.

___

#### **`delete_streams(streams, skip_errors)`**

**streams** : Optional list of names. Default value is `None`. <br>
**skip_errors** : Whether to treat errors as warnings. Default value is `true`.

Delete streams for resources defined within the project. Note that it does not delete pipelines associated with those streams, failing to remove a stream if one exists. For a complete removal of stream/pipeline pairs, see the `cleanup` operation. <br>
If the `streams` arg is provided, the command only considers the listed resources. Otherwise, it attempts to delete all streams associated with the project. <br>
If `skip_errors` is set to `true`, failure to delete a stream (e.g. due to an associated pipeline) will be reported as a warning. Otherwise, the operation stops upon the first error encountered.

___

#### **`cleanup(list, models, seeds, tests)`**

**list** : Optional list of names. Default value is `None`. <br>
**models** : Whether to include models during cleanup. Default value is `true`. <br>
**seeds** : Whether to include seeds during cleanup. Default value is `true`. <br>
**tests** : Whether to include tests during cleanup. Default value is `true`.

Delete all Decodable entities resulting from the materialization of the project's resources, i.e. connections, streams and pipelines. <br>
If the `list` arg is provided, the command only considers the listed resources. Otherwise, it deletes all entities associated with the project. <br>
The `models`, `seeds` and `tests` arguments specify whether those resource types should be included in the cleanup. Note that cleanup does nothing for tests that have not been materialized.

[dbt]: https://www.getdbt.com/
[Decodable]: https://www.decodable.co/
[Decodable CLI]: https://docs.decodable.co/docs/command-line-interface
[PyPI]: https://pypi.org/project/dbt-decodable/
