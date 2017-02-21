# dataset.py
# by James Fulford
# for dataset.py


class Dataset():
    """
    Holds entries of data with a given schema.
    Can have attributes that apply for all entries.
    """

    def __init__(self, dictionary, schema=None, attr_schema=None, save_loc="", error_loc=""):
        """
        Initializes:
            name
            save_path and error_path
            attributes and data
            logger
            schema (declarations and accessors)
            attr_schema
        Logs errors from:
            schema
                initialization
                validation
            attr_schema
                initialization
                validation
        """
        import _dataset_initializer as di
        from copy import deepcopy as dc
        from utils import Logger

        self.name = di.get_name(dictionary)
        self.save_path = di.get_save_path(dictionary, save_loc, name=self.name)
        self.error_path = di.get_error_path(dictionary, error_loc, name=self.name)
        self.attributes = dc(dictionary["attributes"])
        self.data = dc(dictionary["data"])

        self.logger = Logger(self.error_path)

        # SCHEMA
        self.schema = di.get_schema(dictionary, schema)
        self.declarations = self.schema.declarations
        self.accessors = self.schema.accessors
        self.editors = self.schema.editors
        for entry in self.data:
            self.schema.validate(entry)
        self.logger.log(self.schema.logger.errors, error_type="Schema")

        # ATTRIBUTE SCHEMA
        self.attr_schema = di.get_attr_schema(dictionary, attr_schema)
        self.attr_schema.validate(self.attributes)
        self.logger.log(self.attr_schema.logger.errors, error_type="AttrSchema")

        # DATAPOINTS
        from datapoint import Datapoint
        self.datapoints = map(lambda x: Datapoint(x, self.declarations, self.accessors, self.editors), self.data)

    def save(self, path=""):
        """
        Stores dataset in self.save_path.
        Can use Dataset.load to make new Dataset instance off of data
        """
        import utils
        save_path = self.save_path
        if path:
            save_path = path
        utils.save(self.dictionary(), save_path)
        self.logger.errors["Schema"] = self.schema.logger.errors
        self.logger.errors["AttrSchema"] = self.attr_schema.logger.errors
        self.logger.save()

    @staticmethod
    def load(path, save_loc="", error_loc=""):
        import os
        import utils
        ds = utils.load(os.path.abspath(path))
        sl = save_loc
        el = error_loc
        return Dataset(ds, save_loc=sl, error_loc=el)

    def dictionary(self):
        from copy import deepcopy as dc
        return {
            "name": self.name,
            "attributes": dc(self.attributes),
            "data": dc(self.data),
            "schema": dc(self.schema.dictionary),
            "attribute_schema": dc(self.attr_schema.dictionary),
            "save_path": self.save_path,
            "error_path": self.error_path
        }
    __dict__ = dictionary

    def redundantify(self, attr):
        """
        Provided attribute in attributes dictionary is removed
        and stored in every datapoint.
        Schemas are updated appropriately.
        """
        value = self.attributes[attr]
        for entry in self.data:  # add to each data entry
            entry[attr] = value
        del self.attributes[attr]

        # update schemas appropriately
        schema_type = self.attr_schema[attr]
        self.attr_schema.remove_attr(attr)
        self.schema[attr] = schema_type

    def access(self, variable_request):
        """
        Returns a list of data entries
        using accessor(s) by string in variable_request
        """
        if type(variable_request) is not list:
            acs = self.accessors[variable_request]
            return map(acs, self.data)
        else:
            report = []
            for entry in self.data:
                record = {}
                for var in variable_request:
                    acs = self.accessors[var]
                    record[var] = acs(entry)
                report.append(record)
            return report

    __getitem__ = access

    def write(self, variable, content):
        for i in range(len(self.datapoints)):
            self.datapoints[i].write(variable, content)

    def enumerate(self, variable):
        """
        Returns dictionary of unique values mapping to themselves.
        (Useful for constructing content variable in write)
        """
        import json
        values = map(self.accessors[variable], self.data)
        enum = {}
        def go_deeper(vals):
            if type(vals) is list:
                for val in vals:
                    go_deeper(val)
            else:
                enum[vals] = vals
        go_deeper(values)
        return enum

    def test(self, tests):
        for test in tests:
            for dp in self.datapoints:
                try:
                    passed = test(dp)
                    if passed is not True:
                        self.logger.log(passed, test.__name__)
                except(Exception, e):
                    msg = {
                        "datapoint": dp.dictionary,
                        "test": test.__name__,
                        "exception": e,
                    }
                    self.logger.log(msg, "Exception" + test.__name__)

    def __str__(self):
        import json
        return json.dumps(self.data, indent=4)

    def one_var_stats(self):
        reports = {}
        for var in self.accessors.keys():
            dps = self[var]
            decl = {}
            if var not in self.declarations.keys():
                if type(dps[0]) is list:
                    dps = map(len, self[var])
                    decl = {}
                    reports[var] = a.one_var_stats(dps, decl["stat_type"])
            else:
                dps = self[var]
                decl = self.declarations[var]
                reports[var] = a.one_var_stats(dps, decl["stat_type"])


    import merge
    merge = merge.merge
    __add__ = merge


