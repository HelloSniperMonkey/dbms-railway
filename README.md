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
    TRAIN ||--o{ TRAIN_CLASS : has
    CLASS ||--o{ TRAIN_CLASS : belongs_to
    TRAIN ||--o{ SCHEDULE : has
    TRAIN ||--o{ ROUTE : follows
    STATION ||--o{ ROUTE : includes
    PASSENGER ||--o{ BOOKING : makes
    BOOKING ||--o{ TICKET : includes
    PASSENGER ||--o{ PASSENGER_CONCESSION : receives
    CONCESSION ||--o{ PASSENGER_CONCESSION : offers
    BOOKING ||--o{ PAYMENT : has
    TICKET ||--o{ CANCELLATION : may_have
    TRAIN ||--o{ SEAT : provides
    CLASS ||--o{ SEAT : categorizes
    PASSENGER ||--o{ TICKET : holds
    TRAIN ||--o{ TICKET : issues
    CLASS ||--o{ TICKET : specifies
    STATION ||--o{ TICKET : departs_from
    STATION ||--o{ TICKET : arrives_at

    TRAIN {
        train_id
        train_name
        train_type
    }
    CLASS {
        class_id
        class_name
        base_fare_per_km
    }
    TRAIN_CLASS {
        train_id
        class_id
        total_seats
        available_seats
    }
    STATION {
        station_id
        station_name
        station_code
        city
        state
    }
    ROUTE {
        route_id
        train_id
        sequence_number
        station_id
        arrival_time
        departure_time
        distance_from_source
    }
    SCHEDULE {
        schedule_id
        train_id
        running_days
        start_date
        end_date
    }
    SEAT {
        seat_id
        train_id
        class_id
        seat_number
        journey_date
        status
    }
    PASSENGER {
        passenger_id
        name
        age
        gender
        mobile
        email
        proof_type
        proof_number
    }
    CONCESSION {
        concession_id
        concession_type
        discount_percentage
        description
    }
    PASSENGER_CONCESSION {
        passenger_id
        concession_id
        valid_until
    }
    BOOKING {
        booking_id
        passenger_id
        schedule_id
        booking_date
        booking_type
        booking_status
    }
    TICKET {
        ticket_id
        pnr_number
        booking_id
        passenger_id
        train_id
        class_id
        journey_date
        from_station_id
        to_station_id
        seat_number
    }
    PAYMENT {
        payment_id
        booking_id
        amount
        payment_date
        payment_method
        payment_status
    }
    CANCELLATION {
        cancellation_id
        ticket_id
        cancellation_date
        refund_amount
        refund_status
    }
```
