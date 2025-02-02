# Contributing to CareerCanvas.Jobs

## Getting Started

### Development Environment Setup

1. Fork the repository
2. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/CareerCanvas.Jobs.git
cd CareerCanvas.Jobs
```

3. Set up virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development Workflow

### 1. Branch Naming Convention

- Feature: feature/description
- Bug Fix: fix/description
- Documentation: docs/description
- Refactor: refactor/description

### 2. Code Style

- Follow PEP 8 guidelines
- Use type hints
- Maximum line length: 88 characters
- Use Black for code formatting
- Use isort for import sorting

### 3. Testing

- Write unit tests for new features
- Ensure all tests pass locally
- Maintain minimum 80% code coverage

```bash
pytest --cov=services tests/
```

### 4. Commit Guidelines

- Use conventional commits format
- Keep commits atomic and focused
- Include ticket number if applicable

```plaintext
feat(api): add new job search endpoint
fix(scraper): handle rate limit exceptions
docs(readme): update deployment instructions
```

## Pull Request Process

- Update documentation for new features
- Add or update tests
- Ensure CI pipeline passes
- Request review from maintainers
- Address review comments

## Code Review Guidelines

### What to Look For

- Code correctness
- Test coverage
- Documentation
- Performance implications
- Security considerations

### ### Best Practices

- Be constructive and respectful
- Explain your reasoning
- Suggest improvements
- Approve only when satisfied

## Additional Resources

- Project Board
- Issue Tracker
- Documentation
