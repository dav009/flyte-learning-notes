## What is this repo?

Some notes on looking at Flyte internals + some dummy dags to play with features


## Running sample DAGs in this repo

commands below start a sandbox, builds docker file in sandbox. 

```
flytectl sandbox start --source  /Users/dav009/code/david/flytedags
flytectl sandbox exec -- docker build -t hello_world:1 -f Dockerfile .
```

commands below transform dummy dag into protobuf and register the protobuf on the sandbox 

```
pyflyte --pkgs example package --image hello_world:1 -f
flytectl config init
flytectl register files flyte-package.tgz -p flytesnacks -d development --archive --version v2
```

## How does  Flytekit  work ?

Flytepropller
- uses `pyflyte-execute` as entrypoint to a task
- args :

 "args": [
          "pyflyte-execute",
          "--task-module",
          "test_serialization",
          "--task-name",
          "t1",
          "--inputs",
          "{{.input}}",
          "--output-prefix",
          "{{.outputPrefix}}",
          "--raw-output-data-prefix",
          "{{.rawOutputDataPrefix}}"
        ],

sample of entypoint
 https://github.com/flyteorg/flytepropeller/blob/0efd3affc54aa281789ed1463e304f28eee6bd81/pkg/compiler/test/testdata/branch/success_2.json


pyflyte-execute points to `execute_task_cmd`:
https://github.com/flyteorg/flytekit/blob/c011ef7cf47ac8ffc06c48e000cb309d9df99969/flytekit/bin/entrypoint.py#L444

-> _dispatch_execute
    Dispatches execute to PythonTask
        Step1: Download inputs and load into a literal map
        Step2: Invoke task - dispatch_execute
        Step3:
            a: [Optional] Record outputs to output_prefix
            b: OR if IgnoreOutputs is raised, then ignore uploading outputs
            c: OR if an unhandled exception is retrieved - record it as an errors.pb
    
    
-> base_Task.py : dispatch_execute is where the big thing appens

- This method translates Flyte's Type system based input values and invokes the actual call to the executor
- This method is also invoked during runtime.
- literal inputs ( input_literal_map ) are tranlsated to native inputs via   TypeEngine.literal_map_to_kwargs
- to_python_value (type_endgine.py)
- get_transformer (type_engine.py)
 - looks at literal flyte idl and searches if there is a transfoemrt (TypeTransfomer for a given idl, and retunrs it)
 - uses python __origin__ to validate types (keeps a reference to a type that was subscripted,
)
  - typing extensions
  
- structured dwataset is an interface for dataframes. this is to avoid differnt formats i.e: parquet..and others


- what is "FLYTE_INTERNAL_IMAGE" used for?
