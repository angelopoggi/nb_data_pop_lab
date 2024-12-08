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
            location_type = LocationType.objects.get(name="Branch")
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
                    #Find the state based on the two letter code
                    state = self._find_state(row['state'])
                    #Get the object, create if it doesn't exsist
                    state_object = LocationType.get_or_create(
                        name=state,
                        defaults = {
                            "name": state
                        }
                    )
                    #We also need the city object
                    city_object = Location.get_or_create(
                        name = row['city'],
                        defaults = {
                            "name": row['city'],
                            "parent":state_object
                        }
                    )
                    location_type = self._get_location_type(row['name'])
                    site_object, created = Location.objects.get_or_create(
                        name=row['name'],
                        defaults = {
                            "name": row['name'],
                            "location_type": location_type,
                            "parent" : city_object
                        }
                    )
                    if created:
                        self.logger.info(f"Created the Following Entry - State: {state}, Site Name: {row['name']}, Location Type: {location_type}")
                    else:
                        self.logger.info("Location already Exists")
register_jobs(ImportLocations)



