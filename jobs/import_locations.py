from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Location, LocationType
from nautobot.core.api.parsers import NautobotCSVParser
import csv
from io import BytesIO
import codecs

class ImportLocations(Job):
    class Meta:
        name = "Import Locations"

    csv_file = FileVar(description="Upload a CSV file containing location data.")

    STATE_ABBREVIATIONS = {
        "CA": "California",
        "VA": "Virginia",
        "NJ": "New Jersey",
        "IL": "Illinois",
    }

    def _find_state(self, state_two_letters):
        state = self.STATE_ABBREVIATIONS.get(state_two_letters)
        return state
    def _get_location_type(self, site_name):
        '''
        pass in the site name and return datacenter or branch
        :param site_name:
        :return: string
        '''
        if site_name.endswith("-DC"):
            #query NB data to get location Type UUID
            location_type = LocationType.objects.get(name="Data Center")
        elif site_name.endswith("-BR"):
            location_type = LocationType.objects.get(name="Data Center")
        if location_type:
            return location_type
        else:
            self.logger.error("unable to find location type")

    def run(self, csv_file=None):
        if csv_file:
            # data_encoding is utf-8 and file_encoding is utf-8-sig
            # Bytes read from the original file are decoded according to file_encoding, and the result is encoded using data_encoding.
            self.logger.info(type(csv_file))
            with csv_file.open(mode="r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.logger.info(row)

register_jobs(ImportLocations)



