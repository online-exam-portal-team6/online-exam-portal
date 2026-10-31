# OEP-66: Login Sequence Diagram

**Status:** Intended design based on the SRS and authentication-view contract. Confirm future authentication-flow changes against the implementation before updating this diagram.

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant LoginView as Django Login View
    participant Auth as Django Authentication
    participant DB as Database

    User->>Browser: Open login page
    Browser->>LoginView: GET /accounts/login/
    LoginView-->>Browser: Return login form
    Browser-->>User: Display login form

    User->>Browser: Enter username/email and password
    Browser->>LoginView: POST credentials
    LoginView->>Auth: Authenticate credentials
    Auth->>DB: Retrieve user and verify password
    DB-->>Auth: User record or no matching user
    Auth-->>LoginView: Authentication result

    alt Credentials are valid
        LoginView->>LoginView: Establish authenticated session
        LoginView-->>Browser: Redirect according to user role
        Browser-->>User: Display student or admin dashboard
    else Credentials are invalid
        LoginView-->>Browser: Return form with error
        Browser-->>User: Display login error
    end
```
