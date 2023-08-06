# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).
import sys

import ipywidgets as widgets
from threading import Thread

from pysparkgui.helper import notification, safe_cast
from pysparkgui.plugins import LoaderPlugin, DF_NEW, Text, PysparkguiError
from pysparkgui.widgets import Singleselect, CopyButton, CodeOutput

try:
    # We expect this to fail in testing & outside databricks
    from pyspark.sql import SparkSession
except ModuleNotFoundError:
    _spark = None
else:
    _spark = SparkSession.getActiveSession()

DATABASE_DOES_NOT_EXIST = "DATABASE_DOES_NOT_EXIST"
ROW_LIMIT_DEFAULT = 100_000

READ_THE_FIRST = "Read the first"
RANDOMLY_SAMPLE = "Randomly sample"
READ_THE_LAST = "Read the last"

class SparkAutocompletionLoaderForNonUC(widgets.VBox):
    def __init__(self, transformation):
        super().__init__()
        self.transformation = transformation
        self.add_class("pysparkgui-overflow-visible")

        self.database = Singleselect(
            placeholder="Database - leave empty for default database",
            width="xl",
            on_change=lambda _: self._update_tables(),
        )
        self.database_hint_outlet = widgets.VBox()

        self.table = Singleselect(placeholder="Table", width="xl")

        for target in (self._update_databases, self._update_tables):
            Thread(target=target).start()

        self.children = [
            create_description_widget("Database"),
            self.database,
            self.database_hint_outlet,
            create_description_widget("Table"),
            self.table,
            self.transformation.spacer,
            self.transformation.new_df_name_group,
            self.transformation.execute_button,
        ]

    def _update_databases(self):
        self.database.options = self._list_databases()

    def _update_tables(self):
        try:
            options = self._list_tables(self.database.value)
            if options is DATABASE_DOES_NOT_EXIST:
                self.table.options = []
                msg = f"Database '{self.database.value}' does not exist. Most likely the database<br>" \
                      "was recently deleted. Please select a different database."
                self.database_hint_outlet.children = [notification(msg, type="error")]
            else:
                self.database_hint_outlet.children = []
                self.table.options = options
        except Exception as e:
            print(repr(e), sys.stderr)

    def _list_databases(self):
        return [result["databaseName"] for result in _spark.sql("show databases").collect()]

    def _list_tables(self, database):
        if database is None:
            cmd = "show tables"
        elif _spark.catalog.databaseExists(database):
            cmd = f"show tables from {database}"
        else:
            return DATABASE_DOES_NOT_EXIST

        return [result["tableName"] for result in _spark.sql(cmd).collect()]

    def is_valid_loader(self):
        if self.table.value is None:
            raise PysparkguiError("No Table selected.")
        return True

    def get_exception_message(self, exception):
        if "Table or view not found" in str(exception):
            database_name = (
                self.database.value if self.database.value is not None else "default"
            )
            return notification(
                f"""We were not able to find the table <b>{self.table.value}</b> in the database <b>{database_name}</b>.<br>
                Most likely the table or database were recently deleted.<br> 
                """,
                type="error",
            )
        return None

    def get_code(self):
        database_prefix = f"{self.database.value}." if self.database.value is not None else ""
        return f'{DF_NEW} = spark.table("{database_prefix}{self.table.value}")'


UNKNOWN_ERROR = notification("There was an unknown error. You can close the user interface and try again.", type="error")

