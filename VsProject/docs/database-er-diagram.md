# Database / ER Diagram

The application uses Django's built-in `auth_user` table for passenger and staff identities. A driver can optionally be linked one-to-one with an account. All application records use Django's generated integer primary keys unless otherwise constrained below.

```mermaid
erDiagram
    USER ||--o| DRIVER : "optional driver profile"
    ROUTE ||--o{ STOP : contains
    ROUTE ||--o{ TRIP : serves
    VEHICLE ||--o{ TRIP : assigned
    DRIVER ||--o{ TRIP : operates
    USER }o--o{ TRIP : passenger
    TRIP ||--o{ GPS_LOCATION : records

    USER {
        bigint id PK
        string username UK
        string password
        boolean is_staff
    }
    VEHICLE {
        bigint id PK
        string registration_number UK
        string make
        string model
        smallint capacity
        boolean active
    }
    DRIVER {
        bigint id PK
        bigint user_id FK "nullable, unique"
        string full_name
        string license_number UK
        string phone
        boolean active
    }
    ROUTE {
        bigint id PK
        string name UK
        string origin
        string destination
        boolean active
    }
    STOP {
        bigint id PK
        bigint route_id FK
        string name
        smallint sequence
        decimal latitude
        decimal longitude
    }
    TRIP {
        bigint id PK
        bigint route_id FK
        bigint vehicle_id FK
        bigint driver_id FK
        datetime scheduled_departure
        string status
        datetime started_at
        datetime completed_at
    }
    TRIP_PASSENGERS {
        bigint id PK
        bigint trip_id FK
        bigint user_id FK
    }
    GPS_LOCATION {
        bigint id PK
        bigint trip_id FK
        decimal latitude
        decimal longitude
        datetime recorded_at
    }
```

`STOP` sequence is unique within each route. Trip vehicle, driver, and route references are protected from deletion while assigned; deleting a route cascades to its stops. GPS records are deleted with their trip. The trip/passenger relationship is a Django-generated many-to-many join table.