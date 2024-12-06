from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Location, LocationType
import csv

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

    def run(self, data):
        csv_file = data['csv_file']
        with csv_file.open(mode="r") as file:
            reader = csv.DictReader(file)
        for row in reader:
            logger.info(f"{row}")

register_jobs(ImportLocations)