class SparkAutocompletionLoaderForUC(widgets.VBox):
    def __init__(self, transformation, catalogs):
        super().__init__()
        self.transformation = transformation
        self.add_class("pysparkgui-overflow-visible")

        self.catalog = Singleselect(
            placeholder="Catalog",
            options=catalogs,
            on_change=lambda _: self._maybe_update_databases(),
            width="xl",
        )

        self.database = Singleselect(
            placeholder="Database/Schema",
            options=[],
            on_change=lambda _: self._maybe_update_tables(),
            width="xl",
        )
        self.database_hint_outlet = widgets.VBox()

        self.table = Singleselect(
            placeholder="Table",
            options=[],
            width="xl")
        self.table_hint_outlet = widgets.VBox()

        self.children = [
            create_description_widget("Catalog"),
            self.catalog,
            create_description_widget("Database/Schema"),
            self.database,
            self.database_hint_outlet,
            create_description_widget("Table"),
            self.table,
            self.table_hint_outlet,
            self.transformation.spacer,
            self.transformation.new_df_name_group,
            self.transformation.execute_button,
        ]

    def _maybe_update_databases(self):
        if self.catalog.value is None:
            self.database.value = None
            self.database.options = []
            self.database_hint_outlet.children = []
        else:
            self._update_databases()

    def _update_databases(self):
        try:
            databases = [result["databaseName"] for result in _spark.sql(f"show databases in {self.catalog.value}").collect()]
            self.database.options = databases
            if len(databases) == 0:
                self.database.value = None
                self.database_hint_outlet.children = [notification(f"There are no databases in {self.catalog.value} that you are allowed to see", type="error")]
            else:
                self.database_hint_outlet.children = []
        except Exception as exception:
            self.database_hint_outlet.children = [UNKNOWN_ERROR]
            self._print_error_to_stderr(exception)
            
    def _maybe_update_tables(self):
        if self.database.value is None:
            self.table.value = None
            self.table.options = []
            self.table_hint_outlet.children = []
        else:
            self._update_tables()
    
    def _update_tables(self):
        try:
            tables = [result["tableName"] for result in _spark.sql(f"show tables in {self.catalog.value}.{self.database.value}").collect()]
            self.table.options = tables
            if len(tables) == 0:
                self.table.value = None
                self.table_hint_outlet.children = [notification(f"There are no tables in {self.catalog.value}.{self.database.value} that you are allowed to see", type="error")]
            else:
                self.table_hint_outlet.children = []
        except Exception as exception:
            self.table_hint_outlet.children = [UNKNOWN_ERROR]
            self._print_error_to_stderr(exception)
            
    def _print_error_to_stderr(self, exception):
        # It seems like the most typical errors here are Py4JErrors where we cannot get a string representation
        # Also, it seems like we cannot get a traceback from Python.
        # However, we still log the repr to stderr hoping that we might see something.
        print(repr(exception), sys.stderr)

    def is_valid_loader(self):
        if self.catalog.value is None:
            raise PysparkguiError("No Catalog selected.")
        if self.database.value is None:
            raise PysparkguiError("No Database/Schema selected.")
        if self.table.value is None:
            raise PysparkguiError("No Table selected.")
        return True

    def get_exception_message(self, exception):
        # add empty method due to delegation in parent class
        return None

    def get_code(self):
        return f'{DF_NEW} = spark.table("{self.catalog.value}.{self.database.value}.{self.table.value}")'


class SparkLoaderWithoutAutocompletion(widgets.VBox):
    def __init__(self, transformation):
        super().__init__()
        self.transformation = transformation
        self.loader_hint = notification("""
        <b>No autocompletion:</b> Due to technical limitations there is no autocomplete yet.<br>
        As a workaround, you can use the Data tab in the navigation on the left to see available catalogs, databases, and tables.<br>
        """,
        type="info"
        )

        self.catalog = Text(
            description="Catalog",
            width="xl",
        )
        self.database = Text(
            description="Database/Schema",
            width="xl",
        )
        self.table = Text(
            description="Table",
            width="xl",
        )

        self.children = [
            self.loader_hint,
            self.catalog,
            self.database,
            self.table,
            self.transformation.spacer,
            self.transformation.new_df_name_group,
            self.transformation.execute_button,
        ]

    def _get_empty_text_input(self):
        for text_input in [self.catalog, self.database, self.table, self.dataframe_name]:
            if text_input.value == "":
                return text_input
        return None

    def is_valid_loader(self):
        empty_text_input = self._get_empty_text_input()
        if empty_text_input:
            raise PysparkguiError(f"{empty_text_input.description} is empty. Please enter a value")
        return True

    def get_exception_message(self, exception):
        # add empty method due to delegation in parent class
        return None

    def get_code(self):
        catalog = self.catalog.value.strip()
        database = self.database.value.strip()
        table = self.table.value.strip()
        return f"""{DF_NEW} = spark.table("{catalog}.{database}.{table}")"""


