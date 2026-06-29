from registration.registration_request import RegistrationRequest

requests = [
    RegistrationRequest(
        1,
        "Nguyen Van A",
        "2004-01-01",
        "Male",
        "123456789",
        "a@gmail.com",
        "0901234567",
        "123456"
    )
]

def view_requests():
    for req in requests:
        print(
            req.request_id,
            req.full_name,
            req.status
        )

def view_request_detail(request_id):
    for req in requests:
        if req.request_id == request_id:
            print("Name:", req.full_name)
            print("Email:", req.email)
            print("Phone:", req.phone)
            print("Citizen ID")