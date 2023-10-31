from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    DEBUG : bool = True
    FAKE_USER: str = ""
    FAKE_EMPLOYEE: str = ""
    PORT :int = 8090

    # POSTGRES CONFIGS
    POSTGRES_USER : str = ""
    POSTGRES_PASSWORD : str  = ""
    POSTGRES_DATABASE : str  = ""
    POSTGRES_PORT : str  = ""
    POSTGRES_HOST : str  = ""
    
    # ENCRYPTED CONFIG
    ENCRYPTION_KEY : str = ""

    # KAFKA CONFIGS
    KAFKA_ADDRESS : str  = ""
    KAFKA_ORGANIZATION_CREATED_EVENT : str  = "Organization.OrganizationCreatedEvent"
    KAFKA_USER_ID_WAS_SET : str  = "Keycloak.UserIdWasSet"
    KAFKA_FORM_SUBMITTED : str  = "form.submitted"
    KAFKA_RULE_ENGINE_FLOW_REACTIVATION : str  = "rule_engine.flow_reactivation"
    KAFKA_TRAFFIC_PAIRED : str  = "time_attendance.traffic_paired"

    # neo4j
    NEO4J_URL : str  = "localhost:7687"
    NEO4J_PASSWORD : str  = "password"

    # MONGODB CONFIGS
    MONGODB_URL : str  = ""
    MONGODB_DATABASE : str  = ""
    MONGODB_USERNAME : str  = ""
    MONGODB_PASSWORD : str  = ""

    # REDIS CONFIGS
    REDIS_HOST : str  = ""
    REDIS_PORT : str  = ""
    REDIS_USER : str  = ""
    REDIS_PASSWORD : str  = ""

    # s3 config
    S3_ENDPOINT : str  = ""
    S3_BUCKET : str  = ""
    S3_ACCESS_KEY : str  = ""
    S3_SECRET_KEY : str  = ""

    GOOGLE_CLIENT_ID : str  = ""
    GOOGLE_CLIENT_SECRET : str  = ""

    # kavenegar
    KAVENEGAR_ACCESS_KEY : str  = ""

    #Auth
    SECRET_KEY : str  = ""
    ALGORITHM : str  = ""
    ACCESS_TOKEN_EXPIRE_MINUTES : str = ""

    class Config:
        case_sensitive = False
        BASE_DIR = Path(__file__).resolve().parent.parent
        env_file = (str(BASE_DIR) + "/.env").replace("//", "/")
        env_file_encoding = 'utf-8'

config = Config()


# class PasswordConfig:
#     MIN_LENGTH = 8
#     UPPERCASE_REQUIRED = False
#     LOWERCASE_REQUIRED = True
#     DIGIT_REQUIRED = True
#     SPECIAL_CHARACTERS_REQUIRED = False
#     SPECIAL_CHARACTERS = r"[!@#$%^&*()]"
