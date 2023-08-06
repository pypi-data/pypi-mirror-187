# Use Case Outcome

A Python package that records logs and metrics throughout the execution of a Use Case ran in Swimlane. This allows us to easily save a record within our Use Case Outcome application to diagnose issues with Use Cases much quicker.

## In this README :point_down:

- [Setup](#setup)
- [Usage](#usage)
  - [Initial setup](#initial-setup)
  - [Creating releases](#creating-releases)
- [Functionality](#functionality)
- [Contributing](#contributing)

## Usage

### Initial setup

1. Simply install the package

`pip install use_case_outcome` or `pip install use_case_outcome==1.0.0`

2. Import it into your module:

```python
from use_case_outcome import UseCaseOutcome
```

3. Initialise your own instance of `UseCaseOutcome`

```python
uco = UseCaseOutcome(swimlane, "Application Name", "Integration Name", extra_key_value="test")
```

4. Start your use case. This will start your timer and you can log your logs, metrics and fields changed as you go through. Please refer to [Functionality](#functionality)

```python
uco.start()
```

### Creating releases

#### Manually

If you wish to build and deploy a release of this package manually from your own machine, you can do that via the `poetry CLI`. Please ensure that you have a value key setup to access PyPi with Poetry. Please see the docs for poetry [here](https://python-poetry.org/docs/repositories/#configuring-credentials)

Build the package:

Poetry uses the `pyproject.toml` file for it's config when you run commands within this directory, so it gets all of it's information about the package from there including any dependencies and where to look for the modules.

```bash
poetry build
```

Publish the packagee:

Once you have your creds setup with PyPi and you're ready to publish, you should be able to publish by using the below command

```bash
poetry publish
```

## Functionality

### UseCaseOutcome class

#### Properties

* `sl` - Swimlane instance
* `app_name` - The application name that the Use Case belongs to
* `integration_name` - The integration that is running
* `default_fields` - Any default fields that you want available on every log
* `logs` - All of the logs that get logged during the execution of a use case
* `metrics` - All of the metrics that get logged during the execution of a use case
* `fields_changed` - All of the fields changed that get logged during the execution of a use case
* `use_case_started` - The timestamp of when the use case was started (see `start()` method below)
* `arbitrary_record_fields` - This is to protect future enhancements to the UseCaseOutcome application. Applications can make use of new fields without having to update this package

#### Methods

`__init__(self, sl: Swimlane, app_name: str, integration_name: str, **default_fields)`:

Parameters:

    * sl: Swimlane - The Swimlane instance that you instantiate inside of your Use Case
    * app_name: str - The application name that triggered the use case
    * integration_name: str - The integration that is executing
    * default_fields: kwargs - This is a kwargs argument allowing you to pass in default fields for your logs. This means any fields passed in via this parameter will be available on every log

`start(self)`:

> The `start()` method is called at the start of a Use Case and records the time that it starts on the UseCaseOutcome object

`update_field(self, field_name: str, field_value: str)`:

> Update field is used to update a field inside of the Use Case Outcome application. It remains dynamic to ensure that as fields get added to the Use Case Outcome application, we don't have to apply updated to this package

Parameters:

    * field_name: str - The field name on the Use Case Outcome application you wish to update. To conform with Python standards, we have some processing on the field names and so they have to be in a certain format. Example : If the field in the Use Case Outcome application is `Saim Case Created`, then the `field_name` you would pass into this method would be `saim_case_created`. **IMPORTANT: We must ensure that fields in the Use Case Outcome application conform with this format : Saim Case Created. Each word capitalised and separated by a space**
    * field_value: str - The value you wish to set the field to in the Use Case Outcome application

`submit(self, status: Literal["Success", "Failed"], record: Record, auto_closed: bool = False)`:

> This is what you will run at the end, once you have finished the use case. This will take all of the logs, metrics and other pieces of information you have gathered during the executing of your use case and create a record in the Use Case Outcome application allowing you to see them all in a single record

Parameters:

    * status: Literal["Success", "Failed"] - The status of which the use case was. Currently only either a complete success, or a complete failure
    * record: Record - The record the Use Case is running for
    * auto_closed: Bool = False - Whether or not the execution of the use case caused an auto-closure of that current record or not

`duration(self, end_time: DateTime) -> float`:

> A helper method that simply takes in an end time and gets the duration between the `start_time` on the object and the end time that was passed in

Parameters:

    * end_time: DateTime - It uses this time, and the start time registered when running the `start()` method to work out an overall duration. This method is ran as part of the `submit` method so is nothing you have to worry about in a use case

Returns:

    * duration: float - The duration in seconds between `self.start_time` and the `end_time` parameter

`create_uco_record(self, data: Dict[str, Any], record: Record)`

> This is responsible for taking the data that has been processed inside of the object already and creating the Use Case Outcome application which allows us to refer back to this data at a later date. This method is called within the `submit()` method and so is nothing you have to worry about inside of your use case

Parameters:

    * data: Dict[str, Any] - This is the data you want to unpack to create the actual record. The data processing has already been done within the `submit()` method
    * record: Record - The originating record that is creating the Use Case Outcome record. This will allow us to add a reference back to that originating record

`log(self, level: str, **kwargs)`

> This is a generic log method which allows us to create logs to be created in the Use Case Outcome record. The levels allowed are as per below. Kwargs allows you to pass any number of arbitrary key/value pairs into your logs allowing for ultimate flexibility

Levels allowed : `_LEVELS = ["debug", "info", "warning", "error", "critical"]`

Parameters:

    * level: str - The level, as a string. It must be one of those defined in `_LEVELS` as outlined above
    * **kwargs - Each log may require different amounts of information to provide different pieces of contextual information to that log, depending on what it's doing. That's what kwargs allows us to do, each log will have full flexibility in terms of what data it can provide to that particular log

`metric(self, metric_name: str, metric_value: Any)`:

> This is a method, similar to the log method that allows you to create metrics on the fly during the execution of your use case. You can only ever create one metric/value at one time

Parameters:

    * metric_name: str - The name of your metric
    * metric_value: Any - The value of your metric

`record_saved(self)`:

> This is ran whenever you have ran the `save()` or `patch()` method on your record within your use case. This will then record that time against all fields taht were changed as part of that process

`field_changed(self, field_name: str, old_field_value: str, new_field_value: str)`:

> This method allows us to register whenever a field is changed within your use case. For example if you're setting `analysis complete` to `YES`, then this would be an opportunity to run this method. When you run the `record_saved` method, it will go through the fields and record a timestamp against when they changed

Parameters:

    * field_name: str - The field name that we have changed the value of
    * old_field_value: str - The old field value, the value we are changing from
    * new_field_value: str - This is the value we have changed to

`_normalise_logs(self)`:

> The widget responsible for displaying the logs, requires there to be the exact same fields available in each log. This is a problem with the setup we have, as each log can contain any arbitrary key/value pairs and therefore by default this isn't the case. This method will iterate over all of the logs ensuring that they contain all of the same key/value pairs - allowing our widget to work

`_normalise_keys(d: dict)`:

> A helper method to normalise the keys of the dictionary that is passed in. It will iterate over all of the keys, replace the `_` with a `space` and replacing the start of each word with a capitalised letter. `create_saim_case` becomes `Create Saim Case`

Parameters:

    * d: dict - The data of which we want to normalise the keys for

## Contributing

To contribute to this project, please just Git Clone the project and ensure a pull request is raised and assigned to an applicable person
