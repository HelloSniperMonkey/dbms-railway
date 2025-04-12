```bash
python -m venv railway_venv                        
source railway_venv/bin/activate                   
pip install -r requirements.txt
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
        int train_id PK,FK
        int class_id PK,FK
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
        int passenger_id FK
        int concession_id FK
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
    
    TRAIN ||--o{ TRAIN_CLASS : has
    CLASS ||--o{ TRAIN_CLASS : belongs_to
    TRAIN ||--o{ SCHEDULE : has
    TRAIN ||--o{ ROUTE : follows
    STATION ||--o{ ROUTE : is_part_of
    STATION ||--|| TRAIN : is_source_of
    STATION ||--|| TRAIN : is_destination_of
    PASSENGER ||--o{ BOOKING : makes
    BOOKING ||--o{ TICKET : generates
    PASSENGER ||--o{ PASSENGER_CONCESSION : receives
    CONCESSION ||--o{ PASSENGER_CONCESSION : applied_to
    BOOKING ||--o{ PAYMENT : has
    TICKET ||--o{ CANCELLATION : may_have
    TRAIN ||--o{ SEAT : contains
    CLASS ||--o{ SEAT : categorizes
    PASSENGER ||--o{ TICKET : holds
    TRAIN ||--o{ TICKET : issues
    CLASS ||--o{ TICKET : specifies
    STATION ||--o{ TICKET : is_departure_for
    STATION ||--o{ TICKET : is_arrival_for
```
