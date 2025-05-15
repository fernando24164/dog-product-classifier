# 🐾 Dog Product Classifier API

A high-performance API for intelligent categorization of dog products using AI-powered classification. Built with FastAPI and integrated with Groq's lightning-fast LLM inference.

[![Python 3.9+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-blue.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- AI-powered product classification using Groq's LLM inference
- RESTful API endpoints with automatic Swagger documentation
- Strict type validation with Pydantic models
- Confidence scoring and subcategory suggestions
- Production-ready architecture with dependency injection
- Comprehensive test coverage with pytest

## 📦 Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/fernando24164/dog-product-classifier.git
    cd dog-product-classifier
    ```
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3. **Set up environment variables**
    ```bash
    cp .env.example .env
    ```
4. Add your Groq API key to the .env file:
    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

## 🏃 Quick Start

1. **Start the FastAPI server**

```bash
uvicorn app.main:app --reload
```
2. Try the API

```bash
curl -X POST "http://localhost:8000/classify/" \
-H "Content-Type: application/json" \
-d '{"name": "Organic Dental Sticks", "description": "Natural dental chews for small dogs"}'
```

## 📚 API Documentation

Interactive documentation available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Endpoints:

- POST /classify/ - Classify dog products
- GET /health/ - Service health check

## 🔭 Testing

```bash
pytest
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the blazing-fast API framework
- Groq for the lightning-fast LLM inference
- Pydantic for robust data validation