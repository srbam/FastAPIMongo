# FastAPI with MongoDB CRUD

This project is a simple CRUD application using **FastAPI** and **MongoDB**.

## Features

- **Create**: Add new items.
- **Read**: Retrieve items by `id`, `name`, `price`, `count`, or `category`.
- **Update**: Update an existing item.
- **Delete**: Remove an item by `id`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/srbam/FastAPIMongo.git
   cd FastAPIMongo
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
4. Run the application:
    ```bash
    uvicorn main:app --reload