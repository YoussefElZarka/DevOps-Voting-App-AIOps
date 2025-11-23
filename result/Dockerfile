# Stage 1: Build
FROM node:20-slim as builder

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --production

# Stage 2: Final image
FROM node:20-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy installed modules and application code
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Change ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Command to run the application
CMD ["node", "server.js"]
