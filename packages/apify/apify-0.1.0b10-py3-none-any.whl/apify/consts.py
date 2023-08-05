from enum import Enum
from typing import List, Literal, get_args


class ActorEventType(str, Enum):
    """Possible values of actor event type."""

    #: Info about CPU usage of the actor
    CPU_INFO = 'cpuInfo'
    #: Info about resource usage of the actor
    SYSTEM_INFO = 'systemInfo'
    #: Sent when the actor is about to migrate
    MIGRATING = 'migrating'
    #: Sent when the actor should persist its state (every minute or when migrating)
    PERSIST_STATE = 'persistState'
    #: Sent when the actor is aborting
    ABORTING = 'aborting'


class ApifyEnvVars(str, Enum):
    """Possible Apify env vars."""

    ACT_ID = 'APIFY_ACT_ID'
    ACT_RUN_ID = 'APIFY_ACT_RUN_ID'
    ACTOR_BUILD_ID = 'APIFY_ACTOR_BUILD_ID'
    ACTOR_BUILD_NUMBER = 'APIFY_ACTOR_BUILD_NUMBER'
    ACTOR_EVENTS_WS_URL = 'APIFY_ACTOR_EVENTS_WS_URL'
    ACTOR_ID = 'APIFY_ACTOR_ID'
    ACTOR_RUN_ID = 'APIFY_ACTOR_RUN_ID'
    ACTOR_TASK_ID = 'APIFY_ACTOR_TASK_ID'
    API_BASE_URL = 'APIFY_API_BASE_URL'
    API_PUBLIC_BASE_URL = 'APIFY_API_PUBLIC_BASE_URL'
    CHROME_EXECUTABLE_PATH = 'APIFY_CHROME_EXECUTABLE_PATH'
    CONTAINER_PORT = 'APIFY_CONTAINER_PORT'
    CONTAINER_URL = 'APIFY_CONTAINER_URL'
    DEDICATED_CPUS = 'APIFY_DEDICATED_CPUS'
    DEFAULT_BROWSER_PATH = 'APIFY_DEFAULT_BROWSER_PATH'
    DEFAULT_DATASET_ID = 'APIFY_DEFAULT_DATASET_ID'
    DEFAULT_KEY_VALUE_STORE_ID = 'APIFY_DEFAULT_KEY_VALUE_STORE_ID'
    DEFAULT_REQUEST_QUEUE_ID = 'APIFY_DEFAULT_REQUEST_QUEUE_ID'
    DISABLE_BROWSER_SANDBOX = 'APIFY_DISABLE_BROWSER_SANDBOX'
    DISABLE_OUTDATED_WARNING = 'APIFY_DISABLE_OUTDATED_WARNING'
    FACT = 'APIFY_FACT'
    HEADLESS = 'APIFY_HEADLESS'
    INPUT_KEY = 'APIFY_INPUT_KEY'
    INPUT_SECRETS_PRIVATE_KEY_FILE = 'APIFY_INPUT_SECRETS_PRIVATE_KEY_FILE'
    INPUT_SECRETS_PRIVATE_KEY_PASSPHRASE = 'APIFY_INPUT_SECRETS_PRIVATE_KEY_PASSPHRASE'
    IS_AT_HOME = 'APIFY_IS_AT_HOME'
    LOCAL_STORAGE_DIR = 'APIFY_LOCAL_STORAGE_DIR'
    LOG_FORMAT = 'APIFY_LOG_FORMAT'
    LOG_LEVEL = 'APIFY_LOG_LEVEL'
    MEMORY_MBYTES = 'APIFY_MEMORY_MBYTES'
    META_ORIGIN = 'APIFY_META_ORIGIN'
    PERSIST_STORAGE = 'APIFY_PERSIST_STORAGE'
    PROXY_HOSTNAME = 'APIFY_PROXY_HOSTNAME'
    PROXY_PASSWORD = 'APIFY_PROXY_PASSWORD'
    PROXY_PORT = 'APIFY_PROXY_PORT'
    PROXY_STATUS_URL = 'APIFY_PROXY_STATUS_URL'
    SDK_LATEST_VERSION = 'APIFY_SDK_LATEST_VERSION'
    STARTED_AT = 'APIFY_STARTED_AT'
    TIMEOUT_AT = 'APIFY_TIMEOUT_AT'
    TOKEN = 'APIFY_TOKEN'
    USER_ID = 'APIFY_USER_ID'
    WORKFLOW_KEY = 'APIFY_WORKFLOW_KEY'
    XVFB = 'APIFY_XVFB'

    # Extra ones not in @apify/consts:
    METAMORPH_AFTER_SLEEP_MILLIS = 'APIFY_METAMORPH_AFTER_SLEEP_MILLIS'
    PERSIST_STATE_INTERVAL_MILLIS = 'APIFY_PERSIST_STATE_INTERVAL_MILLIS'
    PURGE_ON_START = 'APIFY_PURGE_ON_START'


