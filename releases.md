# Current v0.2.0

# Release Notes - v0.2.0

## New Features

### PLOT Creation
- [NEW] Added a plot for the 20 products with the most variation in the last 30 days

### DB Backup
- [NEW] Instead csv backup, now the project has a .gz backup of the database

### FIX COTTO SERVICE
- [FIX] Fixed the Cotto service: it takes unit price when no kg price is available

### ADD SCRAP DIA SERVICE
- [NEW] Added scrap service for Dia Market

### ADD TWITTER SERVICE
- [NEW] Added tweet option for both bots
- [NEW] Added media upload option for both bots

### ADD CARREFOUR LIST

- Added list of products from Carrefour to the project in csv format
- Create seeder of products_markets for the Carrefour list

### ADD CARREFOUR SCRAP SERVICE

# Release Notes - v0.1.0

## New Features

### ADD FLASK SERVER

- Added a Flask server to the project to serve the model and the API.
- Created basic routes to interact with the model.

### IMPLEMENTS ALL SERVICES

- Backup csv-xlsx: Implemented a backup service to store data locally by creating a new date copy of prices.csv, prices_long_list.csv, prices.xlsx

- Telegram service: Implemented a Telegram service to send messages to a specific chat_id.

  - Implemented general messages of the calculated variation. General variation, products with more variation and products with more reduction.

- Variation calculation service: Implemented a service to calculate the variation between the last two prices of a specific product.

- Scrap service: Implemented a service to scrape the prices of a specific product from a specific website.

- DB Service: Implemented a service to store the scraped data in a database.

## Changes and Improvements

### Dockerized the project

- Dockerized the project to facilitate deployment and development.

### Moved to a modular structure inside /src

- Moved the project to a modular structure to facilitate the addition of new features.

### ENV & ENV.EXAMPLE

- Added the .env and .env.example files to facilitate the configuration of the project.

### README UPDATE

- Updated the README file with the new project structure and instructions.

# EXAMPLE OF A RELEASE FILE

# Release Notes - Version 1.0.0

## New Features

### Feature A

- Added Feature A to allow users to perform specific actions.
- Users can now access Feature A from the main menu.

### UI Enhancements

- Improved the user interface for a more intuitive experience.
- Added new icons and colors to enhance the system's aesthetics.

## Changes and Improvements

### Performance

- Made significant performance improvements, reducing load times by 30%.

### Security

- Implemented additional security measures to protect sensitive user data.

## Bug Fixes

- Fixed an issue causing the application to crash when performing certain actions.
- Corrected a design error causing overlapping elements on the home screen.

## Additional Notes

- Thank you to all our users for their ongoing support and feedback! Your suggestions help us continuously improve.