class SparkUCWorkaroundCodeGenerator(widgets.VBox):
    def __init__(self, transformation):
        super().__init__()
        self.transformation = transformation
        self.loader_hint = notification("""
        <b>Manual action needed:</b> pysparkgui cannot load tables from Unity Catalog yet.<br>
        As a workaround, you can run the code in a notebook cell and then continue to use pysparkgui.<br>
        The shown user interface helps you to write the necessary code.<br>
        Where to find the catalog, schema, table names? You can use the Data tab in the navigation bar on the left.""",
        type="info"
        )

        self.catalog = Text(
            description="Catalog",
            on_change=self._update_result,
            width="xl",
        )
        self.database = Text(
            description="Database/Schema",
            on_change=self._update_result,
            width="xl",
        )
        self.table = Text(
            description="Table",
            on_change=self._update_result,
            width="xl",
        )
        self.dataframe_name = Text(
            description="Table name within notebook",
            value = "df",
            on_change=self._update_result,
            width="xl",
        )

        self.result_outlet = widgets.VBox([notification("The code is shown after you fill in the inputs.", type="info")])

        self.copy_button = CopyButton(style="primary")
        self.code_output = CodeOutput(code="")

        self.children = [
            self.loader_hint,
            self.catalog,
            self.database,
            self.table,
            self.dataframe_name,
            self.transformation.spacer,
            self.result_outlet,
        ]

    def _get_empty_text_input(self):
        for text_input in [self.catalog, self.database, self.table, self.dataframe_name]:
            if text_input.value == "":
                return text_input
        return None

    def _update_result(self, text_widget):
        empty_text_input = self._get_empty_text_input()
        if empty_text_input:
            self.result_outlet.children = [notification(f"{empty_text_input.description} is empty. Please enter a value", type="warning")]
        else:
            code_string = self.get_code()

            self.copy_button.copy_string = code_string
            self.code_output.code = code_string
            self.result_outlet.children = [
                self.copy_button,
                self.code_output,
            ]

    def get_code(self):
        DF_NAME = self.dataframe_name.value
        return f"""
{DF_NAME} = spark.table("{self.catalog.value}.{self.database.value}.{self.table.value}")
{DF_NAME}
""".strip()

class DatabricksDatabaseTableLoader(LoaderPlugin):
    """
    Allows the user to load data from a databricks database table
    """

    name = "Databricks: Load database table"
    new_df_name_placeholder = "df"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if _spark is None:
            return  # continue with render and show error message
        else:
            self.output_outlet = widgets.VBox(layout={"height":"44em"})
            self.output_outlet.children = [widgets.HTML("Loading ...")]
            Thread(target=self._setup_appropriate_loader).start()

    def _setup_appropriate_loader(self):
        try:
            catalogs = [result["catalog"] for result in _spark.sql("show catalogs").collect()]
            is_uc_workspace = len(catalogs) >= 1
            spark_queries_work_from_ipywidgets = True
        except:
            is_uc_workspace = True
            spark_queries_work_from_ipywidgets = False

        if is_uc_workspace:
            if spark_queries_work_from_ipywidgets:
                self.loader = SparkAutocompletionLoaderForUC(self, catalogs)
            else:
                self.loader = SparkUCWorkaroundCodeGenerator(self)
        else:
            self.loader = SparkAutocompletionLoaderForNonUC(self)
        # self.loader = SparkAutocompletionLoaderForNonUC(self)

        self.output_outlet.children = [self.loader]

    def render(self):
        self.set_title("Databricks: Load database table")

        if _spark is None:
            self.set_content(notification(
                f"""This feature only works within the Databricks platform but it seems like you are currently outside of Databricks.<br>
                Please only run this feature from within Databricks.""",
                type="error",
            ))
        else:
            self.set_content(self.output_outlet)
    
    def is_valid_loader(self):
        return self.loader.is_valid_loader()

    def get_exception_message(self, exception):
        return self.loader.get_exception_message(exception)

    def get_code(self):
        return self.loader.get_code()


def create_description_widget(description):
    widget = widgets.HTML(description)
    widget.add_class("pysparkgui-text-label")
    return widget
