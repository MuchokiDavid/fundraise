# Fundraising App - Django Backend

[![Django](https://img.shields.io/badge/Django-3.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django backend for a fundraising platform similar to MsaadaFund, enabling users to create campaigns, donate to causes, and manage funds securely.

## Features

- **User Authentication**: Sign up, login, and profile management for donors and campaign creators
- **Campaign Management**: Create, edit, and manage fundraising campaigns
- **Wallet System**: Each campaign has its own wallet to track funds
- **Donation Processing**: Secure donation system with transaction history
- **Withdrawal System**: Request and approve withdrawals from campaign wallets
- **Admin Dashboard**: Manage users, campaigns, and withdrawals
- **Notifications**: Real-time updates for users about their campaigns and donations

## Models Overview

The application includes the following main models:

1. **User**: Custom user model with different roles (donor, campaign owner, admin)
2. **Campaign**: Fundraising campaigns with targets, progress tracking, and status
3. **CampaignWallet**: Wallet associated with each campaign to manage funds
4. **Donation**: Records of donations made to campaigns
5. **WithdrawalRequest**: Requests to withdraw funds from campaign wallets
6. **Transaction**: Complete history of all financial transactions
7. **Notification**: System notifications for users

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (recommended) or SQLite
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/muchokidavid/fundraiser.git
   cd fundraising-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the project root with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/fundraising_db
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

The API includes endpoints for:

- Authentication (JWT)
- User management
- Campaign CRUD operations
- Donation processing
- Wallet management
- Withdrawal requests
- Notifications

See the API documentation at `/api/docs/` after setting up the project.

## Configuration

Key settings in `settings.py`:

- `AUTH_USER_MODEL = 'app.User'` - Custom user model
- Database configuration (PostgreSQL recommended for production)
- Static and media file settings
- Email backend configuration
- Payment gateway integration settings

## Deployment

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Configure a production database
3. Set up a proper web server (Nginx + Gunicorn recommended)
4. Configure static files serving
5. Set up SSL/TLS for secure connections

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django framework
- MsaadaFund for inspiration
- All contributors and open-source libraries used