# 🎬 Cinema Reservation System API

This project is a RESTful Cinema Reservation backend built using **Django REST Framework**. It allows users to browse movies and showtimes, book seats, manage their reservations, and handle payments via Stripe.

---

## 🚀 Features

- 🔐 JWT Authentication with OTP verification
- 🎥 Movie & showtime listings
- 🎟️ Seat booking with availability check
- 💳 Stripe payment integration
- 📬 Webhooks for payment confirmation
- 🧑 Admin capabilities (CRUD for movies/showtimes)

---

## 📦 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: SQLite (or customizable)
- **Auth**: JWT (SimpleJWT) + OTP
- **Payments**: Stripe

---

## 📂 Installation & Setup

```bash
git clone https://github.com/shahdamohamed/cinema-reservation.git
cd cinema-reservation

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Apply migrations and run server
python manage.py migrate
python manage.py runserver
```

---

## 🔐 Authentication Endpoints

| Method | Endpoint                          | Description                                  |
|--------|-----------------------------------|----------------------------------------------|
| POST   | `/api/users/register/`            | User registration                            |
| POST   | `/api/users/generate_otp/`        | Generating OTP                               |
| POST   | `/api/users/verify_otp/`          | Verify OTP                                   |
| POST   | `/api/reset-password/`            | Reset the user password                      |
| POST   | `/api/token/`                     | Obtain JWT tokens (login)                    |
| POST   | `/api/token/refresh/`             | Refresh JWT access token                     |
| POST   | `/api/token/logout/`              | Logout and blacklist token                   |

---

## 🎬 Movie & ShowTime API (via ViewSets)

| Method | Endpoint                | Description              |
|--------|-------------------------|--------------------------|
| GET    | `/api/movies/`          | List all movies          |
| GET    | `/api/movies/{id}/`     | Retrieve a movie         |
| GET    | `/api/show_times/`      | List all showtimes       |
| GET    | `/api/show_times/{id}/` | Retrieve a showtime      |
| GET    | `/api/seats/`           | List all seats           |
| GET    | `/api/seats/{id}/`      | Retrieve seat info       |

---

## 🕒 Extended Functional Endpoints

| Method | Endpoint                                | Description                            |
|--------|-----------------------------------------|----------------------------------------|
| GET    | `/api/showtime/<movie_id>/`            | Showtimes for a given movie            |
| GET    | `/api/available-seats/`                | List available seats for showtime      |
| POST   | `/api/reservation/`                    | Create a reservation                   |

---

## 💳 Stripe Payment Endpoints

| Method | Endpoint                                                 | Description                           |
|--------|----------------------------------------------------------|---------------------------------------|
| GET    | `/api/create-checkout-session/<reservation_id>/`        | Initiate Stripe checkout              |
| GET    | `/api/payment/success/`                                  | Payment success redirect              |
| GET    | `/api/payment/cancel/`                                   | Payment cancellation redirect         |
| POST   | `/api/webhook/`                                          | Stripe webhook for event listening    |
| GET    | `/api/payment-status/<reservation_id>/`                 | Check payment status                  |

---

## 📌 Project Structure

```bash
cinema-reservation/
├── cinema_reservation/     # Project settings
├── reservation/            # Main logic: movies, showtimes, seats, reservations
├── users/                  # Authentication & user management
```

---

Built with 💙 by [@shahdamohamed](https://github.com/shahdamohamed)