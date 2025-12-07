class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(self, incident_id: int, incident_type: str, severity: str, status: str, description: str):
        self.__id = incident_id
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description