_INTEGER_ENV_VARS_TYPE = Literal[
    ApifyEnvVars.CONTAINER_PORT,
    ApifyEnvVars.DEDICATED_CPUS,
    ApifyEnvVars.LOG_LEVEL,
    ApifyEnvVars.MEMORY_MBYTES,
    ApifyEnvVars.METAMORPH_AFTER_SLEEP_MILLIS,
    ApifyEnvVars.PERSIST_STATE_INTERVAL_MILLIS,
    ApifyEnvVars.PROXY_PORT,
]

INTEGER_ENV_VARS: List[_INTEGER_ENV_VARS_TYPE] = list(get_args(_INTEGER_ENV_VARS_TYPE))

_BOOL_ENV_VARS_TYPE = Literal[
    ApifyEnvVars.DISABLE_BROWSER_SANDBOX,
    ApifyEnvVars.DISABLE_OUTDATED_WARNING,
    ApifyEnvVars.HEADLESS,
    ApifyEnvVars.IS_AT_HOME,
    ApifyEnvVars.PERSIST_STORAGE,
    ApifyEnvVars.PURGE_ON_START,
    ApifyEnvVars.XVFB,
]

BOOL_ENV_VARS: List[_BOOL_ENV_VARS_TYPE] = list(get_args(_BOOL_ENV_VARS_TYPE))

_DATETIME_ENV_VARS_TYPE = Literal[
    ApifyEnvVars.STARTED_AT,
    ApifyEnvVars.TIMEOUT_AT,
]

DATETIME_ENV_VARS: List[_DATETIME_ENV_VARS_TYPE] = list(get_args(_DATETIME_ENV_VARS_TYPE))

_STRING_ENV_VARS_TYPE = Literal[
    ApifyEnvVars.ACT_ID,
    ApifyEnvVars.ACT_RUN_ID,
    ApifyEnvVars.ACTOR_BUILD_ID,
    ApifyEnvVars.ACTOR_BUILD_NUMBER,
    ApifyEnvVars.ACTOR_EVENTS_WS_URL,
    ApifyEnvVars.ACTOR_ID,
    ApifyEnvVars.ACTOR_RUN_ID,
    ApifyEnvVars.ACTOR_TASK_ID,
    ApifyEnvVars.API_BASE_URL,
    ApifyEnvVars.API_PUBLIC_BASE_URL,
    ApifyEnvVars.CHROME_EXECUTABLE_PATH,
    ApifyEnvVars.CONTAINER_URL,
    ApifyEnvVars.DEFAULT_BROWSER_PATH,
    ApifyEnvVars.DEFAULT_DATASET_ID,
    ApifyEnvVars.DEFAULT_KEY_VALUE_STORE_ID,
    ApifyEnvVars.DEFAULT_REQUEST_QUEUE_ID,
    ApifyEnvVars.FACT,
    ApifyEnvVars.INPUT_KEY,
    ApifyEnvVars.INPUT_SECRETS_PRIVATE_KEY_FILE,
    ApifyEnvVars.INPUT_SECRETS_PRIVATE_KEY_PASSPHRASE,
    ApifyEnvVars.LOCAL_STORAGE_DIR,
    ApifyEnvVars.LOG_FORMAT,
    ApifyEnvVars.META_ORIGIN,
    ApifyEnvVars.PROXY_HOSTNAME,
    ApifyEnvVars.PROXY_PASSWORD,
    ApifyEnvVars.PROXY_STATUS_URL,
    ApifyEnvVars.SDK_LATEST_VERSION,
    ApifyEnvVars.TOKEN,
    ApifyEnvVars.USER_ID,
    ApifyEnvVars.WORKFLOW_KEY,
]

STRING_ENV_VARS: List[_STRING_ENV_VARS_TYPE] = list(get_args(_STRING_ENV_VARS_TYPE))


class StorageTypes(str, Enum):
    """Possible Apify storage types."""

    DATASET = 'Dataset'
    KEY_VALUE_STORE = 'Key-value store'
    REQUEST_QUEUE = 'Request queue'


DEFAULT_API_PARAM_LIMIT = 1000

REQUEST_ID_LENGTH = 15

REQUEST_QUEUE_HEAD_MAX_LIMIT = 1000
