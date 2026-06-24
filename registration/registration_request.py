class RegistrationRequest:
    def __init__(
        self,
        request_id,
        full_name,
        dob,
        gender,
        citizen_id,
        email,
        phone,
        password
    ):
        self.request_id = request_id
        self.full_name = full_name
        self.dob = dob
        self.gender = gender
        self.citizen_id = citizen_id
        self.email = email
        self.phone = phone
        self.password = password

        self.status = "Pending"
        self.reject_reason = ""

    def approve(self):
        self.status = "Approved"

    def reject(self, reason):
        self.status = "Rejected"
        self.reject_reason = reason