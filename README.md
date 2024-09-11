# DEGEAI-Project v1.1

<h2>DEGEAI Application with Real-Time Data Integration, Machine Learning, and Face Tracking (v1.1)</h2>

This repository hosts version 1.1 of an AI application that combines real-time data processing, machine learning (ML) capabilities, and a face tracking and swapping system, all designed to operate independently without relying on third-party APIs. The application aims to provide a versatile foundation for developing modern AI-driven solutions across various domains.

<h2>Features</h2>
Real-Time Data Integration: The application collects and processes real-time data from various internet sources without relying on external APIs, ensuring greater control over data flow and enhancing privacy. It utilizes custom web scraping techniques and data parsing methods to keep information up-to-date and relevant.

Machine Learning Models: The application integrates several machine learning models using Python, JavaScript, and SQL for backend processing and data management. These models are capable of handling tasks such as data classification, regression analysis, and simple predictive analytics, providing a versatile foundation for building more complex models in the future.

Face Tracking and Swapping System: A face tracking and swapping module has been implemented using OpenCV and deep learning models. While functional, it is currently optimized for standard use cases, such as AR applications and interactive media, and is intended for further enhancement.

Modular Architecture with Scalability: The application is built with a modular architecture that allows for easy updates and expansions. The codebase is organized to support the integration of additional features, such as more advanced ML models, improved data handling, or enhanced face tracking algorithms.

No Dependence on Third-Party APIs: Unlike many AI applications that rely heavily on external APIs, this application is built to function independently, which enhances flexibility, data privacy, and security.

<h2>Current Status - Version 1.0</h2>
Version 1.1 represents the initial release, with a focus on establishing a solid and flexible foundation for future development. While the core functionality is in place, there are areas that need further refinement and optimization:

<h2>Known Limitations:</h2>

The face tracking and swapping system may experience slow performance under complex conditions or with high-resolution input. Optimization is needed to handle these cases more efficiently.
Current machine learning models are functional but are based on basic architectures; there is significant potential for further refinement and integration of more advanced algorithms.
Real-time data scraping and parsing methods are effective but could benefit from additional robustness and error handling for a broader range of web sources.
Planned Updates:

Performance Optimization: Future updates will focus on optimizing the speed and accuracy of the face tracking system and refining machine learning models for more specialized tasks.
Enhanced Real-Time Data Handling: Improvements will be made to expand data scraping capabilities and provide better support for dynamic source integration.
User Interface Enhancements: Plans are underway to modernize the user interface to offer a more streamlined and intuitive experience.
Bug Fixes and Stability Improvements: Ongoing efforts will address bugs and improve the overall stability and reliability of the system.
Technical Stack
Languages: Python, JavaScript, SQL.
Libraries and Frameworks: OpenCV for computer vision, TensorFlow and PyTorch for ML models, Node.js and Express.js for backend services, and SQL for data management.
Data Handling: Custom web scraping scripts and SQL databases for structured data management and integration with ML models.

<h2>Installation and Usage</h2>

<h3>Clone the Repository:</h3>
        ```
            git clone https://github.com/Dege34/DEGEAI-Project.git    
        ```

        
<h3>Install Dependencies: Install necessary dependencies using requirements.txt for Python and package.json for JavaScript.
bash</h3>

        <h4> pip install -r requirements.txt </h4>
        <h4> npm install </h4>
        
Run the Application: Set up the backend and frontend as described in the README.md file, and configure the environment for data scraping and ML processing.
Contribution
Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to submit a pull request or open an issue. Please follow the project's code of conduct when contributing.

<h2>License</h2>
This project is licensed under the MIT License - see the LICENSE file for more details.

<h2>Future Roadmap</h2>
Optimization and Expansion of ML Models: Incorporate more advanced ML models and improve the accuracy and speed of existing algorithms.
Dynamic Data Source Management: Expand support for adding new data sources dynamically and improving error handling for real-time data integration.
Enhanced UI/UX: Continuously improve the user interface to be more modern, user-friendly, and responsive.
Community Feedback Integration: Gather and incorporate feedback from the community to prioritize updates and new features.

<h2>Contact</h2>
For any questions, suggestions, or collaboration opportunities, please contact <h4>dege.bulte@studenti.polito.it</h4>.
