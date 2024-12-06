from nautobot.apps.jobs import Job, register_jobs, FileVar
from nautobot.dcim.models import Location, LocationType
import us

class ImportLocations(Job):
    class Meta:
        name = "Import Locations"
    '''
    Imports WAYNES LOCATIONS from a CSV
    '''

    csv_file = FileVar(description="Upload a CSV file containing location data.")

    def _find_state(self, state_two_letters):
        state = us.states.lookup(str(state_two_letters))
        return state.name

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

    def run(self):
        pass

register_jobs(ImportLocations)



