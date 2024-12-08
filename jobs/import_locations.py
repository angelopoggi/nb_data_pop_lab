from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Location, LocationType
from nautobot.core.api.parsers import NautobotCSVParser
import csv
from io import TextIOWrapper
from .state_abbreviations import STATE_ABBREVIATIONS

class ImportLocations(Job):
    class Meta:
        name = "Import Locations"

    csv_file = FileVar(description="Upload a CSV file containing location data.")


    def _find_state(self, state_two_letters):
        state = STATE_ABBREVIATIONS.get(state_two_letters)
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
            with csv_file.open(mode="rb") as file:
                #chatGPT helped me at this part - I brute forced it until I figured it out
                text_file = TextIOWrapper(file, encoding="utf-8")
                csv_reader = csv.DictReader(text_file)
                for row in csv_reader:
                    state = self._find_state(row['state'])
                    location_type = self._get_location_type(row['name'])
                    self.logger.info(f"State: {state}, Site Name: {row['name']}, Location Type: {location_type}")

register_jobs(ImportLocations)



