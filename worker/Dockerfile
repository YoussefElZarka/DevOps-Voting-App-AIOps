# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["Worker.csproj", "./"]
RUN dotnet restore "./Worker.csproj"
COPY . .
RUN dotnet publish "Worker.csproj" -c Release -o /app/publish

# Stage 2: Final image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy published application from build stage
COPY --from=build /app/publish .

# Expose the port the app runs on (if any, worker is usually headless)
# EXPOSE 8080

# Switch to the non-root user
USER appuser

# Command to run the application
ENTRYPOINT ["dotnet", "Worker.dll"]
