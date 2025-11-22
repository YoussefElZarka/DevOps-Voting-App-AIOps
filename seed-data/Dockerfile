FROM alpine/curl:latest

WORKDIR /app

# Copy the seed script
COPY generate-votes.sh .

# Make the script executable
RUN chmod +x generate-votes.sh

# The entrypoint is set in docker-compose.yml
# CMD ["./generate-votes.sh"]
