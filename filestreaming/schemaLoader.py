import csv

from interfaces.validationInterface import ValidationInterface
class SchemaLoader(object):

    """
    This class will load a schema file and writes the set of validation rules to validation database.

    """

    @staticmethod

    def loadFields(fileTypeName,schemaFileName):
        """
        Load schema file to create validation rules and removes existing
        schemas

        Arguments:
        schemaFileName -- filename of csv file that holds schema definition
        fileTypeName --  the type of file that the schema represents
        """

        #Step 1 Clean out the database
        database = ValidationInterface()
        database.removeRulesByFileType(fileTypeName)
        database.removeColumnsByFileType(fileTypeName)
        #Step 2 add the new fields
        with open(schemaFileName) as csvfile:
            reader = csv.DictReader(csvfile)
            for record in reader:
                if(SchemaLoader.checkRecord(record, ["fieldname","required","data_type"])) :
                    columnId = database.addColumnByFileType(fileTypeName,record["fieldname"].lower().replace(" ","_"),record["required"],record["data_type"])
                    if "field_length" in record:
                        # When a field length is specified, create a rule for it
                        length = record["field_length"].strip()
                        if(len(length) > 0):
                            # If there are non-whitespace characters here, create a length rule
                            database.addRule(columnId,"LENGTH",length,"Field must be no longer than specified limit")
                else :
                   raise ValueError('CSV File does not follow schema')

    @staticmethod
    def checkRecord (record, fields) :
        """ Returns True if all elements of fields are present in record """
        for data in fields:
            if ( not data in record ):
                return False
        return True

    @staticmethod
    def loadRules(fileTypeName, filename):
        """ Populate rule and multi_field_rule tables from rule rile

        Args:
            filename: File with rule specifications
        """
        validationDb = ValidationInterface()
        fileId = validationDb.getFileId(fileTypeName)
        ruleFile = open(filename)
        reader = csv.DictReader(ruleFile)
        for record in reader:
            if(record["is_single_field"].lower() == "true"):
                # Find column ID based on field name
                columnId = validationDb.getColumnId(record["field_name"],fileId)
                # Write to rule table
                validationDb.addRule(columnId,record["rule_type"],record["rule_text_one"],record["description"])
            else:
                # Write to multi_field_rule table
                validationDb.addMultiFieldRule(fileId,record["rule_type"],record["rule_text_one"],record["rule_text_two"],record["description"])