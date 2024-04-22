.PHONY: start
start:
	@echo "Starting the server..."
	docker-compose up -d

.PHONY: stop
stop:
	@echo "Stopping the server..."
	docker-compose down

.PHONY: app-log
app-log:
	@echo "Showing the logs..."
	docker-compose logs -f app

.PHONY: reset
reset:
	@echo "Reseting server"
	docker-compose restart app
