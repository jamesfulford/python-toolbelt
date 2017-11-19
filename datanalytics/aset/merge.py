# merge.py
# by James Fulford


# currently doesn't work
def merge(self, dataset, log_collisions=True):
        """
        Returns new dataset composed of two given datasets.
        """
        from copy import deepcopy as dc
        result = {}

        def get_all_attributes(this, other):
            """
            Returns list of union of keys of both datasets' attributes
            """
            attrs = dc(this.attributes.keys())
            for key in other.attributes.keys():
                if key not in attrs:
                    attrs.append(dc(key))
            return attrs

        r_attr = get_all_attributes(self, dataset)
        for attr in r_attr:
            try:
                if(self.attributes[attr] is not dataset.attributes[attr]):
                    #
                    # TODO: change these to avoid side effects
                    self.redundantify(attr)
                    dataset.redundantify(attr)
            except KeyError:
                # attr wasn't in one of the datasets.
                # attr not in self.attributes; this too shall
                pass

        # DATA
        def get_id_accessor(ds):
            # Returns function which:
            #   when given entry, returns value of id.
            #   uses schema to find id.
            for decl in ds.declarations:
                if("id" in ds.declarations[decl].keys()):
                    # TODO: return an Extractor, not a lambda!
                    return(lambda x: x[decl])

        self_id_acs = get_id_accessor(self)
        other_id_acs = get_id_accessor(dataset)

        data = {}
        for entry in self.data:
            this_id = self_id_acs(entry)
            data[this_id] = dc(entry)
        for entry in dataset.data:
            that_id = other_id_acs(entry)
            if(that_id not in data.keys()):
                data[that_id] = dc(entry)
            else:
                # collision
                # fields that are the same besides id
                # should be logged if log_collisions.
                # Other fields should fall into place?
                pass
        result["data"] = map(lambda key: data[key], data.keys())

        # SCHEMA
        # ATTRIBUTE SCHEMA
        # NAME