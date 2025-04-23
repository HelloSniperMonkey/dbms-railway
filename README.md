```bash
mysql -u railway -p railway < dump.sql 
mysql -u railway -p railway < new.sql # if you are having trouble doing it with dump.sql

python -m venv railway_venv                        
source railway_venv/bin/activate                   
pip install -r requirements.txt
streamlit run railway_app.py
```
```mermaid
erDiagram
    TRAIN {
        int train_id PK
        string train_name
        string train_type
        int total_seats
        int source_station_id FK
        int destination_station_id FK
    }

    TRAIN_CLASS {
        int train_id PK, FK
        int class_id PK, FK
        int total_seats
        int available_seats
    }

    CLASS {
        int class_id PK
        string class_name
        float base_fare_per_km
    }

    STATION {
        int station_id PK
        string station_name
        string station_code
        string city
        string state
    }

    ROUTE {
        int route_id PK
        int train_id FK
        int sequence_number
        int station_id FK
        time arrival_time
        time departure_time
        float distance_from_source
    }

    SCHEDULE {
        int schedule_id PK
        int train_id FK
        string running_days
        date start_date
        date end_date
    }

    SEAT {
        int seat_id PK
        int train_id FK
        int class_id FK
        string seat_number
        date journey_date
        string status
    }

    PASSENGER {
        int passenger_id PK
        string name
        int age
        string gender
        string mobile
        string email
        string proof_type
        string proof_number
    }

    CONCESSION {
        int concession_id PK
        string concession_type
        float discount_percentage
        string description
    }

    PASSENGER_CONCESSION {
        int passenger_id PK, FK
        int concession_id PK, FK
        date valid_until
    }

    BOOKING {
        int booking_id PK
        int passenger_id FK
        int schedule_id FK
        date booking_date
        string booking_type
        string booking_status
    }

    TICKET {
        int ticket_id PK
        string pnr_number
        int booking_id FK
        int passenger_id FK
        int train_id FK
        int class_id FK
        date journey_date
        int from_station_id FK
        int to_station_id FK
        string seat_number
    }

    PAYMENT {
        int payment_id PK
        int booking_id FK
        float amount
        datetime payment_date
        string payment_method
        string payment_status
    }

    CANCELLATION {
        int cancellation_id PK
        int ticket_id FK
        date cancellation_date
        float refund_amount
        string refund_status
    }

    TRAIN ||--o{ TRAIN_CLASS : offers
    CLASS ||--o{ TRAIN_CLASS : includes
    TRAIN ||--o{ SCHEDULE : scheduled_as
    TRAIN ||--o{ ROUTE : has_route
    STATION ||--o{ ROUTE : part_of
    STATION ||--|| TRAIN : is_source
    STATION ||--|| TRAIN : is_destination
    PASSENGER ||--o{ BOOKING : makes
    BOOKING ||--o{ TICKET : generates
    PASSENGER ||--o{ PASSENGER_CONCESSION : gets
    CONCESSION ||--o{ PASSENGER_CONCESSION : granted_to
    BOOKING ||--o{ PAYMENT : results_in
    TICKET ||--o{ CANCELLATION : may_result_in
    TRAIN ||--o{ SEAT : provides
    CLASS ||--o{ SEAT : consists_of
    PASSENGER ||--o{ TICKET : books
    TRAIN ||--o{ TICKET : contains
    CLASS ||--o{ TICKET : classifies
    STATION ||--o{ TICKET : start_from
    STATION ||--o{ TICKET : ends_at

```
