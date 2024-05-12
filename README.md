# Bank
## Environments
### **PostgreSQL**
- **Db__PROVIDER** -  Specifies the database provider (Default: postgresql+psycopg_async)
- **Db__HOST** - The host where the PostgreSQL server is running (Default: localhost)
- **Db__PORT** - The port on which the PostgreSQL server is listening. (Default: 5432)
- **Db__USER** - The username for database access. (Default: postgres)
- **Db__PASSWORD** - The password for database access. (Default: 12345678)
- **Db__NAME** - The name of the database to be used. (Default: mts-postgresql)

### **JWT**
- **secret** - The secret key used for signing JWT tokens. (Default: openssl rand -hex 32)
- **algorithm** - The algorithm used for signing JWT tokens. (Default: HS256)
- **access_exp** - The expiration time for access tokens in seconds.
- **refresh_exp** - The expiration time for refresh tokens in seconds.

## Docker-compose
Example of docker-compose stored in **deployment/docker-compose.yml**
## API
API stored in directory **api/openapi.yaml**