APP_CONTAINERFILE_NAME := app.Containerfile
APP_IMAGE_NAME := sod-app
APP_CONTAINER_PORT := 8000
APP_HOST_PORT := 8000

build-app-image:
	docker build -t $(APP_IMAGE_NAME) . -f $(APP_CONTAINERFILE_NAME)

run-app-image:
	docker run -p $(APP_HOST_PORT):$(APP_CONTAINER_PORT) $(APP_IMAGE_NAME)
