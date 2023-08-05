"""Little project to create a temparory connection to a psql database."""

__version__ = "1.3.0"

# First party imports
from tmp_connection_psql.tmp_connection_psql import (  # noqa: F401
    connect,
    tmp_connection,
)
