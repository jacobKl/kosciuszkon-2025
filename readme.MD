
# Kościuszkon 2025 – Solar Energy Cost Calculator

This project, named GreenHouse, was developed during the 3rd edition of **Kościuszkon**.

## Overview

The **Solar Energy Cost Calculator** is a web application designed to help users estimate the costs and potential savings associated with installing a photovoltaic (PV) system.  
Users can manually input data about their planned solar installation and utilize auxiliary tools such as:

- **3D visualization** of the installation
- **Predictive model** estimating average household electricity consumption based on provided parameters

The platform provides information on costs, potential savings, eligible subsidies, and allows users to download a detailed report of the calculations.

## Technologies Used

- **Frontend:** [React.js](https://reactjs.org/), [Three.js](https://threejs.org/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Machine Learning:** [scikit-learn](https://scikit-learn.org/), trained on the [RECS](https://www.eia.gov/consumption/residential/) dataset
- **Containerization:** [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/)
- **Maps:** [OpenStreetMap API](https://www.openstreetmap.org/) for interactive building visualization

## Project Structure

The repository is organized as follows:

- `frontend/` – Contains the React.js application with Three.js integration for 3D visualization.
- `backend/` – Contains the FastAPI application, including the scikit-learn model for consumption estimation.
- `ai/` – Contains the machine learning model and dataset.
- `docker-compose.yml` – Docker Compose configuration file for setting up the development environment.

## Getting Started

To run the application locally using Docker Compose:

1. Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/jacobKl/kosciuszkon-2025.git
   cd kosciuszkon-2025
   ```
3. Build and start the containers:
   ```bash
   docker-compose up --build -d
   ```
4. Access the application at [http://localhost:8080](http://localhost:8081) in your web browser.

## Future Development

Potential enhancements for the project include:

- Improving user assistance features, such as 3D visualization, tooltips, and estimations.
- Expanding project management capabilities for photovoltaic installations.
- Integrating with external systems, such as photovoltaic panel manufacturers, for real-time data and product information.
