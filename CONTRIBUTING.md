# Contributing to Fundraising App

Thank you for considering contributing to our fundraising application! We welcome all contributions from the community to help make this project better.

## How to Contribute

### Reporting Issues

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, browser, Django/Python versions)

### Suggesting Enhancements

1. **Check the roadmap** (if available) for planned features
2. **Open an enhancement issue** with:
   - Clear description of the proposed feature
   - Use cases and benefits
   - Suggested implementation approach (optional)
   - Screenshots/mockups if relevant

### Making Code Contributions

#### Prerequisites
- Python 3.8+
- Django 3.2+
- Git

#### Contribution Workflow

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/your-username/fundraising-app.git
   ```
3. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
5. **Make your changes** following our coding standards
6. **Write tests** for new functionality
7. **Run tests**:
   ```bash
   python manage.py test
   ```
8. **Commit changes** with descriptive messages:
   ```bash
   git commit -m "feat: add campaign search functionality"
   ```
9. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
10. **Open a Pull Request** (PR) to the main repository

### Code Review Process

1. Maintainers will review your PR
2. You may receive feedback or requests for changes
3. Once approved, your PR will be merged
4. Your contribution will be included in the next release

## Coding Standards

### Python/Django Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use Django's coding style for model definitions, views, etc.
- Keep lines under 88 characters (use Black formatter)
- Use type hints where appropriate (Python 3.8+)

### Git Commit Messages

- Use [Conventional Commits](https://www.conventionalcommits.org/) style:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `chore:` for maintenance tasks
  - `refactor:` for code refactoring
  - `test:` for test-related changes
- Keep subject line under 50 characters
- Use body to explain what and why (not how)

### Testing Guidelines

- Write tests for all new functionality
- Follow Django's test case structure
- Aim for at least 80% test coverage
- Include both unit and integration tests

## Project Structure

```
fundraising_app/
├── core/               # Core functionality and settings
├── users/              # User authentication and profiles
├── campaigns/          # Campaign-related functionality
├── donations/          # Donation processing
├── wallets/            # Wallet management
├── templates/          # Django templates
├── static/             # Static files
├── tests/              # Test files
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## Getting Help

If you need help with your contribution:
- Join our [community chat] (if available)
- Comment on the relevant issue
- Email the maintainers at [maintainer@email.com]

## Code of Conduct

All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful and inclusive in all interactions.

---

Thank you for your interest in making our fundraising app better!
