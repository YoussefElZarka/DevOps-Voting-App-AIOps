FROM alpine/curl:latest

WORKDIR /app

# Copy the seed script
COPY generate-votes.sh .

RUN apk update && apk add apache2-utils 

RUN sed -i 's/\r$//' generate-votes.sh

# Make the script executable
RUN chmod +x generate-votes.sh

# The entrypoint is set in docker-compose.yml
# CMD ["./generate-votes.sh"]
